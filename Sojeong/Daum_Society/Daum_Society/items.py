# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DaumSocietyItem(scrapy.Item):
    id = scrapy.Field() # id
    platform = scrapy.Field() # 신문사
    main_category = scrapy.Field() # 메인 카테고리
    sub_category = scrapy.Field() # 서브 카테고리
    title = scrapy.Field() # 제목
    content = scrapy.Field() # 기사
    writed_at = scrapy.Field() #등록일
    writer = scrapy.Field() # 기자
    pass
