"""
 rpa.py는 자동화 담당으로 이메일 전송을 담당하고 있습니다. 
"""

import smtplib
import email
from datetime import datetime
# 프로젝트를 위한 네이버 이메일 계정 =>  id : rpanews7 , pw : autonews7! 


def email_sending(top6):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #기본 세팅
    SMTP_SERVER= 'smtp.naver.com'
    SMTP_PORT = 465
    SMTP_USER = 'rpanews7@naver.com'
    SMTP_PASSWORD =open('/home/ubuntu/news7/config','r').read().strip()
    
   
    to_users = ['rpanews7@naver.com'] # 수신자 리스트
    target_addr = ','.join(to_users)
    now = datetime.now().strftime('%Y-%m-%d')
    subject= f'🗞️[{now} IT 간추린 뉴스] 오늘의 주요 IT 뉴스를 확인해보세요🗞️'
       
    contents = open('/home/ubuntu/news7/stripo.html','r').read()

    
    #SMTP 메일 발송하기
    msg = MIMEMultipart('alternative') # alternative , mixed
    msg['From']= SMTP_USER
    msg['To']= target_addr
    msg['Subject']= subject

    # 날짜 오늘날짜로 바꿔서 넣기!   
    today_date = datetime.today().strftime('%B %d , %Y')
    contents = contents.replace("April",today_date) 

    # HTML 문서 내용 집어 넣기! 
    top6['id']=top6['id'].astype('str')
    ID_PATH = 'https://v.daum.net/v/'

    for i in range(len(top6)): 
        #title
        a_title = "a_title"+str(i+1)
        contents = contents.replace(a_title, top6.title[i])
        #summary
        a_s = 's_'+str(i+1)
        contents = contents.replace(a_s, ' '.join(top6.summary[i]))
        #keywords
        a_k ='k_'+str(i+1)
        contents = contents.replace(a_k, '#'+' #'.join(top6.keywords[i]))
        #link
        a_l ='l_'+str(i+1)
        contents=contents.replace(a_l, ID_PATH+top6.id[i])
        #img
        a_i = 'i_'+str(i+1)
        contents= contents.replace(a_i, top6.img[i])

    text = MIMEText(contents,'html','utf-8') 
    msg.attach(text)

    # 메시지 발송하기
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, set(to_users), msg.as_string())
    smtp.close()

if __name__ == '__main__':
    email_sending()