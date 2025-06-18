import requests
from bs4 import BeautifulSoup
import csv
import time

# Setup
base_url = "https://myhartono.com/find/laptop+asus"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

all_data = []

# Loop halaman hanya sampai 10
for page in range(1, 11):  # dibatasi ke 10 halaman
    print(f"[INFO] Mengambil halaman {page}...")

    url = f"https://myhartono.com/find/laptop+asus?page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div.ty-grid-list__item")
    print(f"[INFO] Produk ditemukan: {len(products)}")

    if not products:
        break  # berhenti kalau tidak ada produk di halaman ini

    for product in products:
        try:
            name_tag = product.select_one("a.product-title")
            name = name_tag.get("title", "").strip()
            link = name_tag.get("href", "").strip()
            if not link.startswith("http"):
                link = "https://myhartono.com" + link

            price_tag = product.select_one("div.ty-grid-list__price")
            price = price_tag.text.strip() if price_tag else "N/A"

            image_tag = product.select_one("img.ty-pict.cm-image")
            image_url = image_tag.get("src", "").strip() if image_tag else ""

            all_data.append([name, price, link, image_url])
        except Exception as e:
            print(f"[ERROR] Saat proses produk: {e}")

    time.sleep(1)  # delay agar tidak diblok

# Simpan ke CSV
with open("scraping/asus.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Nama Produk", "Harga", "Link", "Gambar"])
    writer.writerows(all_data)

print("[DONE] Selesai! Data disimpan ke asus.csv")
