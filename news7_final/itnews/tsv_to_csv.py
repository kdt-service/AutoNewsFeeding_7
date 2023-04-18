import pandas as pd
from datetime import datetime
METADATA_PATH = '/home/ubuntu/news7/itnews/itnews/metadata.tsv'
NEWS_PATH = '/home/ubuntu/news7/itnews/itnews/news_contents/'

def get_contents(news_id, ctg):
    if ctg == 'IT':
        return open(NEWS_PATH + str(news_id) + '.txt', 'r', encoding='utf-8').read()

def get_df():
    df = pd.read_csv(METADATA_PATH, sep='\t')
    df.columns=['id',  'main_category', 'sub_category', 'title', 'writer', 'writed_at','img']
    df['content'] = df.apply(lambda x: get_contents(x['id'], x['main_category']), axis=1)
    df['platform'] = '다음'
    df=df[['id', 'platform', 'main_category', 'sub_category', 'title', 'content', 'writer', 'writed_at','img']]
    
    for i in range(len(df.writed_at)) :
        s = df.writed_at[i].split(".")
        if int(s[2])//10== 0: #일이 한자리수
            s[2]=str("0")+s[2].replace(' ','')
        #df.writed_at[i]=s[0]+ "-0"+s[1].strip()+"-"+s[2].strip()+s[3]+":00"
        df.loc[i, 'writed_at'] = s[0] + "-0" + s[1].strip() + "-" + s[2].strip() + s[3] + ":00"
    
    for i in range(len(df)):
        # str(datetime.today().strftime("%Y%m%d")) : 오늘날짜 20230413 형태로 가져오는데 scrapy 실행이 
        if str(datetime.today().strftime("%Y%m%d")) in str(df.id[i]): # 오늘날짜 기사가 크롤링됨ㅠㅠ 이거 없애주는 코드 : 일반화시켜야함
            df.drop(i, axis = 0, inplace= True)
    
    return df
