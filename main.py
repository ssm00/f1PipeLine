import json
import threading

from ImageModifier.ImageArticleEditor import ImageGenerator
from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from ArticleProcessor.ArticleTranslator import ArticleTranslator
from util.commonException import CommonError
from MyMetaData.metadata import MetaData
from tqdm import tqdm
from Db import f1Db
from util import logger
from instagram.instagram_uploader import InstagramUploader
from Slack.SlackClient import SlackClient
from aws.s3 import S3Manager

class F1Main:

    def __init__(self, database, meta_data, logger):
        self.database = database
        self.logger = logger
        self.meta_data = meta_data
        self.s3 = S3Manager()
        self.f1_crawler = F1PageCrawler(database, meta_data.image_save_path, logger)
        self.topic_modeling = TopicModeling(database, meta_data.topic_modeling_properties)
        self.image_generator = ImageGenerator(database, meta_data.image_generator_info, meta_data.image_save_path, logger)
        self.instagram_uploader = InstagramUploader(meta_data.account_info, logger)
        self.article_translator = ArticleTranslator(meta_data.prompt, meta_data.key)
        self.slack_manager = SlackClient(database, meta_data.account_info, logger)
        self.date_range = meta_data.crawler_properties.get("total_crawling_date_from_today")

    def cleanup(self):
        if hasattr(self, 'database') and self.database:
            self.database.close()

    def run_crawling(self, count):
        for i in tqdm(range(1,count+1)):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        self.topic_modeling.run()

    def make_img(self, translate_content, article_sequence):
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
        # 이미지는 id이용 혹은, 이미지 이름 기반 서치
        try:
            image_path_list = self.image_generator.get_original_image_path_list(article_sequence=article_sequence)
            self.image_generator.create_title_image(image_path_list[0], attention_grabbing_title, click_bait_title, article_type, article_sequence)
            self.image_generator.create_main_content(text, image_path_list, article_type, article_sequence)
            self.database.update_image_created(article_sequence)
            self.logger.info(f"seq : {article_sequence} 이미지 생성 성공")
        except CommonError as e:
            self.logger.warning(e.to_dict())

    def _v1_one_article_translate(self):
        #get one
        result = self.database.get_one_article_by_date_range(self.date_range)
        #translator
        sequence = result.get("sequence")
        original_content = result.get("original_content")
        try:
            translate_content = self.article_translator.translate_v1(original_content)
            self.database.update_translate_content(sequence, translate_content)
            self.make_img(translate_content, sequence)
        except CommonError as e:
            self.logger.warning(e.to_dict())

    def v1_article_translate_batch(self):
        # get all
        article_list = self.database.get_all_article_by_date_range(self.date_range)
        # translator
        for article in tqdm(article_list):
            sequence = article.get("sequence")
            original_content = article.get("original_content")
            try:
                translate_content = self.article_translator.translate_v1(original_content)
                self.database.update_translate_content(sequence, translate_content)
                self.logger.info(f"seq : {sequence} 번역 기사 db저장 성공")
            except CommonError as e:
                self.logger.warning(e.to_dict())

    def _v1_make_one_img_by_sequence(self, sequence):
        # get one
        result = self.database.get_one_by_sequence(sequence)
        # translator
        sequence = result.get("sequence")
        translate_content_json = result.get("translate_content")
        translate_content = json.loads(translate_content_json)
        self.make_img(translate_content, sequence)

    def v1_make_img_batch(self):
        try:
            article_list = self.database.get_all_article_image_not_created(self.date_range)
            for article in tqdm(article_list):
                sequence = article.get("sequence")
                translate_content = json.loads(article.get("translate_content"))
                self.make_img(translate_content, sequence)
        except CommonError as e:
            self.logger.warning(e.to_dict())

    def show_all_image(self):
        try:
            image_list = self.s3.get_all_today_image()
            self.slack_manager.show_image_list(image_list)
            self.logger.info("slack 이미지 전송 완료")
        except Exception as e:
            self.logger.info(f"slack 이미지 전송 실패 메시지 {e}")


    def daily_work(self):
        self.run_crawling(5)
        self.v1_article_translate_batch()
        self.v1_make_img_batch()
        self.show_all_image()