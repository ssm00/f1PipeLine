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

with open('../Db/db_info.json', 'r') as file:
    db_info_json = json.load(file)
mysql_db = db_info_json['article_data_source']


# nltk.download('punkt') # 토크나이저
# nltk.download('webtext') # 텍스트 모음
# nltk.download('wordnet') # 영어 어휘 데이터베이스
# nltk.download('stopwords') # 불용어
# nltk.download('tagsets') # 품사태깅
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt_tab')

def get_content(db_info):
    database = f1Db.Database(db_info)
    original_content_query = "select original_content from article where sequence = 1"
    database.execute(query=original_content_query)
    res = database.cursor.fetchall()
    content = res[0].get('original_content')

    # 불용어 처리
    tokens = word_tokenize(content)

    additional_punctuations = set(string.punctuation) | {'“', '”', '’', "'", '"', '‘'}

    # 구두점 제거
    tokens_without_punctuation = [word for word in tokens if word not in additional_punctuations]

    # 불용어 제거 (Gensim 사용)
    tokens_without_stopwords = [remove_stopwords(token) for token in tokens_without_punctuation]
    print(tokens_without_stopwords)

    # 표제어 추출
    lemmatizer = WordNetLemmatizer()
    without_lemma = [lemmatizer.lemmatize(token) for token in tokens_without_stopwords]
    print(without_lemma)


def get_content1(db_info):
    database = f1Db.Database(db_info)
    original_content_query = "select original_content from article where sequence = 1"
    database.execute(query=original_content_query)
    res = database.cursor.fetchall()
    content = res[0].get('original_content')
    tokens = word_tokenize(content)

    # 구두점 + 추가적인 제거하고 싶은 특수문자들
    additional_punctuations = set(string.punctuation) | {'“', '”', '’', "'", '"', '‘'}  # 큰따옴표, 작은따옴표, 특수문자 등 추가

    # 구두점 제거
    tokens_without_punctuation = [word for word in tokens if word not in additional_punctuations]
    print(tokens_without_punctuation)

    # 불용어 제거 (구두점 제거 후에 처리)
    en_stops = set(stopwords.words('english'))
    without_stopwords = [word for word in tokens_without_punctuation if word.lower() not in en_stops]
    print(without_stopwords)

    # 표제어 추출
    lemmatizer = WordNetLemmatizer()
    without_lemma = [lemmatizer.lemmatize(token) for token in without_stopwords]
    print(without_lemma)

get_content(mysql_db)
get_content1(mysql_db)