import scrapy
import traceback

from datetime import datetime, timedelta
import re

            
class DaumnewsspiderSpider(scrapy.Spider):
    name = 'daumnewsspider'

    CATEGORIES = {
        ('사회','society'):
         {'사건/사고':'affair',
          '인물':'people',
          '교육':'education',
          '미디어':'media', 
          '여성':'woman',
          '복지':'welfare',
          '사회일반':'others',
          '노동':'labor',
          '환경':'environment',
          '전국':'nation',
          '서울':'nation/seoul',
          '수도권':'nation/metro',
          '강원':'nation/gangwon',
          '충청':'nation/chungcheong',
          '경상':'nation/gyeongsang',
          '전라':'nation/jeolla',
          '제주':'nation/jeju',
          '지역일반':'nation/others'},
     }


    URL_FORMAT = 'https://news.daum.net/breakingnews/{}/{}?page={}&regDate={}'

    def start_requests(self):
        
        start_date = datetime(2023, 2, 1)
        end_date = datetime(2023, 3, 16)
        dates = [start_date]
        while True:
            start_date = start_date + timedelta(days=1)
            dates.append(start_date)
            if start_date == end_date:
              break

        for main in self.CATEGORIES:
            main_kor, main_eng = main
            for sub_kor, sub_eng in self.CATEGORIES[main].items():
                for date in dates :
                    target_url = self.URL_FORMAT.format(main_eng, sub_eng, 1, date.strftime('%Y%m%d'))
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
            
            news_id = response.url.split('/')[-1]
            
            with open('./news_contents/'+news_id+'.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            
            datas = [news_id, response.meta.pop('main_category'), response.meta.pop('sub_category'), title, writer, writed_at]

            with open('./metadata.tsv', 'a', encoding='utf-8') as f:
                f.write('\t'.join(map(str,datas)) + '\n')

        except:
            print('실패')
            traceback.print_exc()
            with open('error_urls', 'a') as f:
                f.write(response.url+'\n')
    




