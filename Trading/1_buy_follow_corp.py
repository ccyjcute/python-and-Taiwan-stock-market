import sys
# sys.path.append('D:\Trading')
#import剛剛的函數包as uf
import utility_f as uf
import datetime
import os
import pandas as pd
import traceback
try:
    #獲取今日日期
    today = datetime.date.today()
    #傳入判斷今天是否為營業日
    if_trade = uf.is_open(today)
    #如果是N，表示沒開盤，準備寄信
    if if_trade=='N':
        #沒開盤應該收件者
        mail_list = ['a********@gmail.com']
        #標題為三大法人篩選，今日休市
        subject = f'{today} 小幫手三大法人篩選 - 今日休市'
        #郵件內容為空
        body = ''
        #寄信
        uf.send_mail(mail_list, subject, body, 'text' ,None, None)
        exit()
    
    control = 0 # 用control來控制獲得了幾個有開市的資料(因為目的是希望連續三天買超，所以需要三個開市的日子)
    for i in range(0, 10):
        if control <=2:
            date_target = today + datetime.timedelta(days = -int(i)) # 向前推i天
            if_trade = uf.is_open(date_target) # 用我們的函數is_open判斷是否開盤
            # print(date_target)
            # print(if_trade)
            #未開盤的話則continue直接進行下一批檢查
            if if_trade=='N':
                continue
            #有開盤則control要記得+1，並且進行三大法人買賣超處理
            else:
                convert_today = date_target.strftime('%Y%m%d') # 將日期轉為字串以便傳入twse_data()函數
                print(convert_today)
                data = uf.twse_data(convert_today) # 獲取三大法人買賣超日報
                data.to_excel(f'{convert_today}_twse.xlsx')
                #讀取時使用thousands參數讀取，處理數字問題(如果有數字使用,作為千元標示，讀取時即可知道是用來表示數字的)
                data = pd.read_excel(f'{convert_today}_twse.xlsx', thousands=',')
                os.remove(f'{convert_today}_twse.xlsx')
                
                d_s = data[(data[u'三大法人買賣超股數']>0)] #只保留三大法人買賣超股數大於0的
                d_s = d_s[:50] # 獲取前50名三大法人買超最大量的(證交所網站已經事先由大到小進行sort了)

                # 當control ==0的時候意味著是第一次搜尋到清單，因此當主軸
                if control==0:
                    result = set(d_s[u'證券代號'].tolist())
                #如果不是的話我們用intersection函數來取交集
                else:
                    result = result.intersection(set(d_s[u'證券代號'].tolist())) # 這裡的set可以放多個
                
                control+=1
        else:
            break
    #收件名單
    mail_list = ['**@gmail.com']
    #將結果用逗號黏成字串，非必要，但是我不喜歡list的中括號，看起來蠻醜的
    result  = ",".join(result)
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手三大法人篩選'
    #內容就是剛剛篩選完成的股票
    body = f'目標股票 {result} 連續三日法人買超'
    #寄信
    uf.send_mail(mail_list, subject, body, 'text' ,None, None)
    # print("good")
except SystemExit:
    print('Its OK')
except:
    #收件名單
    mail_list = ['**@gmail.com']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手三大法人篩選異常'
    #內容就是剛剛篩選完成的股票
    body = traceback.format_exc()
    #寄信
    uf.send_mail(mail_list, subject, body, 'text' ,None, None)























