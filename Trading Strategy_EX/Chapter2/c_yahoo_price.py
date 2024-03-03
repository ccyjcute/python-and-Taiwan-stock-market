import requests
from bs4 import BeautifulSoup

def stock_price(stock:str): # 定義函數名stock_price，並且需要傳入字串類型的股票代號
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
        }
    data = requests.get(f"https://finance.yahoo.com/quote/{stock}?p={stock}",headers=headers)
    soup = BeautifulSoup(data.text, features="lxml")
    price = soup.find("fin-streamer", {"data-test": "qsp-price"}) # find尋找元素
    return price.text
print(stock_price("2330.TW"))
