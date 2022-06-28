import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from scipy import stats
import matplotlib.pyplot as plt

dow = pdr.get_data_yahoo('^DJI', '2002-07-30')
tlt = pdr.get_data_yahoo('TLT', '2002-07-30')

df = pd.DataFrame({'X':dow['Close'], 'Y':tlt['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'

plt.figure(figsize=(7, 7))
plt.plot(df.X, df.Y, 'gx')
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend(['DOW x TLT', regr_line])
plt.title(f'DOW x TLT (R = {regr.rvalue:.2f})')
plt.xlabel('DOW')
plt.ylabel('TLT')
plt.show()
