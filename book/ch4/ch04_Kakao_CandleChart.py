import pandas as pd
import requests
from bs4 import BeautifulSoup
import mplfinance as mpf
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
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low',
                            '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

mpf.plot(df, title='Kakao candle chart', type='candle')

# mpf.plot(df, title='Kakao ohlc chart', type='ohlc')

# kwargs = dict(title='Kakao customized chart', type='candle', mav=(2,4,6), volume=True, ylabel='ohlc candles')
# mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
# s = mpf.make_mpf_style(marketcolors=mc)
# mpf.plot(df, **kwargs, style=s)
