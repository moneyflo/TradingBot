import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=035720&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
s = str(pgrr.a['href']).split('=')
last_page = s[-1]

# 전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=035720'
for page in range(1, int(last_page) + 1):
    url = '{}&page={}'.format(sise_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(html, header=0)[0])

# 차트 출력을 위한 가공
df = df.dropna()
df = df.iloc[0:30]   # 30일간의 데이터
df = df.sort_values(by='날짜')

# 날짜 종가 칼럼으로 차트 그리기
plt.title('Kakao (close)')
plt.xticks(rotation=45)
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
