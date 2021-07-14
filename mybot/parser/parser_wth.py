import requests

from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/79.0.3945.117 Safari/537.36"
}


result = requests.get('https://kakoysegodnyaprazdnik.ru/', headers=headers)
result.encoding = 'UTF-8'
res = result.text
soup = BeautifulSoup(res, 'html.parser')
holiday = []


def list_holiday():
    for block in soup.find_all('span', itemprop="text"):
        holiday.append(block.text)
    return holiday
