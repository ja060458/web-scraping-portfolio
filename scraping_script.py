from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriverのオプション設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # ヘッドレスモード（ブラウザを表示しない）

# ChromeDriverを自動的にダウンロードして設定
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 任意のURLにアクセス
driver.get('https://www.library.chiyoda.tokyo.jp/facilities/')
driver.implicitly_wait(10)

# ページ全体が読み込まれるのを待機
time.sleep(5)

# 要素が見つかるまで待機（最大30秒）
try:
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'p-library__detail-schedule--body'))
    )

    # 開館か閉館かを判定
    status_text = element.find_element(By.CLASS_NAME, 'p-library__detail-schedule--status---text').text
    if '開館' in status_text:
        print("図書館は開館しています。")
    elif '閉館' in status_text:
        print("図書館は閉館しています。")
    else:
        print("開館状況が不明です。")

finally:
    driver.quit()


