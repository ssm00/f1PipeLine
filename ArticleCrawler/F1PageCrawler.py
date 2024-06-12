import requests as re
from bs4 import BeautifulSoup
import re as regex
import f1Db
import json

mainPageUrl = "https://www.formula1.com/en/latest/all?articleFilters=&page="

class BasicArticleInfo:
    def __init__(self, article_id, href, article_type, original_title):
        self.article_id = article_id
        self.href = href
        self.original_title = original_title
        self.article_type = article_type
        self.original_content = None

    def add_article_content(self, original_content):
        self.original_content = original_content


class F1PageCrawler:

    def __init__(self, db_info):
        self.database = f1Db.Database(db_info_json['article_data_source'])

    def main_page_crawling(self, page_num):
        target_url = mainPageUrl + str(page_num)
        main_page_html = re.get(target_url).text
        bs4_page = BeautifulSoup(main_page_html, 'html.parser')
        article_list = bs4_page.find("ul", {"id": "article-list"})
        basic_article_info_list = self.extract_basic_article_info(article_list)
        self.extract_article_content(basic_article_info_list)

    # 기본 href, 기사 타입, 제목 추출 반환
    def extract_basic_article_info(self, article_list):
        article_info_list = []
        for article in article_list:
            href = article.find("a")['href']
            article_type = article.find("a").find("figcaption").find("span").text
            article_title = article.find("a").find("figcaption").find("p").text
            pattern = r'\.([^.]+)$'
            match = regex.search(pattern, href)
            if match:
                article_id = match.group(1)
            else:
                article_id = None
            article_info_list.append(BasicArticleInfo(article_id, href, article_type, article_title))
        return article_info_list


    def extract_article_content(self, basic_article_info_list):
        for basic_article_info in basic_article_info_list:
            if basic_article_info.article_type == "News" or basic_article_info.article_type == "Technical" or basic_article_info.article_type == "Feature":
                article_request = re.get(basic_article_info.href).text
                article = BeautifulSoup(article_request, 'html.parser')
                article_content_cluster = article.find('article',{"class":"col-span-6"})
                photo_list = article_content_cluster.find_all("div", {"class": "f1-breakout"})
                p_tag_list = article_content_cluster.find_all("p")
                content = ""
                # 아티클 중 p 태그
                for p in p_tag_list:
                    read_more = r'READ MORE'
                    if regex.search(read_more, p.text):
                        continue
                    content += p.text + '\n'
                basic_article_info.add_article_content(content)
                self.database.save_basic_article(basic_article_info)

                # 기사의 사진 저장 하기
                for photo in photo_list:
                    img_source = photo.find("img")['src']
                    img_name = photo.find("img")['alt']
                    image_description = photo.find("figcaption").text
                    self.database.save_article_image_info(basic_article_info.article_id, img_source, img_name, image_description)


with open('db_info.json', 'r') as file:
    db_info_json = json.load(file)

crawler = F1PageCrawler(db_info_json)
crawler.main_page_crawling(1)
