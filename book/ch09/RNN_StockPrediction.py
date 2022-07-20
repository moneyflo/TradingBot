# RNN_StockPrediction
import sys, os
sys.path.append('C:/myPackage')
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt
from Investar import Analyzer

# 데이터셋 준비
mk = Analyzer.MarketDB()
raw_df = mk.get_daily_price('삼성전자', '2020-06-23', '2022-6-30')

def MinMaxScaler(data):
    """ 최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator + 1e-7)

dfx = raw_df[['open','high','low','volume','close']]
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']]

x = dfx.values.tolist()
y = dfy.values.tolist()

# 이전 10일 동안 OHLVC 데이터를 이용하여 다음 날 종가를 예측하도록 준비
data_x = []
data_y = []
window_size = 10
for i in range(len(y) - window_size):
    _x = x[i : i + window_size]  # 다음 날 종가(i+window_size)는 포함되지 않음
    _y = y[i + window_size]      # 다음 날 종가
    data_x.append(_x)
    data_y.append(_y)
# print(_x, "->", _y)


# train test split
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[:train_size])
train_y = np.array(data_y[:train_size])

test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size:])
test_y = np.array(data_y[train_size:])


# 모델 생성
model = Sequential()
model.add(LSTM(units=10, activation='relu', return_sequences=True,
               input_shape=(window_size, 5)))
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_x, train_y, epochs=60, batch_size=30)
pred_y = model.predict(test_x)


# 예측치와 실제 종가 비교
plt.figure()
plt.plot(test_y, color='red', label='real SEC stock price')
plt.plot(pred_y, color='blue', label='predicted SEC stock price')
plt.title('SEC stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()


# 내일의 종가
print("SEC tomorrow's price :", raw_df.close[-1]*pred_y[-1]/dfy.close[-1])


