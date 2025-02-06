import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# Selenium設定
driver_path = 'path/to/your/chromedriver'  # ChromeDriverのパスを指定
driver = webdriver.Chrome(driver_path)

# デバッグ用の出力
print("Driver initialized")

# 検索ワード
search_keyword = "sample search keyword"  # ここに検索ワードを入力
print(f"Search keyword: {search_keyword}")

# 指定のURLにアクセス
url = "URL of the search page"
driver.get(url)
print(f"Accessed URL: {url}")

# 検索ボックスに検索ワードを入力
search_box = driver.find_element(By.ID, "common-header-search-input")
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)
print("Search initiated")

# 検索結果が表示されるまで待機
time.sleep(5)
print("Search results page loaded")

# BeautifulSoupでページの内容を解析
soup = BeautifulSoup(driver.page_source, 'html.parser')
print("Page parsed")

# 商品のURLを取得
product_links = []
for link in soup.find_all('a', href=True):
    product_links.append(link['href'])
print(f"Product links found: {len(product_links)}")

# URLをCSVに保存
with open('product_urls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL"])
    for link in product_links:
        writer.writerow([link])
print("Product URLs saved to CSV")

# 各商品のURLにアクセスして、価格、ポイント数、在庫状況を取得
product_data = []
for link in product_links:
    driver.get(link)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    price = soup.find('span', {'class': 'price-class-name'}).text
    points = soup.find('span', {'class': 'points-class-name'}).text
    stock = soup.find('span', {'class': 'stock-class-name'}).text
    product_data.append({"URL": link, "Price": price, "Points": points, "Stock": stock})
print("Product data extracted")

# 取得したデータをCSVに保存
df = pd.DataFrame(product_data)
df.to_csv('product_data.csv', index=False)
print("Product data saved to CSV")

# ドライバーを終了
driver.quit()
print("Driver closed")
