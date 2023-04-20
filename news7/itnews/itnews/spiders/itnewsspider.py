import scrapy
import traceback
import re

            
class itnewsspiderSpider(scrapy.Spider):
    name = 'itnewsspider'
    
    CATEGORIES = {
        ('IT','digital'):
         {'인터넷':'internet','게임':'game','휴대폰통신':'it','IT기기':'device', 
        '통신_모바일':'mobile', '소프트웨어':'software', 'Tech일반':'others'},
    } #'과학':'science' 수집 x 

    URL_FORMAT = 'https://news.daum.net/breakingnews/{}/{}?page={}&regDate={}'
    

    def start_requests(self):
        from datetime import datetime, timedelta, date
        if datetime.now().hour <= 9 : # 오전 9시 이전이면 
            start_date = date.today()- timedelta(1) #2023-04-10 식으로 출력 
        else : # 오전 9시 이후면 오늘 날짜 기사 크롤링
            start_date = date.today()
        end_date = start_date
        date_list = [start_date] #[datetime.date(2023, 4, 10)] # 어제, 오늘
        
        # 새 urls 기존 urls로 내용 복사. 
        f= open('/home/ubuntu/news7/last_urls_original','w')   # 파일열기
        last_urltext= open('/home/ubuntu/news7/last_urls_new','r').read()  # last_urls에 있는 내용 str 형태로 가져오기
        f.write(last_urltext)
        f.close()  # 파일닫기 -> 파일 안에 있는 내용 초기화하기! for 새로운 뉴스기사 저장하기 위해

        # last_urls: 초기화
        fn= open('/home/ubuntu/news7/last_urls_new','w')
        fn.close()

        for main in self.CATEGORIES:
            main_kor, main_eng = main
            for sub_kor, sub_eng in self.CATEGORIES[main].items(): # items니까 key, item 동시에 갖고온다
                for dates in date_list : # target_url은 15개 목록들 나와져있는 url 갖고오기
                    target_url = self.URL_FORMAT.format(main_eng, sub_eng, 1, dates.strftime('%Y%m%d'))
                    yield scrapy.Request(url = target_url, callback= self.url_parse, 
                                         meta={'page':1, 'urls':[], 'main_category':main_kor, 'sub_category':sub_kor, 'last_url':last_urltext})
            

    def url_parse(self, response):
        urls = response.css('a.link_thumb::attr(href)').getall()

        # 마지막 url 저장하는 코드
        if response.meta['page']==1:
            # 각 카테고리별 끝나고 마지막 url 저장해놔야하고.     
                fn= open('/home/ubuntu/news7/last_urls_new','a')   # 파일열기
                fn.write(response.css('a.link_thumb::attr(href)').get()+'\n') # 카테고리별 마지막 url 넣기     
                fn.close()  # 파일닫기 

        if response.meta.pop('urls') == urls: # 마지막 페이지인지 확인 : 제일 최근 url들이 같으면 stop의 의미. 
            return
        
        # 겹쳤으면 더이상 진행 안해도 돼! 
        for url in urls:
            if url in response.meta['last_url'].split('\n'): # 이미 scrawl했던 url이면 더이상 할 필요 없어! 중지! 
                print('겹쳤다!',url) # break문이 어디서 걸리는지 확인, 최신 last_urls과 같아야함. 
                break
            yield scrapy.Request(url=url, callback=self.parse, meta={**response.meta})
        
        page = response.meta.pop('page')
        target_url = re.sub('page\=\d+', f'page={page+1}', response.url)
        yield scrapy.Request(url = target_url, callback=self.url_parse,  meta={**response.meta, 'page': page+1, 'urls':urls})
       
    def parse(self, response):
        try:
            title = response.css('.tit_view::text').get().strip()
            content = response.css('.article_view')[0].xpath('string(.)').extract()[0].strip()  
            
            infos = response.css('.info_view .txt_info')
            if len(infos) == 1:
                writer = ''
                writed_at = infos[0].css('.num_date::text').get()
            else:
                writer = response.css('.info_view .txt_info::text').get()
                writed_at = infos[1].css('.num_date::text').get()
            
            img_tag = response.css('.thumb_g_article')
            if img_tag:
                img = img_tag.css('img::attr(src)').get()
            else: # 기사에 이미지가 없는 경우 대체 이미지 투입! 
                img = 'https://sitem.ssgcdn.com/95/89/87/item/1000111878995_i1_1100.jpg'
            
            news_id = response.url.split('/')[-1]

            with open('/home/ubuntu/news7/itnews/itnews/news_contents/'+news_id+'.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            
            datas = [news_id, response.meta.pop('main_category'), response.meta.pop('sub_category'), title, writer, writed_at, img]

            with open('/home/ubuntu/news7/itnews/itnews/metadata.tsv', 'a', encoding='utf-8') as f:
                f.write('\t'.join(map(str,datas)) + '\n')
        
        except:
            traceback.print_exc()
            with open('error_urls', 'a') as f:
                f.write(response.url+'\n')