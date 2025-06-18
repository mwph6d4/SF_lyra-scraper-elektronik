from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Siapkan Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Ganti path ini dengan lokasi chromedriver.exe milikmu
chrome_driver_path = r"C:\Users\Lyra Geyska\single-template-copy\chromedriver.exe"
service = Service(chrome_driver_path)

# Inisialisasi driver
driver = webdriver.Chrome(service=service, options=options)

# Akses URL target
url = "https://store.acer.com/en-id/catalogsearch/result/?q=laptop&product_list_limit=all"
driver.get(url)

# Tunggu sampai produk muncul
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-item")))

# Ambil semua elemen produk
products = driver.find_elements(By.CSS_SELECTOR, "li.product-item")

# Ambil data produk
data = []
for product in products:
    try:
        name = product.find_element(By.CSS_SELECTOR, ".product-item-name a").text.strip()
        link = product.find_element(By.CSS_SELECTOR, ".product-item-name a").get_attribute("href")
        price = product.find_element(By.CSS_SELECTOR, ".price").text.strip()
        image = product.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        data.append({
            "name": name,
            "price": price,
            "link": link,
            "image": image
        })
    except Exception as e:
        continue

# Tutup browser
driver.quit()

# Simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("scraping/laptop/csv/acer.csv", index=False, encoding='utf-8-sig')
print("Selesai! Data disimpan")