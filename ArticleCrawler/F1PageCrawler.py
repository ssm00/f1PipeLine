import requests as re
from bs4 import BeautifulSoup
import pymysql
import re as regex


mainPageUrl = "https://www.formula1.com/en/latest/all?articleFilters=&page="

class BasicArticleInfo:
    def __init__(self, href, article_type, article_title, uuid):
        self.href = href
        self.article_type = article_type
        self.article_title = article_title
        self.uuid = uuid


def main_page(page_num):
    target_url = mainPageUrl + str(page_num)
    main_page_html = re.get(target_url).text
    bs4_page = BeautifulSoup(main_page_html, 'html.parser')
    article_list = bs4_page.find("ul", {"id": "article-list"})
    basic_article_info_list = extract_basic_article_info(article_list)
    extract_article_content(basic_article_info_list)


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
        article_info_list.append(BasicArticleInfo(href, article_type, article_title, uuid))
    return article_info_list


def extract_article_content(basic_article_info_list):
    for basic_article_info in basic_article_info_list:
        if basic_article_info.article_type == "News" or basic_article_info.article_type == "Technical" or basic_article_info.article_type == "Feature":
            article_request = re.get(basic_article_info.href).text
            article = BeautifulSoup(article_request, 'html.parser')
            article_content_cluster = article.select('article.col-span-6')
            print(article_content_cluster)

main_page(1)
