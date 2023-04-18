# main에서 전체 실행

#crontab 관련 : */5 * * * * /usr/bin/python3 /home/ubuntu/news7/main.py > /home/ubuntu/news7/log_file 2>&1

# 파일 가져오는 부분은 결과 확인용을 위해 사용. 실제작동할때는 없앨 예정. 함수만 담아놓을 예정. 
import pandas as pd

# tsv_to_csv.py 실행하여 온전한 csv파일 만들기
from itnews import tsv_to_csv
tsv_news = tsv_to_csv.get_df() 
tsv_news.to_csv('sample1.csv', index = False ) # csv파일로 저장
news = pd.read_csv('/home/ubuntu/news7/itnews/sample1.csv') # 여기까지는 cleansing 진행되지 않음. 


# nlp.py에 있는 함수들 가져와서 적용시키기 
# nlp.py에 있는 print구문들 (오류 확인용으로 남겨놨지만) 실제코드 작동할 때는 다 주석처리하거나 삭제해야함. 
import nlp
new_news = nlp.cleansing(news)
new_news = nlp.morecleansing(news)
new_news = nlp.preprocessing(new_news)
top6 = nlp.topicmodeling(new_news) # top6안에 id, title, content, img, keywords, summary 들어있다. => HTML 문서 작성할떄 활용할 것! 
print(top6.img[0])


# 이메일 발송 코드
import rpa
rpa.email_sending(top6)
