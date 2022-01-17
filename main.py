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
        # test version
        # html = open('test/temp.html', 'r', encoding='utf-8').read()
        # soup = BeautifulSoup(html, 'html.parser')

        # production version
        html = requests.get(SOURCE_PAGE_URL)
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup

    def parse_html(self):
        soup = self.fetch_html_soup()
        contents = soup.find_all(class_='emergency-kv_table02')
        emergency_result = []
        manbou_result = []
        for content in contents:
            h2 = content.previous_sibling.previous_sibling
            result = re.match('緊急事態宣言', h2.text)
            if result:
                emergency_result.append(self.parse_emergency([content]))
            result = re.match('まん延防止', h2.text)
            if result:
                manbou_result.append(self.parse_manbou([content]))
        return emergency_result, manbou_result

    def parse_emergency(self, contents):
        for content in contents:
            return self.parse_main_content(content)
        return []

    def parse_manbou(self, contents):
        for content in contents:
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
        pettern1 = re.compile(r'令和(\d+)年(\d+)月(\d+)日から')
        pettern2 = re.compile(r'令和(\d+)年(\d+)月(\d+)日まで')
        from_ = pettern1.search(period)
        to_ = pettern2.search(period)
        return {
            'name': prefecture,
            'from': str(self.reiwa_to_seireki(from_.group(1))) + '-' + str(from_.group(2)).zfill(2) + '-' + str(from_.group(3)).zfill(2) if from_ else '',
            'to': str(self.reiwa_to_seireki(to_.group(1))) + '-' + str(to_.group(2)).zfill(2) + '-' + str(to_.group(3)).zfill(2) if to_ else '',
        }

    def reiwa_to_seireki(self, reiwa):
        return int(reiwa) - 3 + 2021


class Generator:
    emergency_data = []
    manbou_data = []

    def __init__(self, emergency_data, manbou_data):
        self.emergency_data = emergency_data
        self.manbou_data = manbou_data

    def json_export(self):
        with open('data/all.json', 'w', encoding='utf-8') as f:
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
