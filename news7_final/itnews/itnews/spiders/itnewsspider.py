import scrapy
import traceback #오류추적 모듈
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
        start_date = date.today() - timedelta(1) #2023-04-10 식으로 출력 
        end_date = start_date
        date_list = [start_date] #[datetime.date(2023, 4, 10)]
        
        for main in self.CATEGORIES:
            main_kor, main_eng = main
            for sub_kor, sub_eng in self.CATEGORIES[main].items(): # items니까 key, item 동시에 갖고온다
                for dates in date_list : # target_url은 15개 목록들 나와져있는 url 갖고오기
                    target_url = self.URL_FORMAT.format(main_eng, sub_eng, 1, dates.strftime('%Y%m%d'))
                    yield scrapy.Request(url = target_url, callback= self.url_parse, 
                                         meta={'page':1, 'urls':[], 'main_category':main_kor, 'sub_category':sub_kor})                               

    def url_parse(self, response):
        urls = response.css('a.link_thumb::attr(href)').getall()
        if response.meta.pop('urls') == urls:
            return
        
        for url in urls:
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