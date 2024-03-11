import pandas as pd
import datetime

def is_open(target_date:datetime.date):
    hd = pd.read_excel("./holiday.xlsx")
    hd_date = list(map(lambda x: x.strftime('%Y%m%d'), pd.to_datetime(hd['日期'])))
    # print(type(hd_date[0]))
    
    str_date = target_date.strftime('%Y%m%d') # 將日期進行格式化
    # print(type(str_date))

    day = target_date.weekday()
    if day == 5 or day==6: return 'N' # 判定是不是星期六或日，如果是的話就print N出來       
    if str_date in hd_date: return 'N'
    return 'Y'
# print(is_open(datetime.date(2024, 1, 3)))

