import datetime
import glob
import json
import os
import re
import requests

from bs4 import BeautifulSoup

SOURCE_PAGE_URL = 'https://corona.go.jp/emergency/'


class Covid19Data:
    def run(self):
        return self.parse_html()

    def fetch_html_soup(self):
        html = requests.get(SOURCE_PAGE_URL)
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup

    def parse_html(self):
        soup = self.fetch_html_soup()
        contents = soup.find_all(class_='emergency-kv_table02')
        return self.parse_emergency(contents), self.is_manbou(contents)

    def parse_emergency(self, contents):
        for content in contents:
            text = content.find(class_='detail-item').find(class_='detail-item_hd').text
            result = re.match('緊急事態宣言', text)
            if result:
                return self.parse_main_content(content)
        return []

    def is_manbou(self, contents):
        for content in contents:
            text = content.find(class_='detail-item').find(class_='detail-item_hd').text
            result = re.match('まん延防止', text)
            if result:
                return self.parse_main_content(content)
        return []

    def parse_main_content(self, contents):
        results = []
        contents = contents.find_all(class_='emergency-kv_detail02')
        for content in contents:
            period = content.find(class_='detail-item period').find(class_='detail-item_txt').text
            prefectures = content.find(class_='detail-item area').find(class_='detail-item_txt').text.split('、')
            for prefecture in prefectures:
                results.append(self.prefecture_data(period, prefecture))
        return results

    def prefecture_data(self, period, prefecture):
        pettern1 = re.compile(r'(\d+)月(\d+)日から')
        pettern2 = re.compile(r'(\d+)月(\d+)日まで')
        from_ = pettern1.search(period)
        to_ = pettern2.search(period)
        return {
            'name': prefecture,
            'from': str(from_.group(1)) + '月' + str(from_.group(2)) + '日' if from_ else '',
            'to': str(to_.group(1)) + '月' + str(to_.group(2)) + '日' if to_ else '',
        }


class Generator:
    emergency_data = []
    manbou_data = []

    def __init__(self, emergency_data, manbou_data):
        self.emergency_data = emergency_data
        self.manbou_data = manbou_data

    def json_export(self):
        with open('data/emergency.json', 'w', encoding='utf-8') as f:
            json.dump({
                'emergency': self.emergency_data,
                'manbou': self.manbou_data,
                'updatedAt': str(datetime.datetime.now())
            }, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print('---fetch data---')
    covid_data = Covid19Data()
    emergency_data, manbou_data = covid_data.run()
    print('---export jsons---')
    generator = Generator(emergency_data, manbou_data)
    generator.json_export()
    print('---done---')
