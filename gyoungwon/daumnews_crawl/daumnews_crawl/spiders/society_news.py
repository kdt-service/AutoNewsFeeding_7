import scrapy
from <프로젝트 이름>.items import <item 이름> 

class SocietyNewsSpider(scrapy.Spider):
    name = "society_news"
    allowed_domains = ["news.daum.net"] #allowed_domains으로 시작하는 url이 아니면 접근하지마
    start_urls = ["http://news.daum.net/breakingnews/society"] #크롤링할 페이지 주소를 나타내는 속성

    def parse(self, response): #parse() 추출한 웹페이지 처리를 위한 콜백 함수
        # print(response.text)
        for main in mains :
            for sub in subs:

   
        li_tags = response.css('.list_news2.list_allnews li::text').getall()

        for li in li_tags: 
        
        item = <item 이름>()

    item['title'] = response.css('.cont_thumb .tit_thumb .link_txt::text').get() # title
    item['platform'] = response.css('.cont_thumb .tit_thumb .info_news::text').get()[:-8] #platform
    response.css('.cont_thumb .tit_thumb .info_news::text').get()[-6:] #writed_at (초는 없음)
    #date_time = str(date)[:4]+"-"+str(date)[4:6]+"-"+str(date)[6:]+str(time)+":00" # 작성시각
    response.css('.cont_thumb .desc_thumb .link_txt::text').get()#context 짤림
    #url
    

#url 들어가서 기자이름이랑 본문 내용은 따로???... 클래스 다르게 해서?..

#id
    item['writer'] = response.css('.info_view .txt_info::text').get() #writer                    
    item['article'] = response.css('section p[dmcf-ptype=general]::text').get() #FULL context  


yield item #마지막으로 item에 데이터 저장 
   