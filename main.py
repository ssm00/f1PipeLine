import json

from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from multiprocessing import Process, freeze_support
from datetime import datetime
from datetime import timedelta
from ArticleProcessor.ArticleTranslator import ArticleTranslator
from Db import f1Db
from ImageModifier.ImageArticleEditor import ImageGenerator

with open('./MyMetaData/db_info.json', 'r') as file:
    db_info_json = json.load(file)
    mysql_db = db_info_json.get('article_data_source')
with open('MyMetaData/crawler_properties.json', 'r') as file:
    crawler_properties_json = json.load(file)
with open('./MyMetaData/topic_modeling_properties.json', 'r') as file:
    topic_modeling_properties_json = json.load(file)
with open('./MyMetaData/f1_name_list.json', 'r') as file:
    f1_name_list_json = json.load(file)
with open('./MyMetaData/key.json', 'r') as file:
    key_json = json.load(file)
with open('./MyMetaData/prompt.json', encoding="utf-8") as file:
    prompt_json = json.load(file)
with open('./MyMetaData/image_generator_info.json',"r") as file:
    image_generator_info = json.load(file)

class F1Main:

    def __init__(self, database):
        self.f1_crawler = F1PageCrawler(database, crawler_properties_json.get("download_prefix_path"))
        self.topic_modeling = TopicModeling(database, f1_name_list_json.get("people"), topic_modeling_properties_json.get("visualization_output_path"))
        self.image_generator = ImageGenerator(image_generator_info)
        self.database = database

    def test_crawling(self):

        for i in range(1,3):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        date_range = topic_modeling_properties_json.get("topic_modeling_date_range")
        dynamic_topic_number_range = topic_modeling_properties_json.get("dynamic_topic_number_range")

        dynamic_topic_range = (dynamic_topic_number_range.get("start"), dynamic_topic_number_range.get("end"), dynamic_topic_number_range.get("step"))
        self.topic_modeling.run(date_range, dynamic_topic_range)


    def v1_one_article(self):
        database = f1Db.Database(mysql_db)

        #crawlinwg
        #self.test_crawling()

        #get one
        result = database.get_one_article(crawler_properties_json.get("total_crawling_date_from_today"))
        #translator
        prompt_v1 = prompt_json.get("prompt_v1")
        key = key_json.get("open_ai_api_key")
        article_translator = ArticleTranslator(prompt_v1, key)

        sequence = result.get("sequence")
        original_title = result.get("original_title")
        original_content = result.get("original_content")
        article_type = result.get("article_type")
        article_id = result.get("article_id")
        translated_content_json = article_translator.translate_v1(original_content)
        translated_content = json.loads(translated_content_json)
        recommend_title = translated_content.get("recommendTitle")
        print(translated_content)
        database.update_translate_content(sequence, translated_content_json)

    def make_img(self):
        database = f1Db.Database(mysql_db)
        article = database.get_translate_content(478)
        translate_content = json.loads(article.get("translate_content"))
        paragraph_list = translate_content.get("paragraph")
        text = ""
        for paragraph, content in paragraph_list.items():
            text += content + "\n"
        image_list = database.get_images_by_article_id("4xrZ1DlFphcguA6lmabrIE")
        image_path_list = []
        for image in image_list:
            image_path_list.append(image_generator_info.get("image_source_path") + image.get("image_name") + ".png")
        self.image_generator.create_main_content(text, image_path_list, "Information", 478)
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
    database = f1Db.Database(mysql_db)
    main = F1Main(database)
    #main.v1_one_article()
    main.make_img()

