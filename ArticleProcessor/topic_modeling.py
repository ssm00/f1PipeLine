import pymysql
import nltk
from Db import f1Db
import json
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
from nltk.stem import WordNetLemmatizer
import string
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import PorterStemmer
from collections import Counter

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

def get_content1(db_info):
    database = f1Db.Database(db_info)
    original_content_query = "select original_content from article where sequence = 2"
    database.execute(query=original_content_query)
    res = database.cursor.fetchall()
    content = res[0].get('original_content')
    #tokens = TreebankWordTokenizer().tokenize(content)

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
    res = []
    for tag in tag_list:
        if tag[1] in need_tags:
            res.append(tag)

    bow = Counter([f"{word}/{pos_tag}" for word, pos_tag in res])
    bow_json = json.dumps(bow)
    query = "update article set bow = %s where sequence = %s"
    values = bow_json, 2
    database.cursor.execute(query, values)
    #database.commit()

get_content1(mysql_db)
