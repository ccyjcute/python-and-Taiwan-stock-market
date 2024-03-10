import ta
import yfinance as yf
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt

stock  = yf.Ticker('2330.TW')
df = stock.history(start = '2023-01-01')

fig = plt.figure(figsize = (24, 8))
ax = fig.add_subplot(1, 1, 1) # 詳細看3-31
ax.set_xticks(range(0, len(df.index), 30))

temp = df.index.date # 將小時分鐘秒去掉
ax.set_xticklabels(temp[::30], rotation=90, fontsize=6)

mpf.candlestick2_ochl(ax, df['Open'], df['Close'], df['High'], df['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)

plt.title(f'2330 Stock Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.savefig('test.png')   
plt.show()