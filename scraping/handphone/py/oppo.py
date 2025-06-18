import requests
from bs4 import BeautifulSoup
import csv
import time

# Setup
base_url = "https://myhartono.com/find/oppo"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

all_data = []

# Loop halaman hanya sampai 10
for page in range(1, 11):
    print(f"[INFO] Mengambil halaman {page}...")

    url = f"https://myhartono.com/find/oppo?page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div.ty-grid-list__item")
    print(f"[INFO] Produk ditemukan: {len(products)}")

    if not products:
        break

    for product in products:
        try:
            # Nama dan link
            name_tag = product.select_one("a.product-title")
            name = name_tag.get("title", "").strip() if name_tag else "N/A"
            link = name_tag.get("href", "").strip() if name_tag else ""
            if link and not link.startswith("http"):
                link = "https://myhartono.com" + link

            # Gambar
            image_tag = product.select_one("img.ty-pict.cm-image")
            image_url = image_tag.get("src", "").strip() if image_tag else ""

            # Harga
            price_tag = product.select_one("span[id^='sec_discounted_price']")
            price = price_tag.text.strip() if price_tag else "N/A"

            all_data.append([name, price, link, image_url])
        except Exception as e:
            print(f"[ERROR] Saat proses produk: {e}")

    time.sleep(1)

# Simpan ke CSV
with open("scraping/oppo.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Nama Produk", "Harga", "Link", "Gambar"])
    writer.writerows(all_data)

print("[DONE] Selesai! Data disimpan ke oppo.csv")
