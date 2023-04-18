"""
 rpa.py는 자동화 담당으로 이메일 전송을 담당하고 있습니다. 
"""

import smtplib
import email
from datetime import datetime
# 프로젝트를 위한 네이버 이메일 계정 =>  id : rpanews7 , pw : autonews7! 


def email_sending(top6):
    #기본 세팅
    SMTP_SERVER= 'smtp.naver.com'
    SMTP_PORT = 465
    SMTP_USER = 'rpanews7@naver.com'
    SMTP_PASSWORD =open('/home/ubuntu/news7/config','r').read().strip()
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
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

    # 날짜 오늘날짜로 바꿔서 넣기!   a_title1, s_1, k_1, l_1
    today_date = datetime.today().strftime('%B %d , %Y')
    contents = contents.replace("April",today_date) 
    # title 넣기
    contents = contents.replace('a_title1',top6.title[0]).replace('a_title2',top6.title[1]).replace('a_title3',top6.title[2]).replace('a_title4',top6.title[3]).replace('a_title5',top6.title[4]).replace('a_title6',top6.title[5])
    # 세줄요약 넣기
    contents = contents.replace('s_1',' '.join(top6.summary[0])).replace('s_2',' '.join(top6.summary[1])).replace('s_3',' '.join(top6.summary[2])).replace('s_4',' '.join(top6.summary[3])).replace('s_5',' '.join(top6.summary[4])).replace('s_6',' '.join(top6.summary[5]))
    # 키워드 해시태그 형태로 넣기
    contents = contents.replace('k_1','#'+' #'.join(top6.keywords[0])).replace('k_2','#'+' #'.join(top6.keywords[1])).replace('k_3','#'+' #'.join(top6.keywords[2])).replace('k_4','#'+' #'.join(top6.keywords[3])).replace('k_5','#'+' #'.join(top6.keywords[4])).replace('k_6','#'+' #'.join(top6.keywords[5]))
    # 이미지 링크 연결
    top6['id']=top6['id'].astype('str')
    ID_PATH = 'https://v.daum.net/v/'
    contents = contents.replace('l_1',ID_PATH+top6.id[0]).replace('l_2',ID_PATH+top6.id[1]).replace('l_3',ID_PATH+top6.id[2]).replace('l_4',ID_PATH+top6.id[3]).replace('l_5',ID_PATH+top6.id[4]).replace('l_6',ID_PATH+top6.id[5])
    
    # 기사 이미지 넣기 : 기사이미지가 없는 경우도 있잖아! 
    contents = contents.replace('i_1',top6.img[0]).replace('i_2',top6.img[1]).replace('i_3',top6.img[2]).replace('i_4',top6.img[3]).replace('i_5',top6.img[4]).replace('i_6',top6.img[5])
    
    text = MIMEText(contents,'html','utf-8') 
    #text = MIMEText(contents) 
    msg.attach(text)

    # 메시지 발송하기
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, set(to_users), msg.as_string())
    smtp.close()

if __name__ == '__main__':
    email_sending()