#import需要的套件
import yfinance as yf
import pandas as pd
import numpy as np
import time
import datetime
import traceback
import utility_f as uf
try:
    
    stock_list = pd.read_excel('./stock_list.xlsx') # 讀取台股列表
    all_stock = stock_list['代號'].values # 獲取所有的股票代號(.value是將pandas轉成numpy)
    print(all_stock)
    
    dividend_store = [] # 儲存每支股票的殖利率
    stock_store = []
    count = 0 # 計數用
    #迴圈loop每一支股票
    for i in all_stock:
        start = time.time() # 計算每一筆處理的時間，在開頭記錄一個start時間點
        count+=1 # 計數用參數
 
        stock = yf.Ticker(f'{i}.TW') # info的殖利率是從第一季的配息預估整年的配息
        try:
            d_y = stock.info['dividendYield']
            if d_y !=None and d_y>=0.05: # 殖利率大於5%
                    stock_store.append(i)
                    dividend_store.append(d_y)
            else:
                d_y=None
            
            end = time.time() # 記錄每一筆結束時間
            
            print(f'Dealing: {count} | All: {len(all_stock)} | Stock: {i} | DY: {d_y} | Cost Time: {end-start}s')
        except:
            print(f'Error Stock ! Dealing: {count} | All: {len(all_stock)} | Stock: {i}')
    data = pd.DataFrame()
    data['代號'] = stock_store
    data['殖利率'] = dividend_store
    data.to_excel('dividend_list.xlsx')
except SystemExit:
    print('Its OK')
except:
    today = datetime.date.today()
    #收件名單
    mail_list = ['a*****@gmail.com','0*****@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手高配息名單篩選異常'
    #內容就是剛剛篩選完成的股票
    body = traceback.format_exc()
    #寄信
    uf.send_mail(mail_list, subject, body,'text', None, None)
    
	
