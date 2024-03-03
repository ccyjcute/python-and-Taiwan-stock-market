import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
設計上是先在新聞列表中取得每一篇新聞的連結，再去每一篇新聞獲取標題以及日期資訊
其實新聞列表就已經具有標題以及連結這些元素，但問題是他的時間是例如1小時前、50分鐘前、三天前
這並不是我們想要的格式，所以我們還需要一個步驟，獲取每個詳細新聞網址去裡頭獲取詳細的年月日時間(例如2021/9/27)
當然如果你不介意例如1小時前這樣的時間，那爬蟲速度應該至少可以快50%以上
因為就不需要每一篇新聞都還要為了時間資訊去request獲取資訊
看個人取捨設計了，我先寫比較繁複的，這樣讀者要改成簡單的也比較容易
"""


def get_yahoo_news2(stock: str):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }
    data = requests.get(
        f"https://tw.stock.yahoo.com/quote/{stock}/news", headers=headers
    )
    soup = BeautifulSoup(data.text, "html.parser")
    all_news = soup.find_all("h3", {"class": "Mt(0) Mb(8px)"})

    all_news_link = []
    for a in all_news:
        news_path = a.find("a")["href"]
        if news_path[-4:] == "html": # 雅虎新聞目前的設計是中間會夾雜一兩篇廣告，這些廣告的特點是他們的連結最後沒有html的文字，因此可以用這個方法剔除他們
            all_news_link.append(news_path)

    date_store, title_store = [], [] # 開始進行獲取日期，標題我也在這裡做，當然如果你要再上一個步驟就獲取標題也可以
    for new in all_news_link: # loop剛剛獲得的每一篇新聞網址
        each_data = requests.get(f"{new}", headers=headers)
        each_soup = BeautifulSoup(each_data.text, "html.parser")

        title = each_soup.find("h1", {"data-test-locator": "headline"}).text # find獲取title
        news_time = each_soup.find("div", {"class": "caas-attr-time-style"}).text # find獲取時間
        # 整理時間格式，只想要前面的年月日資訊，中間有空白剛好可以利用split切割空白，取第一個元素
        news_time = news_time.split(" ")[0]
        # 這裡看個人要不要做，我不喜歡例如2021年9月27日這樣的格式，因此我用replace轉換成2021/9/27
        news_time = news_time.replace("年", "/")
        news_time = news_time.replace("月", "/")
        news_time = news_time.replace("日", "")
        # append整理資料
        title_store.append(title)
        date_store.append(news_time)
    # 整理成DataFrame
    result = pd.DataFrame()
    result["title"] = title_store
    result["url"] = all_news_link
    result["date"] = date_store
    return result
print(get_yahoo_news2("2330"))
