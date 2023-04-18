# 📬AutoNewsFeeding_7📬
Daum 뉴스 크롤링 7조   
https://www.notion.so/7-7b61e47096184f6c8c1cb718d8807ec5   
3월 17일부터 4월 18일까지 프로젝트 진행

# Step by Step
📬 1) BeautifulSoup 으로 다음뉴스 사회부분 뉴스기사 크롤링   
&nbsp; &nbsp;&nbsp; &nbsp;  : 칼럼명은 id, platform, main_category, sub_category, title, content, writer, writed_at 정보 가져오기   
&nbsp; &nbsp; &nbsp; &nbsp;  : 🗞️ => 해당 일자의 마지막 기사 확인방법 (마지막 페이지의 기사 개수 확인, 그 전 페이지의 기사와 동일한지 확인으로 해결!)   
📬 2) Scrapy 활용하여 대용량 데이터 가져오기 + csv로 저장하기   
📬 3) Data Cleansing 작업    
&nbsp; &nbsp; &nbsp; &nbsp; : 뉴스기사 본문에서 특수기호, 이미지 출처 등 뉴스기사 내용과 관련 없는 내용 삭제    
&nbsp; &nbsp; &nbsp; &nbsp; : 🗞️ => 정규표현식 활용  
📬 4) NLP - Topic Modeling 으로 뉴스기사들 주제별로 분류하기   
&nbsp; &nbsp;&nbsp; &nbsp;  : Scikit Learn으로 토픽별 주요 기사 추출        
&nbsp; &nbsp;&nbsp; &nbsp;  : 주요기사 추출후 각 기사에 대하여 Text Rank로 Matrix을 활용하여 핵심단어(키워드)추출     
&nbsp; &nbsp;&nbsp; &nbsp;  : 기사요약도 키워드 추출과 동일하게 Text Rank로 Matrix을 활용하여 주요기사 요약    
📬 5) Crontab 활용하여 Scheduling
&nbsp; &nbsp;&nbsp; &nbsp;  : Crontab 활용하여 매일 아침 전날 자료지우고, Scrpay 실행하여 새로운 자료 가져오고 main.py 실행하여 이메일 발송 할 수 있도록 설정!      
📬 5) HTML 문서 이메일로 발송시키기
