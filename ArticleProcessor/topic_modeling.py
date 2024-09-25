import spacy

from Db import f1Db
from tqdm import tqdm
from datetime import datetime
import json
import string
import nltk
import time

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import ne_chunk
from nltk.tree import Tree

from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim


from multiprocessing import Process, freeze_support
from collections import defaultdict

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
    nltk.download('maxent_ne_chunker_tab')
    nltk.download('words')


def exe_bow(content):
    # content = content.get('original_content')
    tokens = word_tokenize(content)
    # 구두점 + 추가적인 제거하고 싶은 특수문자들
    additional_punctuations = set(string.punctuation) | {'“', '”', '’', "'", '"', '‘', "-",
                                                         "–"}  # 큰따옴표, 작은따옴표, 특수문자 등 추가
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

    #사람이름 추출
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    with open("./f1_name_list.json", "r") as file:
        f1_name_list_json = json.load(file)
        f1_name_list = f1_name_list_json.get("people")

    driver_list = []
    engineer_list = []
    director_list = []
    ceo_list = []
    f1_name_category = {
        "driver": driver_list,
        "engineer": engineer_list,
        "director": director_list,
        "ceo": ceo_list
    }
    for people_type, name_list in f1_name_list.items():
        if people_type in f1_name_category:
            f1_name_category[people_type].extend(name for full_name in name_list for name in full_name.split(" "))
    # nn, nnp, nns, nnps, vb, vbd,
    need_tags = ["NN", "NNP", "NNS", "NNPS", "VB", "VBD"]

    res_list = []
    for tag in tag_list:
        if tag[1] in need_tags and tag[0] in driver_list:
            res_list.extend([tag[0]] * 3)
        elif tag[1] in need_tags and tag[0] in director_list:
            res_list.extend([tag[0]] * 3)
        elif tag[1] in need_tags and tag[0] in engineer_list:
            res_list.extend([tag[0]] * 2)
        elif tag[1] in need_tags and tag[0] in ceo_list:
            res_list.extend([tag[0]] * 2)
        elif tag[1] in need_tags:
            res_list.append(tag[0])
    res = ",".join(res_list)
    return res

def spyc(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    person_names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    print(person_names)
    return person_names

def update_bow(db_info):
    database = f1Db.Database(db_info)
    original_content_query = "select sequence, original_content from article where Date(created_at) = %s"
    today = datetime.now().date()
    content_list = database.fetch_all(original_content_query, today)
    for content in content_list:
        query = "update article set bow = %s where sequence = %s"
        bow = exe_bow(content)
        values = (bow, content.get("sequence"))
        database.cursor.execute(query, values)
    database.commit()

def get_all_bow(db_info):
    start = time.time()
    database = f1Db.Database(db_info)
    select_all_bow = "select sequence, bow from article where Date(created_at) = %s"
    today = datetime.now().date()
    bow_list = database.fetch_all(select_all_bow, today)

    all_word_list = []
    id_list = []
    for bow in bow_list:
        id = bow.get("sequence")
        bow = bow.get("bow")
        id_list.append(id)
        all_word_list.append(bow.split(","))

    #corpora의 매개변수로는 문서의 각 단어를 담고 있는리스트를 담고있는 전체 리스트. 즉 문서마다 리스트로 분리 해야함, 하나의 리스트에 모든 단어 다넣으면 하나의 문서로 인식함
    dictionary = corpora.Dictionary(all_word_list)
    corpus = [dictionary.doc2bow(doc) for doc in tqdm(all_word_list)]

    #토픽모델링
    modeling_range = range(2, 20, 2)
    coherence_values = []
    model_list = []
    for i in tqdm(modeling_range):
        # passes : 최대 반복 횟수
        ldamodel = LdaModel(corpus, num_topics=i, id2word=dictionary, passes=5)
        model_list.append(ldamodel)
        coherence_model_lda = CoherenceModel(model=ldamodel, texts=all_word_list, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        coherence_values.append(coherence_lda)
    best_model_index = coherence_values.index(max(coherence_values))
    best_model = model_list[best_model_index]
    # doc_topics 토픽의 분포 [(0, 0.4), (1, 0.3), (2, 0.2), (3, 0.1)] 첫번째 토픽에 40프로 분포
    doc_topics = best_model[corpus]
    find_best_source(doc_topics, id_list)

    #time checker
    end = time.time()
    print(best_model[corpus])
    print(f"{end - start:.5f} sec")

def visualization_topic(best_model, corpus, dictionary):
    vis = pyLDAvis.gensim.prepare(best_model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis, './lda.html')

def find_best_source(doc_topics, id_list):
    topic_to_pks_with_probs = defaultdict(list)
    for doc_index, topics in enumerate(doc_topics):
        for topic_id, prob in topics:
            topic_to_pks_with_probs[topic_id].append((id_list[doc_index], prob))
    # 각 토픽별로 확률이 높은 순으로 상위 5개의 문서 선택
    top_n = 5  # 상위 5개의 문서를 선택
    topic_top_articles = {}
    for topic_id, pk_prob_list in topic_to_pks_with_probs.items():
        # 확률 기준으로 정렬 (내림차순)
        sorted_pks_by_prob = sorted(pk_prob_list, key=lambda x: x[1], reverse=True)

        # 상위 5개의 문서 선택
        top_articles = sorted_pks_by_prob[:top_n]

        # 토픽별 상위 5개 문서의 PK 저장
        topic_top_articles[topic_id] = [pk for pk, prob in top_articles]
    for topic_id, top_pks in topic_top_articles.items():
        print(f"토픽 {topic_id}를 가장 잘 나타내는 문서들의 PK: {top_pks}")


if __name__ == '__main__':
  freeze_support()
  #update_bow(mysql_db)
  Process(target=get_all_bow(mysql_db)).start()
