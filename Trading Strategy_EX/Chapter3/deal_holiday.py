# 將放假日變成正確的日期格式
import pandas as pd
import datetime

today = datetime.date.today() # today獲取今天的日期
convert_today = today.strftime('%Y') # 透過strftime只留下年
# print(convert_today)

x = pd.read_csv(f"./holidaySchedule_{int(convert_today) - 1911}.csv",encoding='big5',skiprows=[0]) #如果單純填一個數字的話，會跳過數字+1個row。另外big5是專門編碼中文的
# print(x)
# print(x.columns)
x = x[x['備註(* : 市場無交易，僅辦理結算交割作業。o : 交易日。)'] != 'o']
x['日期'] = x['日期'].apply(lambda x:convert_today+'-'+x) # 針對日期apply，將year加上原先的日期

# 一樣對日期做apply，並且replace年月為-，日為空白
x['日期'] = x['日期'].apply(lambda x:x.replace('月','-'))
x['日期'] = x['日期'].apply(lambda x:x.replace('日',''))

x['日期'] = x['日期'].apply(lambda x:x.split()[0]) # 將星期去掉
print(x['日期'])

x['日期'].to_excel('./holiday.xlsx',columns=['日期'])