import pandas as pd
import psycopg2
import os

# Koneksi ke PostgreSQL
conn = psycopg2.connect(
    dbname="fighter", user="postgres", password="lyra123", host="localhost", port="5432"
)
cur = conn.cursor()

# Folder tempat file CSV berada
csv_folder = "scraping/laptop/csv"

# Daftar file CSV yang ingin diproses
files_to_process = ["asus.csv", "hp.csv"]

for file in files_to_process:
    filepath = os.path.join(csv_folder, file)

    if not os.path.exists(filepath):
        print(f"⚠️ File tidak ditemukan: {file}")
        continue

    # Nama brand diambil dari nama file (contoh: "asus.csv" → "Asus")
    brand_nama = os.path.splitext(file)[0].capitalize()

    # Kategori default
    kategori_nama = "Laptop"

    # Sumber default
    sumber_nama = "Hartono"

    # Cek dan insert kategori
    cur.execute("SELECT id FROM kategori WHERE nama_kategori = %s", (kategori_nama,))
    kategori = cur.fetchone()
    if not kategori:
        cur.execute("INSERT INTO kategori (nama_kategori) VALUES (%s) RETURNING id", (kategori_nama,))
        kategori_id = cur.fetchone()[0]
    else:
        kategori_id = kategori[0]

    # Cek dan insert brand
    cur.execute("SELECT id FROM brand WHERE nama_brand = %s", (brand_nama,))
    brand = cur.fetchone()
    if not brand:
        cur.execute("INSERT INTO brand (nama_brand) VALUES (%s) RETURNING id", (brand_nama,))
        brand_id = cur.fetchone()[0]
    else:
        brand_id = brand[0]

    # Cek dan insert sumber
    cur.execute("SELECT id FROM sumber WHERE nama_sumber = %s", (sumber_nama,))
    sumber = cur.fetchone()
    if not sumber:
        cur.execute("INSERT INTO sumber (nama_sumber) VALUES (%s) RETURNING id", (sumber_nama,))
        sumber_id = cur.fetchone()[0]
    else:
        sumber_id = sumber[0]

    # Baca isi CSV
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    # Ganti nama kolom ke format sesuai dengan database
    df.rename(columns={
        "name": "Nama Produk",
        "price": "Harga",
        "link": "Link",
        "image": "Gambar"
    }, inplace=True)

    print(f"[INFO!] Memproses file: {file} | Jumlah data: {len(df)}")

    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO produk (nama_produk, harga, link, gambar, kategori_id, brand_id, sumber_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row["Nama Produk"], row["Harga"], row["Link"], row["Gambar"],
            kategori_id, brand_id, sumber_id
        ))


# Selesai
conn.commit()
cur.close()
conn.close()

print("Data dari file CSV yang dipilih berhasil dimasukkan ke PostgreSQL")
