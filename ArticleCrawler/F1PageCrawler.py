import requests as re
from bs4 import BeautifulSoup
import re as regex
from Db import f1Db
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
        self.database = f1Db.Database(db_info)
        self.header = {
            '_scid': '2fec4d4c-acb5-4c9a-ab8d-0d7ef93ad926',
            '_cb': 'ByHKf7BTh2wJDUG93t',
            '_sfid_8374': '{"anonymousId":"ed7952e81c4262a0","consents":[]}',
            'talkative_ecs__eu__260c846d-7b81-400a-b5e7-e4c3ec819064__widget_is_controlled_fullscreen': '0',
            'talkative_ecs__eu__260c846d-7b81-400a-b5e7-e4c3ec819064__push_prompt_dismissed': '0',
            'consentUUID': '9550e568-2532-4304-941c-52c3597be36c_23_29_31_32',
            '_gcl_au': '1.1.290777826.1716859512',
            '_tt_enable_cookie': '1',
            '_ttp': 'NmoEoOb8ZZ31laGk0jtOndLno4M',
            '_sctr': '1|1716789600000',
            '_scid_r': '2fec4d4c-acb5-4c9a-ab8d-0d7ef93ad926',
            'minVersion': '{"experiment":1283684404,"minFlavor":"IA Fixmi-1.17.1.123.js100"}',
            '_abck': '8583570C0031FD835ECB70FEEEA8975D~0~YAAQfEq/zNPyAQmQAQAAi448DgxaosbrSKNh3FGFPnj7B4onNP731rbq+cpDSouSpJ7igJKVUNjT1E7/MA3CjrG+lIBfu30vt+De2u4leSCVgoP5/QTeDiu9ip/9kGBns3DyJwwAduL+eeqDlxFWTJpJYku22iwAQsxyHbPKxJ3EQ1L9Iqo304QAtpXjoiukZ33oieCMyM5xU5EnT+Entf7XNpQjdcvq+scjfskJ59w8su+EkVpijzBSRpH8NmrGfrESHmpjKGKlvhwkAx21xZ/ynrX3ujbTFi1sTPFp19o/PIynNXInkum4cISVvoIWYmAyuqZqgqrAIPe49ox80sZbD78qhhHV98GqIvHpypLyuHFhPUrV1S+MoBRKG1twBPFEoh8vH6x724XW/+SLTD9C0LQqq55NVGo=~-1~-1~-1',
            'bm_s': 'YAAQfEq/zNTyAQmQAQAAi448DgH8dAFcWYMRqo2Rtbhy5ZuewxOkX4w04d2/qdVdMr7dhPabzTJWUhMYnu9t9l0Ybc3haBSqgkHZM+kUvqT6trRSNINy4cjQNIguhMsuw9V4ZJv4pPXp5FxxbMCl1H8UgceeKhS9IBDrQCLPFMqEREbnt3nydRGOUeGrCby2baQaHruZ4lkCYVujEC/dvsiRkV6Py4p1ugjZ3nbj/IKwLpf+cTtam7EleDAqF9vrwvWJyhzpxqqpz/H1ZVXZC8D4yHOFTHwhRmamDQ8Q7EnJyesubpMJnoFS4rfA0TBmUzRdgM6zCC/Sk0a2v0S04g3a4iwP0IGj',
            'LeadSourceName': 'LOG OUT from https://www.formula1.com/en/latest/all',
            '_evga_95b0': '{"uuid":"ed7952e81c4262a0","puid":"4EEF7nQjdUPmlt3jNHES_RqrVy0yYivrbc22FE_67Iysl9C7Z5GaDgZPPpjeUjLTSe_GcbPW_sS2l1Ou1szUUH_GEGK0H-9vY3yfECviByZmSAuXxAm_8TGvEYtJIYhJzg5bGXIgZfRgi7U-4IRiMw","affinityId":"0kt"}',
            '_rdt_uuid': '1716079952278.47af6b7b-3c05-4867-aa02-ecddcfaacbc6',
            '_gid': 'GA1.2.522657492.1718496352',
            '_ga_VWRQD933RZ': 'GS1.1.1718496353.11.0.1718496353.0.0.0',
            '_ga': 'GA1.1.776790023.1716859514',
            '_chartbeat2': '.1691157556370.1718496353622.0110000000011001.C5MATnm0pA2BvqSg4CqLkX5DLSUKI.1',
            '_cb_svref': 'https://tatrck.com/9z7K3hGCLg',
            'minUnifiedSessionToken10': '{"sessionId":"a55fceb88a-719d5a0543-13d2343f1a-c3f7f9dcb3-1c1c89fd45","uid":"dae81ab49c-8ee80798da-e702743ce9-a448ad28cb-ecb9e4f6cc","__sidts__":1718496353657,"__uidts__":1718496353657}',
            'ecos.dt': '1718496354932',
            'consentDate': '2024-06-16T00:05:55.238Z',
            '_chartbeat4': 't=CB3Jj7DkELKNBdDn6_DkMKYFBN1-ee&E=1&x=0&c=0.03&y=1665&w=559',
            'isFirstRendering': 'true',
            'reese84': '3:F/8BDr4baq28vcRp/67/Gg==:FLAoGUf51pbTE9SnkP4ra+jRMDEFJEOnY52PyM9FF9uJ5WvTelC/OWHE6lGZr1twwocst4OPD68ed/NqhR5s4lt6cz2JuZOzuNZ8eIBZF0PhVdAzc/53zjlxpSlkUMinx3L2K03WmLe3N/bC4/VE2joc5guYBn4XVbd0U4fCO+CfXvUopeoJV1MUCUHnGMauZeoePITBiqJ0ryqPcxW7RvlpTwAlcgKXIgDRAkkV4m82WgperSEsw7y7CKYNrIqJ8kCUhRQOjM2trS5EnT4+y425CqNW0d/KphRY/XVpJ4w4B3kREIR/6oKp/uBvLKJIdc/LbLaSR22i84E4ltYEG/k0WyLpyDktEzlYxToarKKph1mkE9RnpLDWQMANuOMGhR6U5cLMiGMPBH5h8H8JtczkxFVQaRoUd28NE9gFrRyjevdv0lJXffjLTE6DflkWR6mgOGMHQK0mXVSiAVHXea3rmoLV2feZHX4c+ZFlGnryxB6HaDB+pzscodtB4ph8Rhp6im4c7ewnO+kCeGn15w==:ZMqef+4/ssku7muGiPaNzHq90KmfEBLteIWKwM6Je0Y=',
            'login': '{"event":"login","componentId":"component_login_page","actionType":"success"}',
            'login-session': '{"data":{"subscriptionToken":"eyJraWQiOiIxIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJFeHRlcm5hbEF1dGhvcml6YXRpb25zQ29udGV4dERhdGEiOiJLT1IiLCJTdWJzY3JpcHRpb25TdGF0dXMiOiJpbmFjdGl2ZSIsIlN1YnNjcmliZXJJZCI6IjE5NjMzOTkxNSIsIkZpcnN0TmFtZSI6IiIsImVudHMiOlt7ImNvdW50cnkiOiJLT1IiLCJlbnQiOiJSRUcifV0sIkxhc3ROYW1lIjoiIiwiZXhwIjoxNzE4ODQxOTk3LCJTZXNzaW9uSWQiOiJleUpoYkdjaU9pSm9kSFJ3T2k4dmQzZDNMbmN6TG05eVp5OHlNREF4THpBMEwzaHRiR1J6YVdjdGJXOXlaU05vYldGakxYTm9ZVEkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaWRTSTZJakV3TURFeElpd2ljMmtpT2lJMk1HRTVZV1E0TkMxbE9UTmtMVFE0TUdZdE9EQmtOaTFoWmpNM05EazBaakpsTWpJaUxDSm9kSFJ3T2k4dmMyTm9aVzFoY3k1NGJXeHpiMkZ3TG05eVp5OTNjeTh5TURBMUx6QTFMMmxrWlc1MGFYUjVMMk5zWVdsdGN5OXVZVzFsYVdSbGJuUnBabWxsY2lJNklqRTVOak16T1RreE5TSXNJbWxrSWpvaU1UQTBPR1JoT0RZdFlUbGtaaTAwTW1Vd0xUbGlPV1F0TTJZM1pESmlaVFZsT1dJeElpd2lkQ0k2SWpFaUxDSnNJam9pWlc0dFIwSWlMQ0prWXlJNklqTTJORFFpTENKaFpXUWlPaUl5TURJMExUQTJMVE13VkRBd09qQTJPak0yTGprek5Wb2lMQ0prZENJNklqRWlMQ0psWkNJNklqSXdNalF0TURjdE1UWlVNREE2TURZNk16WXVPVE0xV2lJc0ltTmxaQ0k2SWpJd01qUXRNRFl0TVRkVU1EQTZNRFk2TXpZdU9UTTFXaUlzSW1sd0lqb2lNall3TkRvelpEQTVPamc1TjJRNlpUVXdNRHBtTVRVeU9tUXdabUk2WTJGa01EbzNZVGRtSWl3aVl5STZJa05CVEVkQlVsa2lMQ0p6ZENJNklrRkNJaXdpY0dNaU9pSlVNbG9nTVVvMklpd2lZMjhpT2lKRFFVNGlMQ0p1WW1ZaU9qRTNNVGcwT1RZek9UWXNJbVY0Y0NJNk1UY3lNVEE0T0RNNU5pd2lhWE56SWpvaVlYTmpaVzVrYjI0dWRIWWlMQ0poZFdRaU9pSmhjMk5sYm1SdmJpNTBkaUo5LmlSTi1oSHBCWmttZXRkNGxpMTh1bkpzZ2VwcFoxb0U4Q2dPXzNqX2FhZG8iLCJpYXQiOjE3MTg0OTYzOTcsIlN1YnNjcmliZWRQcm9kdWN0IjoiIiwianRpIjoiMmVhNDI0ZjQtMzkwYS00NTU2LWJiMmMtZmUyMGIwYjE1NDM5IiwiaGFzaGVkU3Vic2NyaWJlcklkIjoicHF6V2NIdmRnVVg5ZjNTQUhhTlYzYzZzOHIxWW9xS2M0YnV1VjVyOXlDND0ifQ.uI9QkMOdes1YQ6On_UhAIOqp-E5WU08krwrK6F6A7L2SheSg1wcDAV13voV7rGfiYF3wv69ZdhOei-aTIwrVp8JmYzlvRS08HANpYhwATRtig833xTeSqrMYqbJs7D8mJQl2knshM1mShL7ntyQzri7J302uv1bef5Sr-7ssBs4QSaT6nKWenPOM0Wm157oQj5XqaplQ7IMe5vQ_WMUbjaIkWLZ2MOWQKubq_Lzn4J_nqs5G97TVe6USaqCSUQ6y14YKg32nuUhgVGbk6Sv_ibRGRljKa_Gu8Zu5wPc94qqQTtpdg74iTDK7Gpy2XXnlcF1amXyWn5OIAdjyyJqqvg"}}',
            'user-metadata': '{"subscriptionSource":"","userRegistrationLevel":"full","subscribedProduct":"","subscriptionExpiry":"99/99/9999"}'
        }

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
            print("START")
            print(basic_article_info.href)
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
                    if photo.find("figure") is not None:
                        img_source = photo.find("img")['src']
                        img_name = photo.find("img")['alt']
                        img_name = self.replace_invalid_chars(img_name)
                        img_name = self.replace_spaces_with_underscores(img_name)
                        image_description = photo.find("figcaption").text
                        self.img_download(img_source, img_name, "../download_image")
                    elif photo.find("div",{"class","f1-carousel__slide"}) is not None:
                        photo_slide = photo.find_all("div", {"class", "f1-carousel__slide"})
                        for photo_in_slide in photo_slide:
                            img_source = photo_in_slide.find("img")['src']
                            img_name = photo_in_slide.find("img")['alt']
                            img_name = self.replace_invalid_chars(img_name)
                            img_name = self.replace_spaces_with_underscores(img_name)
                            image_description = img_name
                            self.img_download(img_source, img_name, "../download_image")
                    self.database.save_article_image_info(basic_article_info.article_id, img_source, img_name, image_description)

    def replace_invalid_chars(self, name):
        # 윈도우에서 허용되지 않는 문자: \ / : * ? " < > |
        invalid_chars = r'[\\/*?:"<>|]'
        sanitized_filename = re.sub(invalid_chars, '', name)
        return sanitized_filename[:255]

    def replace_spaces_with_underscores(self, name):
        return regex.sub(r'\s+', '_', name)

    def img_download(self, img_source, img_name, save_path):
        response = re.get(img_source)
        if response.status_code == 200:
            file_name = f"{save_path}/{img_name}.png"
            print(file_name)
            with open(file_name, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")

    def start(self, page_num):
        target_url = mainPageUrl + str(page_num)
        main_page_html = re.get(target_url, headers=self.header).text
        bs4_page = BeautifulSoup(main_page_html, 'html.parser')
        article_list = bs4_page.find("ul", {"id": "article-list"})
        basic_article_info_list = self.extract_basic_article_info(article_list)
        self.extract_article_content(basic_article_info_list)

with open('../Db/db_info.json', 'r') as file:
    db_info_json = json.load(file)

mysql_db = db_info_json['article_data_source']
crawler = F1PageCrawler(mysql_db)

for i in range(10):
    crawler.start(i)
