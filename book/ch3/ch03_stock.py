# 삼성전자와 MS의 일별 주가 데이터를 받아와 수익률 비교
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

sec = pdr.get_data_yahoo('005930.KS', start='2021-06-22')
msft = pdr.get_data_yahoo('MSFT', start='2021-06-22')

import matplotlib.pyplot as plt
'''
plt.plot(sec.index, sec.Close, 'b', label='Samsung Electronics')
plt.plot(msft.index, msft.Close, 'r--', label='Microsoft')
plt.legend(loc='best')
plt.show()
'''
# 위와 같이 그냥 비교할 시 환율을 고려하지 않고 수치만 반영된 꼴이라
# 일간 변동률을 가지고 비교해준다.

# 주가 일간 변동률 히스토그램
sec_dpc = (sec['Close']/sec['Close'].shift(1) - 1) * 100
sec_dpc.iloc[0] = 0
'''
plt.hist(sec_dpc, bins=18, label='Samsung daily percent change')
plt.legend()
plt.grid(True)
plt.show()
'''

# 일간 변동률 누적곱
sec_dpc_cp = ((100+sec_dpc)/100).cumprod()*100 - 100

msft_dpc = (msft['Close']/msft['Close'].shift(1) - 1)*100
msft_dpc_cp = ((100+msft_dpc)/100).cumprod()*100 - 100

plt.plot(sec.index, sec_dpc_cp, 'b', label='Samsung Electronics')
plt.plot(msft.index, msft_dpc_cp, 'r--', label='Microsoft')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()
