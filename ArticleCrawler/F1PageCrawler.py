import requests as re
from bs4 import BeautifulSoup
import re as regex
import f1Db
import json

mainPageUrl = "https://www.formula1.com/en/latest/all?articleFilters=&page="

class BasicArticleInfo:
    def __init__(self, uuid, href, article_type, original_title):
        self.uuid = uuid
        self.href = href
        self.original_title = original_title
        self.article_type = article_type
        self.original_content = None

    def add_article_content(self, original_content):
        self.original_content = original_content


def main_page(page_num):
    target_url = mainPageUrl + str(page_num)
    main_page_html = re.get(target_url).text
    bs4_page = BeautifulSoup(main_page_html, 'html.parser')
    article_list = bs4_page.find("ul", {"id": "article-list"})
    basic_article_info_list = extract_basic_article_info(article_list)
    extract_article_content(basic_article_info_list)
    execute_basic_article_list(basic_article_info_list)

# 기본 href, 기사 타입, 제목 추출 반환
def extract_basic_article_info(article_list):
    article_info_list = []
    for article in article_list:
        href = article.find("a")['href']
        article_type = article.find("a").find("figcaption").find("span").text
        article_title = article.find("a").find("figcaption").find("p").text
        pattern = r'\.([^.]+)$'
        match = regex.search(pattern, href)
        if match:
            uuid = match.group(1)
        else:
            uuid = None
        article_info_list.append(BasicArticleInfo(uuid, href, article_type, article_title))
    return article_info_list


def extract_article_content(basic_article_info_list):
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
            # 기사의 사진 저장 하기
            for photo in photo_list:
                img_source = photo.find("img")['src']
                img_name = photo.find("img")['alt']
                description = photo.find("figcaption").text
                download_photo(basic_article_info.uuid, img_source, img_name, description)

def download_photo(uuid, img_source, img_name, description):
    # 사진 저장하는 코드 여기에
    pass

def execute_basic_article_list(basic_article_info_list):
    # mysql 기본 데이터 저장하기
    with open('db_info.json', 'r') as file:
        db_info_json = json.load(file)
    database = f1Db.Database(db_info_json)
    database.execute_basic_article_list(basic_article_info_list)



main_page(1)
