#先將可能會用到的套件import起來
import ta
import yfinance as yf
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt

stock = yf.Ticker('2330.TW')
df = stock.history(start="2017-01-01",end="2021-02-02")

#呼叫布林通道
indicator_bb = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
#布林中線
df['bbm'] = indicator_bb.bollinger_mavg()
#布林上線
df['bbh'] = indicator_bb.bollinger_hband()
#布林下線
df['bbl'] = indicator_bb.bollinger_lband()

fig = plt.figure(figsize=(24, 8)) # 創建畫布視窗，其中figsize代表你要的畫布大小，你也可以不設，不設就基礎的小小一張

grid = plt.GridSpec(3,20) # 定義出模板大小，3*20

ax = fig.add_subplot(grid[0:2,1:]) # 區塊一畫主圖，所以我們給他兩個空間，另外會切20格並且留一格在左邊是為了讓左標題更加明顯(如果切太大很奇怪)
ax2 = fig.add_subplot(grid[2:,1:]) # 詳見3-46

#使用mpl_finance的candlestick2_ochl函數，傳入剛剛的畫布加上OCHL值
mpf.candlestick2_ochl(ax, df['Open'], df['Close'], df['High'],
      df['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
#使用mpl.volume_overlay畫出成交量
mpf.volume_overlay(ax2, df['Open'], df['Close'], df['Volume'], colorup='r', colordown='g')

#將以30為間隔的df以apply+小函數lambda轉換日期
convert_date = pd.DataFrame(df.index[::30])['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

ax.set_xticks(range(0,len(df.index),30))# 設置你要的刻度
ax.set_xticklabels(convert_date ,rotation=90,fontsize=6) # 設置這幾個刻度的值

#在ax區塊上畫上布林上中下線
ax.plot(df['bbm'].values,  color='b', label = 'bbm', linestyle="--")
ax.plot(df['bbh'].values,  color='g', label = 'bbh', linestyle="--")
ax.plot(df['bbl'].values,  color='r', label = 'bbl', linestyle="--")

ax2.set_xticks(range(0,len(df.index),30)) # 設置你要的刻度
ax2.set_xticklabels(convert_date ,rotation=90,fontsize=6) # 設置這幾個刻度的值

ax.set_title(f'2330 Stock Price')
ax.set_xlabel('Date')
ax.set_ylabel("Price")

fig.tight_layout() # 自動微調位置以防重疊文字
ax.legend() # 設置legend才會有label跑出來

plt.savefig('test2.png')   
plt.show()

# 可以參考matplotlib gallery參考圖面
