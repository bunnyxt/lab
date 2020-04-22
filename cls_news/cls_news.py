from bs4 import BeautifulSoup
from urllib.request import urlopen
import schedule
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

news_file_name = 'cls_news.txt'

def get_ts_s():
    return int(round(datetime.datetime.now().timestamp()))


def ts_s_to_str(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def init():
    print(ts_s_to_str(get_ts_s()))
    print('now go init...')
    html = urlopen('http://www.cls.edu.cn/Academicactivities/notices/index.shtml')
    soup = BeautifulSoup(html, features="lxml")
    div = soup.find('div', {"class": "r_con_w"})
    trs = div.findChildren('tr')
    with open(news_file_name, 'w') as f:    
        for tr in trs:
            tds = tr.findChildren('td')
            title = tds[0].findChildren('a')[0].string
            link = 'http://www.cls.edu.cn' + tds[0].findChildren('a')[0]['href']
            date = tds[1].string
            print(title, link, date)
            f.write('%s\t%s\t%s\n' % (title, link, date))
    print('init done!')


def check():
    print(ts_s_to_str(get_ts_s()))
    print('now go check...')
    html = urlopen('http://www.cls.edu.cn/Academicactivities/notices/index.shtml')
    soup = BeautifulSoup(html, features="lxml")
    div = soup.find('div', {"class": "r_con_w"})
    trs = div.findChildren('tr')
    news_list = []
    with open(news_file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_arr = line.rstrip('\n').split('\t')
            news_list.append(line_arr)
    
    news_list_new = []
    for tr in trs:
        tds = tr.findChildren('td')
        title = tds[0].findChildren('a')[0].string
        link = 'http://www.cls.edu.cn' + tds[0].findChildren('a')[0]['href']
        date = tds[1].string
        if title == news_list[0][0] and link == news_list[0][1] and date == news_list[0][2]:
            # got same, break
            break
        print(title, link, date)
        news_list_new.append([title, link, date])
    
    with open(news_file_name, 'w') as f:
        for news in news_list_new:
            title = news[0]
            link = news[1]
            date = news[2]
            f.write('%s\t%s\t%s\n' % (title, link, date))
            send_mail(title, link, date)
        for line in lines:
            f.write(line)
    
    print('check done!')


def send_mail(title, link, date):
    # 第三方 SMTP 服务
    mail_host="<your-sender-email-smtp-server>"  #设置服务器
    mail_user="<your-sender-email>"    #用户名
    mail_pass="<your-sender-password>"   #口令 
    
    sender = '<your-sender-email>'
    receivers = ['<your-receiver-email-1>', '<your-receiver-email-1>']
    
    message = MIMEText('叮叮叮~监测到CLS通知公告网页有新的新闻哦，请留意~\n' + \
        '- 新闻标题: %s \n' % title + \
        '- 新闻连接: %s \n' % link + \
        '- 发布日期: %s \n' % date + \
        '更多通知公告：http://www.cls.edu.cn/Academicactivities/notices/index.shtml', 'plain', 'utf-8')
    message['From'] = formataddr(['<your-sender-name>', '<your-sender-email>'])
    message['To'] = formataddr(['<your-receiver-name>', '<your-receiver-email>'])
    message['Subject'] = Header('CLS新闻更新', 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # smtp port 465
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('email semd success')
    except smtplib.SMTPException as e:
        print('fail to send email, %r' % e)


if __name__ == "__main__":
    init()
    check()
    schedule.every(1).minutes.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)