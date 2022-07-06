# 시총 상위권 4 종목으로 효율적 투자선 구하기
import sys
sys.path.append('C:/myPackage')
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer

# 국내 첫 코로나 환자 발생일부터의 주가 데이터 사용
mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2020-01-20')['close']

daily_ret = df.pct_change()          # 일간 변동률
annual_ret = daily_ret.mean() * 252  # 연간 변동률
daily_cov = daily_ret.cov()          # 일간 변동률의 공분산
annual_cov = daily_cov * 252         # 연간 변동률의 공분산

port_ret = []
port_risk = []
port_weights = []

# Monte Carlo simulation
for _ in range(20000):  # 랜덤한 20000개의 포트폴리오 생성
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weights[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk'] + [s for s in stocks]]

df.plot.scatter(x='Risk', y='Returns', figsize=(10, 7), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
