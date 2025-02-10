import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_company_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    company_name = soup.find('h1', class_='company-name').text.strip()
    phone_number = soup.find('span', class_='phone-number').text.strip()
    address = soup.find('div', class_='address').text.strip()
    industry = soup.find('span', class_='industry').text.strip()
    website = url
    
    return {
        '会社名': company_name,
        '電話番号': phone_number,
        '住所': address,
        '業種': industry,
        'URL': website
    }

# スクレイピングする企業のURLリスト
urls = [
    'https://example.com/company1',
    'https://example.com/company2',
    'https://example.com/company3'
]

# 各企業の情報を抽出
companies_data = []
for url in urls:
    company_info = scrape_company_info(url)
    companies_data.append(company_info)

# データフレームを作成
df = pd.DataFrame(companies_data)

# Excelファイルに保存
output_path = r"C:\Users\ja060\Downloads\python2\.vscode\company_info.xlsx"
df.to_excel(output_path, index=False)

print(f'企業情報を{output_path}に保存しました。')
