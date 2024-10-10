import json

from ImageModifier.ImageArticleEditor import ImageGenerator
from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from multiprocessing import Process, freeze_support
from ArticleProcessor.ArticleTranslator import ArticleTranslator
from Db import f1Db

from tqdm import tqdm

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
        for i in range(1,5):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        date_range = topic_modeling_properties_json.get("topic_modeling_date_range")
        dynamic_topic_number_range = topic_modeling_properties_json.get("dynamic_topic_number_range")

        dynamic_topic_range = (dynamic_topic_number_range.get("start"), dynamic_topic_number_range.get("end"), dynamic_topic_number_range.get("step"))
        self.topic_modeling.run(date_range, dynamic_topic_range)

    def make_img(self, translate_content, article_sequence, article_id, article_type):
        paragraph_list = translate_content.get("paragraph")
        recommend_title = translate_content.get("recommendTitle")
        click_bait_title = translate_content.get("clickBaitTitle")
        final_sentence = translate_content.get("finalSentence")
        text = ""
        for paragraph, content in paragraph_list.items():
            text = text + content + " "
        text += final_sentence
        image_list = database.get_images_by_article_id(article_id)
        image_path_list = []
        for image in image_list:
            image_path_list.append(image_generator_info.get("image_source_path") + image.get("image_name") + ".png")
        ######### 이미지 없는 경우 필터링 IndexError
        self.image_generator.create_title_image(image_path_list[0], recommend_title, click_bait_title, article_type, article_sequence)
        self.image_generator.create_main_content(text, image_path_list, article_type, article_sequence)

    def v1_one_article(self):
        #crawlinwg
        self.test_crawling()

        #get one
        result = self.database.get_one_article_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        #translator
        prompt_v1 = prompt_json.get("prompt_v1")
        key = key_json.get("open_ai_api_key")
        article_translator = ArticleTranslator(prompt_v1, key)

        sequence = result.get("sequence")
        original_content = result.get("original_content")
        article_type = result.get("article_type")
        article_id = result.get("article_id")
        translate_content_json = article_translator.translate_v1(original_content)
        translate_content = json.loads(translate_content_json)
        self.make_img(translate_content, sequence, article_id, article_type)
        
        #db translate_content 업데이트
        database.update_translate_content(sequence, translate_content_json)

    def v1_all_article(self):
        # crawling
        #self.test_crawling()

        # get all
        article_list = self.database.get_all_article_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        # translator
        prompt_v1 = prompt_json.get("prompt_v1")
        key = key_json.get("open_ai_api_key")
        article_translator = ArticleTranslator(prompt_v1, key)
        for article in tqdm(article_list):
            sequence = article.get("sequence")
            original_content = article.get("original_content")
            article_type = article.get("article_type")
            article_id = article.get("article_id")

            translate_content_json = article_translator.translate_v1(original_content)
            translate_content = json.loads(translate_content_json)
            database.update_translate_content(sequence, translate_content_json)
            self.make_img(translate_content, sequence, article_id, article_type)
            # db translate_content 업데이트

    def v1_one_article_sequence(self, sequence):

        # get one
        result = self.database.get_one_by_sequence(sequence)
        # translator

        sequence = result.get("sequence")
        original_content = result.get("original_content")
        article_type = result.get("article_type")
        article_id = result.get("article_id")
        translate_content_json = result.get("translate_content")
        translate_content = json.loads(translate_content_json)
        self.make_img(translate_content, sequence, article_id, article_type)

if __name__ == '__main__':
    freeze_support()
    database = f1Db.Database(mysql_db)
    main = F1Main(database)
    main.v1_all_article()
    #main.v1_one_article_sequence(512)

