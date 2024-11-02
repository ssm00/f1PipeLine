import json
from ImageModifier.ImageArticleEditor import ImageGenerator
from ArticleCrawler.F1PageCrawler import F1PageCrawler
from ArticleProcessor.Topic_modeling import TopicModeling
from ArticleProcessor.ArticleTranslator import ArticleTranslator
from util.commonException import CommonError
import traceback

from tqdm import tqdm


class F1Main:

    def __init__(self, database, logger, meta_data):
        self.database = database
        self.f1_crawler = F1PageCrawler(database, meta_data.crawler_properties)
        self.topic_modeling = TopicModeling(database, meta_data.topic_modeling_properties)
        self.image_generator = ImageGenerator(database, meta_data.image_generator_info)
        self.article_translator = ArticleTranslator(meta_data.prompt, meta_data.key)
        self.date_range = meta_data.crawler_properties.get("total_crawling_date_from_today")
        self.meta_data = meta_data
        self.logger = logger

    def run_crawling(self, count):
        for i in tqdm(range(1,count)):
            self.f1_crawler.run(i)

    def test_topic_modeling(self):
        self.topic_modeling.run()

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
        # 이미지는 id이용 혹은, 이미지 이름 기반 서치
        try:
            image_path_list = self.image_generator.get_image_path_list(article_id=article_id)
            self.image_generator.create_title_image(image_path_list[0], attention_grabbing_title, click_bait_title, article_type, article_sequence)
            self.image_generator.create_main_content(text, image_path_list, article_type, article_sequence)
        except CommonError as e:
            self.logger.info(e.to_dict())


    def v1_one_article_translate(self):
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
            self.logger.info(e.to_dict())

    def v1_all_article_translate(self):
        # get all
        article_list = self.database.get_all_article_by_date_range(self.date_range)
        # translator
        for article in tqdm(article_list):
            sequence = article.get("sequence")
            original_content = article.get("original_content")
            article_id = article.get("article_id")
            try:
                translate_content = self.article_translator.translate_v1(original_content)
                # db translate_content 업데이트
                self.database.update_translate_content(sequence, translate_content)
                self.make_img(translate_content, sequence)
                self.logger.info(f"seq : {sequence} 성공")
            except CommonError as e:
                self.logger.info(e.to_dict())

    def v1_article_translate_batch(self):
        # crawling
        #self.test_crawling()
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
                self.logger.info(e.to_dict())

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
        try:
            article_list = self.database.get_all_translate_content_today()
            for article in tqdm(article_list):
                sequence = article.get("sequence")
                article_id = article.get("article_id")
                translate_content = json.loads(article.get("translate_content"))
                self.make_img(translate_content, sequence, article_id)
                self.logger.info(f"seq : {sequence} 이미지 생성 성공")
        except Exception as e:
            traceback.format_exc()

