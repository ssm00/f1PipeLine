import json

import anthropic

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
        self.article_translator = ArticleTranslator(prompt_json, key_json)
        self.database = database

    def run_crawling(self, count):
        for i in range(1,count):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        date_range = topic_modeling_properties_json.get("topic_modeling_date_range")
        dynamic_topic_number_range = topic_modeling_properties_json.get("dynamic_topic_number_range")

        dynamic_topic_range = (dynamic_topic_number_range.get("start"), dynamic_topic_number_range.get("end"), dynamic_topic_number_range.get("step"))
        self.topic_modeling.run(date_range, dynamic_topic_range)

    def make_img(self, translate_content, article_sequence, article_id):
        paragraph_list = translate_content.get("paragraph")
        attention_grabbing_title = translate_content.get("attentionGrabbingTitle")
        click_bait_title = translate_content.get("clickBaitTitle")
        final_sentence = translate_content.get("finalSentence")
        keyword_list = translate_content.get("properNouns")
        article_type = translate_content.get("articleType").get("type")
        text = ""
        for paragraph, content in paragraph_list.items():
            text = text + content + " "
        text += final_sentence
        ######### 이미지 없는 경우 필터링 IndexError
        #image_list = self.database.get_images_by_keyword_list(keyword_list)
        #image_list = self.database.get_pair_images_by_keyword_list(keyword_list)
        image_list = self.database.get_images_by_article_id(article_id)
        image_path_list = []
        for image in image_list:
            image_path_list.append(image_generator_info.get("image_source_path") + image.get("image_name") + ".png")
        try:
            self.image_generator.create_title_image(image_path_list[0], attention_grabbing_title, click_bait_title, article_type, article_sequence)
            self.image_generator.create_main_content(text, image_path_list, article_type, article_sequence)
        except IndexError:
            print(f"list : {image_list}, keyword = {keyword_list} 메인 컨텐츠 생성 적합한 이미지 없음")

    def v1_one_article_translate(self):
        #get one
        result = self.database.get_one_article_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        #translator
        sequence = result.get("sequence")
        original_content = result.get("original_content")
        try:
            translate_content_json = self.article_translator.translate_v1(original_content)
            translate_content = json.loads(translate_content_json)
            database.update_translate_content(sequence, translate_content_json)
            self.make_img(translate_content, sequence)
        except json.decoder.JSONDecodeError:
            print(f"GPT output json 잘못 생성함 seq : {sequence} 일단 넘어감 내용은 \n {translate_content}")

    def v1_all_article_translate(self):
        # get all
        article_list = self.database.get_all_article_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        # translator
        prompt_v1 = prompt_json.get("prompt_v1")
        key = key_json.get("open_ai_api_key")
        for article in tqdm(article_list):
            sequence = article.get("sequence")
            original_content = article.get("original_content")
            article_id = article.get("article_id")

            translate_content_json = self.article_translator.translate_v1(original_content)
            try:
                translate_content = json.loads(translate_content_json)
                # db translate_content 업데이트
                database.update_translate_content(sequence, translate_content_json)
                self.make_img(translate_content, sequence)
                print(f"seq : {sequence} 성공")
            except json.decoder.JSONDecodeError:
                print(f"GPT output json 잘못 생성함 seq : {sequence} 일단 넘어감 내용은 \n {translate_content}")

    def v1_article_translate_batch(self):
        # crawling
        #self.test_crawling()
        # get all
        article_list = self.database.get_all_article_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        # translator
        for article in tqdm(article_list):
            sequence = article.get("sequence")
            original_content = article.get("original_content")
            try:
                translate_content_json = self.article_translator.translate_v1(original_content)
                translate_content = json.loads(translate_content_json)
                # db translate_content 업데이트
                database.update_translate_content(sequence, translate_content_json)
                print(f"seq : {sequence} 번역 기사 db저장 성공")
            except json.decoder.JSONDecodeError:
                print(f"GPT output json 잘못 생성함 seq : {sequence} 일단 넘어감 내용은 \n {translate_content_json}")
            except anthropic.InternalServerError as err:
                if err.status_code == "529":
                    print("anthropic 서버 과부화 나중에 일단 넘어감 나중에 다시 시도")

    def v1_make_one_img_by_sequence(self, sequence):
        # get one
        result = self.database.get_one_by_sequence(sequence)
        # translator
        sequence = result.get("sequence")
        article_id = result.get("article_id")
        translate_content_json = result.get("translate_content")
        translate_content = json.loads(translate_content_json)
        self.make_img(translate_content, sequence, article_id)

    def v1_make_img_batch(self):
        article_list = self.database.get_all_translate_content_by_date_range(crawler_properties_json.get("total_crawling_date_from_today"))
        for article in tqdm(article_list):
            try:
                sequence = article.get("sequence")
                article_id = article.get("article_id")
                translate_content = json.loads(article.get("translate_content"))
                self.make_img(translate_content, sequence, article_id)
                print(f"seq : {sequence} 이미지 생성 성공")
            except json.decoder.JSONDecodeError:
                print(f"GPT output json 잘못 생성함 seq : {sequence} 일단 넘어감 내용은 \n {translate_content}")


if __name__ == '__main__':
    freeze_support()
    database = f1Db.Database(mysql_db)
    main = F1Main(database)
    #main.v1_all_article()
    #main.run_crawling(5)
    # main.v1_article_translate_batch()
    # main.v1_make_img_batch()
    main.v1_make_one_img_by_sequence(606)
    #main.test_output_text()
    #main.v1_one_article()

