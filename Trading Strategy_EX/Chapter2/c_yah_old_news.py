import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_yahoo_news(stock:str,target_page:int): # 指定股票以及新聞頁數
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
    }
    #===========================獲取頁數===========================
    data = requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}",headers=headers)
    soup = BeautifulSoup(data.text)
    page = soup.find('span',{'class':'mtext'}) # find我們找到的共幾頁元素

    digit = filter(str.isdigit, page.text)
    all_page = int(''.join(list(digit)))

    if target_page<all_page: # 如果目標頁數比x小，那我們的拿來帶入頁數的x就可以直接替換成目標頁數
        all_page = target_page
#===========================取得資料===========================
    title,url,date_store = [],[],[] # 準備儲存變數的list
    result = pd.DataFrame() # 準備儲存所有資料的空dataframe

    for i in range(1, all_page+1):
        time.sleep(1)
        data = requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}&pg={str(i)}",headers=headers)
        soup = BeautifulSoup(data.text)

        article = soup.find_all('td',{'height':'37'})
        date_data = soup.find_all('td',{'height':'29'}) 
        for x,y in zip(article, date_data): # zip方法可以把多個list拿來一起loop
            title.append(x.text)
            url.append('https://tw.stock.yahoo.com'+x.find('a')['href'])
            date_store.append((y.text.split()[0])[1:])

    result['title'] = title
    result['url'] = url
    result['date'] = date_store
    
    return result

