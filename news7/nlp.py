""" 
nlp.py는 데이터클렌징, 전처리, 토픽모델링, 키워드추출, 기사요약하는 코드를 담고 있습니다. 
"""

# data 전처리 부분 : 추가 cleansing 
import re
def cleansing(data): # 해결 안된 부분 : url, 기자, 
    new_df = data
    # 특수기호 제거
    new_df['content']=new_df['content'].map(lambda x:re.sub('[▶△▶️◀️▷ⓒ■◆●©️]', '', str(x))) 
    new_df['content']=new_df['content'].map(lambda x:re.sub('“', '"', str(x))) 
    new_df['content']=new_df['content'].map(lambda x:re.sub('”','"', str(x))) 
    new_df['content']=new_df['content'].map(lambda x:re.sub("‘","'", str(x))) 
    new_df['content']=new_df['content'].map(lambda x:re.sub("’","'", str(x))) 
    # 인코딩 오류 해결 (공백으로 치환) , 이메일, url 지우기
    new_df['content']=new_df['content'].map(lambda x:re.sub("[\xa0\u2008\u2190]"," ", str(x))) 
    new_df['content']=new_df['content'].map(lambda x:re.sub('([\w\-]+(\@|\.)[\w\-.]+)',"", str(x)))
    new_df['content']=new_df['content'].map(lambda x:re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',"", str(x)))
    # ., 공백, 줄바꿈 여러개 제거 , \s -> 공백( ), 탭(\t), 줄바꿈(\n)
    new_df['content']=new_df['content'].map(lambda x:re.sub('[\.]{2,}', '.', x) )
    new_df['content']=new_df['content'].map(lambda x:re.sub('[\t]+', ' ', x) )
    new_df['content']=new_df['content'].map(lambda x:re.sub('[ ]{2,}', ' ', x) )
    new_df['content']=new_df['content'].map(lambda x:re.sub('[\n]{2,}', '\n', x) )

def morecleansing (data):
    new_df = data
    #뉴스기사 출처 ( = ) 형태 없애기 코드 '\(.*=.*\) '
    new_df['content']=new_df['content'].map(lambda x:re.sub('\(.*=.*\) ', '', str(x))) 
    #뉴스기사 출처 ( = ) 형태 없애기 코드 '\[.*=.*\] '
    new_df['content']=new_df['content'].map(lambda x:re.sub('\[.*=.*\] ', '', str(x))) 
    # 날짜 지우기 '2023.[0-9]?[0-9].[0-9]?[0-9]'
    new_df['content']=new_df['content'].map(lambda x:re.sub('2023.[0-9]?[0-9].[0-9]?[0-9]', '', str(x))) 
    # '제보는 카톡 okjebo' 없애기'
    new_df['content']=new_df['content'].map(lambda x:re.sub('제보는 카톡 okjebo' , '', str(x))) 
    # '재판매 및 DB 금지'  없애기
    new_df['content']=new_df['content'].map(lambda x:re.sub('재판매 및 DB 금지', '', str(x))) 
    # '※ 자세한 내용은 동영상으로 확인하실 수 있습니다.'  없애기
    new_df['content']=new_df['content'].map(lambda x:re.sub('※ 자세한 내용은 동영상으로 확인하실 수 있습니다.', '', str(x))) 
    #※CBS노컷뉴스는 여러분의 제보로 함께 세상을 바꿉니다. 각종 비리와 부당대우, 사건사고와 미담 등 모든 얘깃거리를 알려주세요.\n이메일 :\n카카오톡 :@노컷뉴스\n사이트 :\nCBS노컷뉴스 김승모 기자 \n기자와 카톡 채팅하기 노컷뉴스 영상 구독하기'
    sth = '※CBS노컷뉴스는 여러분의 제보로 함께 세상을 바꿉니다. 각종 비리와 부당대우, 사건사고와 미담 등 모든 얘깃거리를 알려주세요.\n이메일 :\n카카오톡 :@노컷뉴스\n사이트 :\nCBS노컷뉴스 김승모 기자 \n기자와 카톡 채팅하기 노컷뉴스 영상 구독하기'
    new_df['content']=new_df['content'].map(lambda x:re.sub(sth, '', str(x))) 
    #무단전재 및 재배포 금지 없애기기
    new_df['content']=new_df['content'].map(lambda x:re.sub('무단전재 및 재배포 금지', '', str(x))) 
    # 제공 없애기
    new_df['content'] = new_df['content'].map(lambda x:re.sub(' 제공', '', str(x))) 
    # 페이스북 /LeYN1 트위터 @yonhap_graphic 없애기
    new_df['content'] = new_df['content'].map(lambda x:re.sub('페이스북 /LeYN1 트위터 @yonhap_graphic', '', str(x))) 
    return new_df

def preprocessing (data):
    news = data
    news.dropna(subset=['content'], inplace=True) #content null 값 행 삭제 
    news.drop_duplicates(subset=['content'], ignore_index=True, inplace=True) # 중복 기사 삭제 
    return news

import konlpy
import pandas as pd
import numpy as np

def topicmodeling(data):
    news= data
    #tokenization함수 만들기
    def tokenize_korean_text(text):
        okt = konlpy.tag.Okt()
        okt_morphs = okt.pos(text) 
        words = []
        stopwords = ['하는', '있다', '있는', '위해', '통해', '한다', '때문', '했다'] # 불용어 사전  
        for word, pos in okt_morphs:
            if pos in ['Adjective', 'Verb', 'Noun', 'Alpha', 'Number'] and word not in stopwords:  # 형용사, 동사, 명사, 영어, 숫자만 남김
                words.append(word)
        words_str = ' '.join(words)
        return words_str
    
    # 1. news['content']를 하나씩 tokenize해서 list로 저장 : okay 
    tokenized_list = []
    for text in news['content']:
        tokenized_list.append(tokenize_korean_text(text))
    
    #2. 단어가 1-20개만 포함된 corpus 삭제  
    drop_corpus = []
    for index in range(len(tokenized_list)):
        corpus = tokenized_list[index]
        if len(set(corpus.split())) < 21:   # 같은 단어 1-20개만 반복되는 corpus도 지우기 위해 set()을 사용
            news.drop(index=[index], axis=0, inplace=True)
            drop_corpus.append(corpus)                   
    for corpus in drop_corpus:
        tokenized_list.remove(corpus)
    news.reset_index(drop=True, inplace=True)

    #3.vectorization 
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    count_vectorizer = CountVectorizer() # total number of tokens 구하기
    X = count_vectorizer.fit_transform(tokenized_list)
    word_count = X.toarray().sum(axis=1)
    
    count_vectorizer = CountVectorizer() # total number of unique tokens 구하기
    X = count_vectorizer.fit_transform(tokenized_list)
    unique_tokens = count_vectorizer.get_feature_names()
    count_unique_tokens = len(unique_tokens)

    #LDA 는 Count기반의 Vectorizer만 적용 
    count_vectorizer_0 = CountVectorizer(max_df=0.8, max_features=round(count_unique_tokens*0.8), min_df=10, ngram_range=(1,2))
    # 10개의 문서 미만으로 등장하는 단어는 제외, 전체의 80% 이상으로 자주 등장하는 단어는 제외, 최대로 사용할 단어 수(백터 수)는 유니크한 토큰 수의 80%  # unigram, bigram 포함
    feat_vect = count_vectorizer_0.fit_transform(tokenized_list)

    #4. LDA 
    lda = LatentDirichletAllocation(n_components=6)  # 토픽 수는 6개로 설정
    lda.fit(feat_vect)

    def display_topics(model, feature_names, num_top_words):
        for topic_index, topic in enumerate(model.components_):
            print('Topic #', topic_index)

            # components_ array에서 가장 값이 큰 순으로 정렬했을 때, 그 값의 array index를 반환. 
            topic_word_indexes = topic.argsort()[::-1]
            top_indexes=topic_word_indexes[:num_top_words]
            
            # top_indexes대상인 index별로 feature_names에 해당하는 word feature 추출 후 join으로 concat
            feature_concat = ' '.join([feature_names[i] for i in top_indexes])                
            print(feature_concat)

    #5. 토픽별 연관어 출력
    # CountVectorizer객체내의 전체 word들의 명칭을 get_features_names()를 통해 추출
    feature_names = count_vectorizer_0.get_feature_names()
    # Topic별 가장 연관도가 높은 word를 10개만 추출
    display_topics(lda, feature_names, 10)

    #6. 각 문서별로 가장 가까운 topic으로 할당
    doc_topic = lda.transform(feat_vect)
    doc_per_topic_list = []
    for n in range(doc_topic.shape[0]):
        topic_most_pr = doc_topic[n].argmax()
        topic_pr = doc_topic[n].max()
        doc_per_topic_list.append([n, topic_most_pr, topic_pr])
    doc_topic_df = pd.DataFrame(doc_per_topic_list, columns=['Doc_Num', 'Topic', 'Percentage'])
    doc_topic_df = doc_topic_df.join(news)

    #7. 토픽별로, 가장 높은 확률로 할당된 문서 top3 확인
    for topic in range(len(doc_topic_df['Topic'].unique())):
        top_pr_topics = doc_topic_df[doc_topic_df['Topic'] == topic].sort_values(by='Percentage', ascending=False)
        
   #8. 키워드 요약, 문장 요약을 위해 토픽 6개만 들어있는 리스트 만들기
    top6_topic_contents = [] #content만 담겨있는 list
    for topic in range(len(doc_topic_df['Topic'].unique())):
        top_pr_topics = doc_topic_df[doc_topic_df['Topic'] == topic].sort_values(by='Percentage', ascending=False)
        content1 = top_pr_topics['content'].iloc[0]
        top6_topic_contents.append([content1])
    top6_topic = [] #id, title, content만 담겨있는 list
    for topic in range(len(doc_topic_df['Topic'].unique())):
        top_pr_topics = doc_topic_df[doc_topic_df['Topic'] == topic].sort_values(by='Percentage', ascending=False)
        content1 = top_pr_topics.iloc[0]
        top6_topic.append([content1['id'], content1['title'], content1['content'], content1['img']])
    top6_topic = pd.DataFrame(top6_topic, columns=['id', 'title', 'content','img']) # 현재는 id,제목, 내용, img만 들어가 있는 df

    #9. 키워드 추출단계 : TextRank 활용
    import matplotlib.pyplot as plt #한글깨짐 처리
    plt.rc('font', family='NanumBarunGothic') 
    plt.rcParams['axes.unicode_minus'] = False

    import warnings #경고무시
    warnings.filterwarnings('ignore')

    from konlpy.tag import Mecab
    mecab = Mecab()
    preprocessed_docs = []

    for idx,doc in enumerate(top6_topic.content) :
        preprocessed_docs.append(' '.join([token[0] for token in mecab.pos(doc) if token[1][0] in ['N', 'V']])) # 명사와 동사만으로 문서 전처리
    count_vectorizer = CountVectorizer(max_df=0.85, max_features=10000)
    word_count_vector = count_vectorizer.fit_transform(preprocessed_docs)    

    from sklearn.feature_extraction.text import TfidfTransformer
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    def sort_keywords(keywords):
        return sorted(zip(keywords.col, keywords.data), key=lambda x: (x[1], x[0]), reverse=True)
    def extract_keywords(feature_names, sorted_keywords, n=5):
        return [(feature_names[idx], score) for idx, score in sorted_keywords[:n]]
    keywords_list =[]
    for i in range(len(preprocessed_docs)):
        doc = preprocessed_docs[i] # 핵심키워드 추출할 문서 조회
        feature_names = count_vectorizer.get_feature_names() # TF-IDF 단어 목록
        tf_idf_vector = tfidf_transformer.transform(count_vectorizer.transform([doc])) # 문서의 tf-idf 추출
        sorted_keywords = sort_keywords(tf_idf_vector.tocoo()) # TF-IDF를 기준으로 역순 정렬
        keywords = extract_keywords(feature_names, sorted_keywords, 5) # 사용자가 지정한 개수(5)만큼 키워드 추출
        keywords_list.append([k[0] for k in keywords])
    top6_topic['keywords']= keywords_list
    
    #10. 기사요약 단계
    def sentence_similarity(sentence1, sentence2): # 문장간 유사도 측정 (자카드 유사도 사용)
        mecab = Mecab()
        # 각 문장을 소문자로 변환
        sentence1 = [word for word in mecab.pos(sentence1) if word[1][0] in ['N', 'V']]
        sentence2 = [word for word in mecab.pos(sentence2) if word[1][0] in ['N', 'V']]

        union = set(sentence1).union(set(sentence2))
        intersection = set(sentence1).intersection(set(sentence2))
        return len(intersection)/len(union) 
    
    import nltk
    nltk.download('punkt')
    from nltk.tokenize import sent_tokenize
    def buildMatrix(sentences):
        score = np.ones(len(sentences) ,dtype=np.float32) # zeros도 가능, 결국 나한테 들어오는 엣지 가중치들을 통해 최초 점수를 가지게 되므로
        # 문장별로 그래프 edge를 Matrix 형태로 생성
        weighted_edge = np.zeros((len(sentences), len(sentences))
                                ,dtype=np.float32)

        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i == j: continue
                weighted_edge[i][j] = sentence_similarity(sentences[i], sentences[j])
        # normalize 
        for i in range(len(weighted_edge)):
            score[i] = weighted_edge[i].sum()
            weighted_edge[i] /= score[i]

        return score, weighted_edge
    def scoring(A, P, eps=0.0001, d=0.85, max_iter = 50):
        for iter in range(0,max_iter):
            newP = (1 - d) + d * A.T.dot(P)

            if abs((newP - P).sum()) <= eps:
                return newP
            P = newP
        return newP

    def summarize(text, n=10):
        text = sent_tokenize(text)
        score_init, weighted_edge = buildMatrix(text) 
        score = scoring(weighted_edge, score_init)
        
        sorted_scores = sorted(enumerate(score), key=lambda item: item[1], reverse=True)[:n]
        return [(text[s[0]], s[1]) for s in sorted_scores ]
    summary_list = []
    for i in range(len(top6_topic)):
        summary = summarize(top6_topic.content[i], 3)
        summary_list.append([sent[0] for sent in summary])
    top6_topic['summary']= summary_list

    return top6_topic