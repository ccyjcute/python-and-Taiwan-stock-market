import pandas as pd
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
    }
html_data = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",headers=headers)


x = pd.read_html(html_data.text) # 使用pandas的read_html處理表格
x = x[0] # list取出list裡面的第一個元素，就是我們的Dataframe

x.columns  = x.iloc[0,:]
x = x.iloc[1:,:] # 因為已經指定columns了，所以原本的row可以刪除

x['代號'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[0]) # 使用split方法，以兩個空白切割字串，並取切割完後第一個，儲存至新增的代號欄位(詳見2-25)
x['股票名稱'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[-1])

x['上市日'] = pd.to_datetime(x['上市日'], errors='coerce') # 將無法轉成datetime的資料化為Nan
x = x.dropna(subset=['上市日']) # 把上市日的Nan去掉即可

x = x.drop(['有價證券代號及名稱', '國際證券辨識號碼(ISIN Code)', 'CFICode','備註'], axis=1) # Drop掉不要的欄位

x = x[['代號','股票名稱', '上市日', '市場別', '產業別']] # 更換剩餘的欄位順序
x = x.dropna(subset=['產業別']) # Drop掉產業別是空的row
x = x[x["代號"].str.isdigit()] # pandas的str.isdigit()函數，確認是不是為數字(省略==true)

print(x)
x.to_excel('stock_list.xlsx', index=False)
