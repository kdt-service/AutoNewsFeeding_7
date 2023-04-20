# 📬AutoNewsFeeding_7📬
Daum 뉴스 크롤링 7조   
https://www.notion.so/7-7b61e47096184f6c8c1cb718d8807ec5   
3월 17일부터 4월 18일까지 프로젝트 진행   
news7_final 폴더를 통해 프로젝트 최종 코드 확인가능    

## 📬최종산출물 확인📬
[🗞️[2023-04-19 IT 간추린 뉴스] 오늘의 주요 IT 뉴스를 확인해보세요🗞️.pdf](https://github.com/kdt-service/AutoNewsFeeding_7/files/11267705/2023-04-19.IT.IT.pdf) 


# Step by Step
1) BeautifulSoup 으로 다음뉴스 사회부분 뉴스기사 크롤링   
&nbsp; &nbsp;&nbsp; &nbsp;  : 칼럼명은 id, platform, main_category, sub_category, title, content, writer, writed_at 정보 가져오기   
&nbsp; &nbsp; &nbsp; &nbsp;  📬  해당 일자의 마지막 기사 확인방법 (마지막 페이지의 기사 개수 확인, 그 전 페이지의 기사와 동일한지 확인으로 해결!)   
2) Scrapy 활용하여 대용량 데이터 가져오기 + csv로 저장하기   
&nbsp; &nbsp; &nbsp; &nbsp;  📬 3시간에 한번씩 Scrapy 가동! 가장 최신 url들 last_urls_new에 갱신. last_urls_original은 그 전 scrpay에서 최신 urls저장.      
&nbsp; &nbsp; &nbsp; &nbsp;  📬 Scrpay 양을 나눠서 함으로써 서버에 부담을 줄여 봇으로 차단되는 상황 방지 가능!      
3) Data Cleansing 작업    
&nbsp; &nbsp; &nbsp; &nbsp; : 뉴스기사 본문에서 특수기호, 이미지 출처 등 뉴스기사 내용과 관련 없는 내용 삭제    
&nbsp; &nbsp; &nbsp; &nbsp; 📬  정규표현식 활용  
4) NLP - Topic Modeling  LDA로 뉴스기사들 주제별로 분류하기   
&nbsp; &nbsp;&nbsp; &nbsp;  📬 Scikit Learn으로 토픽별 주요 기사 추출        
&nbsp; &nbsp;&nbsp; &nbsp;  📬 주요기사 추출후 각 기사에 대하여 Text Rank로 Matrix을 활용하여 핵심단어(키워드)추출     
&nbsp; &nbsp;&nbsp; &nbsp;  📬 기사요약도 키워드 추출과 동일하게 Text Rank로 Matrix을 활용하여 주요기사 요약   
5) Figma , Stripo.email 활용하여 HTML문서 양식 만들기   
&nbsp; &nbsp;&nbsp; &nbsp;  : 메일로 발송할 HTML 문서 양식 디자인 만들기
6) Crontab 활용하여 Scheduling & 자동화    
&nbsp; &nbsp;&nbsp; &nbsp;  📬 Crontab 활용하여 전날 자료 지우기, 최신 기사 Scrawl, 메일발송까지 매일 아침 실행하도록 설정
7) 모든 과정이 유기적으로 진행되도록 통합하는 코드 작성     
&nbsp; &nbsp;&nbsp; &nbsp;  : 실행분야에 따라서 파일분리, 전체 관리 코드는 main.py








