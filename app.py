import os
import psycopg2
from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi Database dan JWT
DB_URL = os.getenv("DB_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 1

# Buat koneksi database per permintaan
def get_db_connection():
    return psycopg2.connect(DB_URL)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "Selamat datang di halaman utama!"

@app.route("/api/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username dan password tidak boleh kosong"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "Username sudah terdaftar"}), 409

            hashed_password = generate_password_hash(password)
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                conn.commit()
                return jsonify({"success": True, "message": "Registrasi berhasil!"}), 201
            except Exception:
                conn.rollback()
                return jsonify({"success": False, "message": "Terjadi kesalahan server"}), 500

@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username dan password tidak boleh kosong"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if not user:
                return jsonify({"success": False, "message": "Username tidak ditemukan."}), 404

            user_id, db_username, db_password = user

            if check_password_hash(db_password, password):
                token = jwt.encode({
                    "username": db_username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
                }, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

                return jsonify({
                    "success": True,
                    "message": "Login berhasil!",
                    "username": db_username,
                    "id": user_id,
                    "token": token
                }), 200
            else:
                return jsonify({"success": False, "message": "Password salah!"}), 401

@app.route("/api/logout", methods=["POST", "OPTIONS"])
def logout():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200
    return jsonify({"success": True, "message": "Logout berhasil!"}), 200

@app.route("/api/protected", methods=["GET", "OPTIONS"])
def protected():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return jsonify({"success": True, "message": f"Selamat datang, {decoded_token['username']}!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token kedaluwarsa"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Token tidak valid"}), 401

@app.route('/api/product', methods=['GET'])
def get_product():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    produk.id, produk.nama_produk, produk.harga, produk.link, 
                    produk.gambar, sumber.nama_sumber, kategori.nama_kategori
                FROM produk
                JOIN sumber ON produk.sumber_id = sumber.id
                JOIN kategori ON produk.kategori_id = kategori.id
            """)
            products = cur.fetchall()
            result = [
                {
                    "id": p[0], "name": p[1], "price": p[2], "url": p[3],
                    "imageUrl": p[4], "store": p[5], "category": p[6]
                }
                for p in products
            ]
            return jsonify(result)

@app.route("/api/user/update", methods=["POST", "OPTIONS"])
def update_profile():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.json
    old_username = data.get("old_username", "").strip()
    new_username = data.get("new_username", "").strip()

    if not old_username or not new_username:
        return jsonify({"success": False, "message": "Data tidak lengkap"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (new_username,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "Username baru sudah digunakan"}), 409

            cur.execute("UPDATE users SET username = %s WHERE username = %s", (new_username, old_username))
            if cur.rowcount == 0:
                return jsonify({"success": False, "message": "Username lama tidak ditemukan"}), 404

            conn.commit()
            return jsonify({"success": True, "message": "Profil berhasil diperbarui"}), 200

@app.route('/api/save-product', methods=['POST'])
def save_product():
    data = request.get_json()
    user_id = data.get('user_id')
    produk_id = data.get('product', {}).get('id')

    if not user_id or not produk_id:
        return jsonify({"error": "Missing user_id or product_id"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM user_saved_products WHERE user_id=%s AND produk_id=%s", (user_id, produk_id))
            if cur.fetchone():
                return jsonify({"message": "Produk sudah disimpan"}), 200

            cur.execute("""
                INSERT INTO user_saved_products (user_id, produk_id)
                VALUES (%s, %s)
            """, (user_id, produk_id))
            conn.commit()
            return jsonify({"message": "Produk berhasil disimpan"}), 201

@app.route('/api/saved-products', methods=['GET'])
def get_saved_products():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, p.nama_produk, p.harga, p.link, p.gambar, s.nama_sumber
                FROM user_saved_products up
                JOIN produk p ON up.produk_id = p.id
                JOIN sumber s ON p.sumber_id = s.id
                WHERE up.user_id = %s
            """, (user_id,))
            result = cur.fetchall()
            produk_list = [
                {
                    "id": r[0], "name": r[1], "price": r[2], "url": r[3],
                    "imageUrl": r[4], "store": r[5]
                }
                for r in result
            ]
            return jsonify(produk_list), 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT nama_kategori FROM kategori")
            categories = cur.fetchall()
            result = [{"name": row[0].capitalize(), "slug": row[0].lower()} for row in categories]
            return jsonify(result), 200

@app.route("/api/search-history", methods=["POST"])
def save_search_history():
    data = request.get_json()
    user_id = data.get("user_id")
    query = data.get("query")

    if not user_id or not query:
        return jsonify({"success": False, "message": "Missing data"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO search_history (user_id, query, searched_at)
                VALUES (%s, %s, %s)
            """, (user_id, query, datetime.now(timezone.utc)))
            conn.commit()
            return jsonify({"success": True})

@app.route('/api/delete-saved-product', methods=['DELETE'])
def delete_saved_product():
    data = request.get_json()
    user_id = data.get('user_id')
    produk_id = data.get('produk_id')

    if not user_id or not produk_id:
        return jsonify({"error": "Missing user_id or produk_id"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM user_saved_products
                WHERE user_id = %s AND produk_id = %s
            """, (user_id, produk_id))
            conn.commit()
            return jsonify({"message": "Produk berhasil dihapus"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
