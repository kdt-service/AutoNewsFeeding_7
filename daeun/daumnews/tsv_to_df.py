import pandas as pd
METADATA_PATH = './daumnews/metadata.tsv'
NEWS_PATH = './daumnews/news_contents/'

def get_contents(news_id, ctg):
    if ctg == '사회':
        return open(NEWS_PATH + news_id + '.txt', 'r', encoding='utf-8').read()

def get_df():
    df = pd.read_csv(METADATA_PATH, sep='\t')
    df['content'] = df.apply(lambda x: get_contents(x['id'], x['main_category']), axis=1)
    return df

if __name__ == '__main__':
    get_df()
