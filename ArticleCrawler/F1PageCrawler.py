import requests as re
from bs4 import BeautifulSoup
import pymysql


mainPageUrl = "https://www.formula1.com/en/latest/all?articleFilters=&page="

class BasicArticleInfo:
    def __init__(self, href, article_type, article_title):
        self.href = href
        self.article_type = article_type
        self.article_title = article_title


def main_page(page_num):
    target_url = mainPageUrl + str(page_num)
    main_page_html = re.get(target_url).text
    bs4_page = BeautifulSoup(main_page_html, 'html.parser')
    article_list = bs4_page.find("ul", {"id": "article-list"})
    basic_article_info = extract_basic_article_info(article_list)

    

# 기본 href, 기사 타입, 제목 추출 반환
def extract_basic_article_info(article_list):
    article_info_list = []
    for article in article_list:
        href = article.find("a")['href']
        article_type = article.find("a").find("figcaption").find("span").text
        article_title = article.find("a").find("figcaption").find("p").text
        article_info_list.append(BasicArticleInfo(href, article_type, article_title))
    return article_info_list


main_page(1)
