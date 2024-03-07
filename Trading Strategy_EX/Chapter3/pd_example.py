import pandas as pd
import yfinance as yf
#yfinance產出台積電股價資料
stock = yf.Ticker('2330.TW')
#獲取20170101-20210202
df = stock.history(start="2017-01-01", end="2021-02-02")
#rolling以6為單位位移並取最大值
df['Highest_high'] =df['High'].rolling(6).max()
# #rolling以6為單位位移並取最小值
df['Lowest_low'] = df['Low'].rolling(6).min()

#一樣用6根作為rolling，並且設計計算函數第一個值減去最後一個值
O_C_high = df['High'].rolling(6).apply(lambda x : x[0]-x[-1])
#加入dataframe
df['OCHIGH'] = O_C_high

df.index = df.index.tz_localize(None) # 因為索引是timezone，所以需要改成無時區的時間
df.to_excel('./final.xlsx')

# df['Highest_high'] = Highest_high
# df['Lowest_Low'] = Lowest_low
# df['OCHIGH'] = O_C_high
# print(df)
