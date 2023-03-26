import scrapy
from daumnews_crawl.items import DaumnewsCrawlItem
from datetime import datetime, timedelta

import time
import re

class SocietyNewsSpider(scrapy.Spider): # 클래스 생성
    name = "society_news"
    allowed_domains = ["news.daum.net"] #allowed_domains으로 시작하는 url이 아니면 접근하지마
    start_urls = ["http://news.daum.net/breakingnews/society"] #크롤링할 페이지 주소를 나타내는 속성

    def start_requests(self): #날짜 및 카테고리 객체

        mains = ['society']
        subs = ['affair', 'people','education','media','woman','welfare','others','labor','environment',
        'nation','nation/seoul','nation/metro','nation/gangwon','nation/chungcheong', 'nation/gyeongsang',
        'nation/jeolla','nation/jeju','nation/others']

      # 탐색할 날짜 리스트를 먼저 생성합니다.
      start_date = datetime(2023, 2, 1)
      end_date = datetime(2023, 3, 16)
      dates = [start_date]
      while True:
          start_date = start_date + timedelta(days=1)
          dates.append(start_date)
          if start_date == end_date:
              break
      
      # 날짜 -> 카테고리1 -> 카테고리2
      for date in dates:
        detail_date = date.strftime('%Y%m%d') #  20230201 형태
        for main in mains: # main category
          for sub in subs: # sub category 
            #url = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={sub}&sid1={main}&date={detail_date}&page=1'  
            #URL = 'https://news.daum.net/breakingnews/{}/{}?page={}&regDate={}' response = requests.get(URL.format(main, sub,page,date)
            # meta는 다양한 정보를 보관하는 보관함으로 생각하면 편합니다.
            # yield scrapy.Request(url, self.url_parse, meta = {'page' : 1, 'urls' : [],  'main' : main, 'sub' : sub})

    # def url_parse(self, response):
       


    def parse(self, response): #parse() 추출한 웹페이지 처리를 위한 콜백 함수
        # print(response.text)
   
        li_tags = response.css('.list_news2.list_allnews li::text').getall()

        for li in li_tags: 
        
        item = <item 이름>()

        item['title'] = response.css('.cont_thumb .tit_thumb .link_txt::text').get() # title
        item['platform'] = response.css('.cont_thumb .tit_thumb .info_news::text').get()[:-8] #platform
        response.css('.cont_thumb .tit_thumb .info_news::text').get()[-6:] #writed_at (초는 없음)
        #date_time = str(date)[:4]+"-"+str(date)[4:6]+"-"+str(date)[6:]+str(time)+":00" # 작성시각
        response.css('.cont_thumb .desc_thumb .link_txt::text').get()#context 짤림
        #url
    

        #url 들어가서 기자이름이랑 본문 내용은 따로??? 함수 따로 만들어서??

        #id 
        item['writer'] = response.css('.info_view .txt_info::text').get() #writer                    
        item['article'] = response.css('section p[dmcf-ptype=general]::text').get() #FULL context  


yield item #마지막으로 item에 데이터 저장 
   