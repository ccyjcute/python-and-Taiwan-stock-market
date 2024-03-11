# import sys
# sys.path.append('D:\Trading Strategy_EX\Chapter3') # vscode所需
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#從AES_Encrytion資料夾中import encrype_process.py裡面的所有函數*
from AES_Encryption.encrype_process import *
#節錄原先的寄信函數
def send_mail(mail_list:list, subject:str, body:str, mode :str , file_path:list, file_name:list):

    # 決定金鑰跟config檔位置
    key_path = '/mnt/d/key/'
    config_path = '/mnt/d/config/' 
    # 引用加解密的主要程式check_encrype
    user_id, password = check_encrype('gmail', key_path, config_path)
    

    #創建一個MIMEMultipart()類
    msg = MIMEMultipart()
    
    #對它傳入三個基本信息: 寄件者(From)、收件者(To)、標題(Subject)
    msg['From'] = user_id
    msg['To'] = ",".join(mail_list) # 使用join將list中的元素以逗號黏起來
    msg['Subject'] = subject

    #呼叫Attach，並傳入content信件內容
    if mode =='html': # 如果想要傳表格的話可以使用html
        msg.attach(MIMEText(body, mode))
    else:
        msg.attach(MIMEText(body))

    if file_path!=None:
        assert len(file_path) == len(file_name)
        for x in range(len(file_path)):
            #先透過內建的with open讀取檔案
            with open(file_path[x], 'rb') as opened: # 使用rb可以讀取需要專門軟體的byte檔(像是word, pdf)
                openedfile = opened.read()
        
            attachedfile = MIMEApplication(openedfile) # 呼叫MIMEApplication並放入byte類型
            attachedfile.add_header('content-disposition', 'attachment', filename = file_name[x]) # 根據指示加入至附檔，並可以指定與原本檔名不一樣的獨立檔名
            msg.attach(attachedfile) # 跟上面attach信件內容一樣，我們把附檔資訊也attach進去

    server = smtplib.SMTP('smtp.gmail.com', 587) # 設定smtp server，以gmail當例子
    server.starttls() # TLS安全傳輸設定
    server.login(user_id, password) # 登入你的gmail帳密

    # print(msg)
    # exit()

    text = msg.as_string() # msg是Mimemulipart類，我們將他轉為sendmail函數接受的字串
    server.sendmail(user_id, mail_list , text) # 指定寄件者跟收件者，還有剛剛加的信件內容、標題、附檔等等資訊(text)
    server.quit()

#測試加入了加解密套件的程式

mail_list = [''] # 定義收件者
subject = '測試測試' # 標題
body = '借我測試' # 內容
mode = 'text'

file_path = [r"./test.png",r"./test2.png"] # 副檔的位置
file_name = ["借我測.png","借我測2.png"] # 希望傳送的檔名
send_mail(mail_list, subject, body, mode, file_path, file_name) # 如果有那裡不需要就None
