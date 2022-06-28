import pandas as pd
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

url = 'https://finance.naver.com/item/sise_day.nhn?code=035720&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')

s = str(pgrr.a['href']).split('=')
last_page = s[-1]

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=035720'

for page in range(1, int(last_page) + 1):
    url = '{}&page={}'.format(sise_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(html, header=0)[0])

df = df.dropna()
