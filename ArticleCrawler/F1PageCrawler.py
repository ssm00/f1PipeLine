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
            article_content_cluster = article.find('article',{"class":"col-span-6"})

            photo_list = article_content_cluster.find_all("div", {"class": "f1-breakout"})
            p_tag_list = article_content_cluster.find_all("p")
            print(basic_article_info.href)
            content = ""
            # 아티클 중 p 태그
            for p in p_tag_list:
                read_more = r'READ MORE'
                if regex.search(read_more, p.text):
                    continue
                content += p.text + '\n'
            for photo in photo_list:
                img_source = photo.find("img")['src']
                print(img_source)
                img_name = photo.find("img")['alt']
                print(img_name)
                description = photo.find("figcaption").text
                print(description)



main_page(1)
