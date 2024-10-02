import json

from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from multiprocessing import Process, freeze_support
from datetime import datetime
from datetime import timedelta
from ArticleProcessor.ArticleTranslator import ArticleTranslator
from Db import f1Db

with open('./MyMetaData/db_info.json', 'r') as file:
    db_info_json = json.load(file)
    mysql_db = db_info_json.get('article_data_source')
with open('MyMetaData/crawler_properties.json', 'r') as file:
    crawler_properties_json = json.load(file)
with open('./MyMetaData/topic_modeling_properties.json', 'r') as file:
    topic_modeling_properties_json = json.load(file)
with open('./MyMetaData/f1_name_list.json', 'r') as file:
    f1_name_list_json = json.load(file)
with open('../MyMetaData/key.json', 'r') as file:
    key_json = json.load(file)
with open('../MyMetaData/prompt.json', encoding="utf-8") as file:
    prompt_json = json.load(file)

class F1Main:

    def __init__(self, database):
        self.f1_crawler = F1PageCrawler(database, crawler_properties_json.get("download_prefix_path"))
        self.topic_modeling = TopicModeling(database, f1_name_list_json.get("people"), topic_modeling_properties_json.get("visualization_output_path"))
        self.database = database

    def test_crawling(self):

        for i in range(1,10):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        date_range = topic_modeling_properties_json.get("topic_modeling_date_range")
        dynamic_topic_number_range = topic_modeling_properties_json.get("dynamic_topic_number_range")

        dynamic_topic_range = (dynamic_topic_number_range.get("start"), dynamic_topic_number_range.get("end"), dynamic_topic_number_range.get("step"))
        self.topic_modeling.run(date_range, dynamic_topic_range)


    def v1(self):
        database = f1Db.Database(mysql_db)

        #crawlinwg
        self.test_crawling()

        #get one
        article = database.get_one_article(crawler_properties_json.get("total_crawling_date_from_today"))

        #translator
        prompt_v1 = prompt_json['prompt_v1']
        key = key_json['api_key']
        article_translator = ArticleTranslator(prompt_v1, key)


        article_translator.translate_v1(content)

        get_article_id =
        article_images =


    # def v2():
    #     test_crawling()
    #     date_range = crawler_properties_json.get("total_crawling_date_from_today")
    #     now = datetime.now()
    #     start_date = now - timedelta(days=date_range - 1)
    #     end_date = now + timedelta(days=1)
    #
    #     get_today_article = "select * from article where published_at between Date(%s) and Date(%s)"
    #     values = (start_date, end_date)
    #
    #     # translator
    #     prompt_v1 = prompt_json['prompt_v1']
    #     key = key_json['api_key']
    #     article_translator = ArticleTranslator(prompt_v1, key)
    #
    #     article_translator.translate_v1(content)
    #
    #     get_article_id =
    #     article_images =

if __name__ == '__main__':
    freeze_support()
    database = f1Db(mysql_db)
    main = F1Main(database)

#     f1_crawler = F1PageCrawler(mysql_db)
#     f1_crawler.start(1)
#     f1_crawler.start(2)
#     f1_crawler.start(3)
