from Db import f1Db
import tqdm
import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

with open('../Db/db_info.json', 'r') as file:
    db_info_json = json.load(file)
mysql_db = db_info_json['article_data_source']

def download_nltk_package():
    nltk.download('punkt') # 토크나이저
    nltk.download('webtext') # 텍스트 모음
    nltk.download('wordnet') # 영어 어휘 데이터베이스
    nltk.download('stopwords') # 불용어
    nltk.download('tagsets') # 품사태깅
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('punkt_tab')

def update_bow(db_info):
    database = f1Db.Database(db_info)
    original_content_query = "select original_content from article where sequence = 2"
    database.execute(query=original_content_query)
    res = database.cursor.fetchall()
    content = res[0].get('original_content')

    tokens = word_tokenize(content)

    # 구두점 + 추가적인 제거하고 싶은 특수문자들
    additional_punctuations = set(string.punctuation) | {'“', '”', '’', "'", '"', '‘', "-","–"}  # 큰따옴표, 작은따옴표, 특수문자 등 추가

    # 구두점 제거
    tokens_without_punctuation = [word for word in tokens if word not in additional_punctuations]

    # 불용어 제거 (구두점 제거 후에 처리)
    en_stops = set(stopwords.words('english'))
    without_stopwords = [word for word in tokens_without_punctuation if word.lower() not in en_stops]

    # 표제어 추출
    lemmatizer = WordNetLemmatizer()
    without_lemma = [lemmatizer.lemmatize(token) for token in without_stopwords]
    
    # 어간 추출
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens_without_punctuation]

    tag_list = nltk.pos_tag(without_lemma)

    #nn, nnp, nns, nnps, vb, vbd,
    need_tags = ["NN","NNP","NNS","NNPS","VB","VBD"]
    res_list = []
    for tag in tag_list:
        if tag[1] in need_tags:
            res_list.append(tag[0])
    res = ",".join(res_list)
    query = "update article set bow = %s where sequence = %s"
    values = res, 2
    database.cursor.execute(query, values)
    database.commit()

def get_all_bow(db_info):
    database = f1Db.Database(db_info)
    select_all_bow = "select bow from article where sequence = 2"
    bow_list = database.fetch_all(select_all_bow)
    all_word_list = []
    for bow in bow_list:
        bow = bow.get("bow")
        all_word_list.append(bow.split(","))

    #corpora의 매개변수로는 문서의 각 단어를 담고 있는리스트를 담고있는 전체 리스트. 즉 문서마다 리스트로 분리 해야함, 하나의 리스트에 모든 단어 다넣으면 하나의 문서로 인식함
    dictionary = corpora.Dictionary(all_word_list)
    corpus = [dictionary.doc2bow(doc) for doc in tqdm.tqdm(all_word_list)]

    #토픽모델링
    #NUM_TOPICS = 20  # 20개의 토픽, k=20
    #ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
    #topics = ldamodel.print_topics(num_words=4)
    coherence_values = []
    for i in range(2, 15):
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=i, id2word=dictionary, passes=15)
        coherence_model_lda = CoherenceModel(model=ldamodel, texts=all_word_list, dictionary=dictionary, topn=10)
        coherence_lda = coherence_model_lda.get_coherence()
        coherence_values.append(coherence_lda)
    x = range(2, 15)
    plt.plot(x, coherence_values)
    plt.xlabel("number of topics")
    plt.ylabel("coherence score")
    plt.show()


#update_bow(mysql_db)
get_all_bow(mysql_db)

