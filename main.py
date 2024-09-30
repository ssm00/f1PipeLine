import json

from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from multiprocessing import Process, freeze_support

with open('./MyMetaData/db_info.json', 'r') as file:
    db_info_json = json.load(file)
    mysql_db = db_info_json.get('article_data_source')
with open('MyMetaData/crawler_properties.json', 'r') as file:
    crawler_properties_json = json.load(file)
with open('./MyMetaData/topic_modeling_properties.json', 'r') as file:
    topic_modeling_properties_json = json.load(file)
with open('./MyMetaData/f1_name_list.json', 'r') as file:
    f1_name_list_json = json.load(file)

def test_crawling():
    f1_crawler = F1PageCrawler(mysql_db,"./download_image")
    for i in range(1,10):
        f1_crawler.run(i)

def test_topic_modeling():
    date_range = topic_modeling_properties_json.get("topic_modeling_date_range")
    dynamic_topic_number_range = topic_modeling_properties_json.get("dynamic_topic_number_range")
    visualization_output_path = topic_modeling_properties_json.get("visualization_output_path")
    dynamic_topic_range = (dynamic_topic_number_range.get("start"), dynamic_topic_number_range.get("end"), dynamic_topic_number_range.get("step"))
    f1_name_dict = f1_name_list_json.get("people")
    topic_modeling = TopicModeling(mysql_db, f1_name_dict, visualization_output_path)
    topic_modeling.run(date_range, dynamic_topic_range)


if __name__ == '__main__':
    freeze_support()
    #test_crawling()
    test_topic_modeling()

#     f1_crawler = F1PageCrawler(mysql_db)
#     f1_crawler.start(1)
#     f1_crawler.start(2)
#     f1_crawler.start(3)
