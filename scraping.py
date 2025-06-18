from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=opsi)

shopee_link = "https://torch.id/search?sort_by=relevance&q=tas+ransel&options%5Bprefix%5D=last&filter.p.product_type=Backpack&filter.v.price.gte=&filter.v.price.lte="
driver.set_window_size(1300,800)
driver.get(shopee_link)
time.sleep(5)

driver.save_screenshot("home.png")
driver.quit()