import os
import sys
import pymysql
from datetime import datetime
from datetime import timedelta
from itertools import combinations
import json
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

class LoginInfo:
    def __init__(self, loginid, password, sequence):
        self.loginid = loginid
        self.password = password
        self.sequence = sequence

    def get_loginid(self):
        return self.loginid

    def get_password(self):
        return self.password

    def get_sequence(self):
        return self.sequence

class Article:
    def __init__(self,seq,article_id,original_title,original_content,href,article_type,published_at,collected_at):
        self.seq = seq
        self.article_id = article_id
        self.original_title = original_title
        self.original_content = original_content
        self.href = href
        self.article_type = article_type
        self.published_at = published_at
        self.collected_at = collected_at


class Database:
    def __init__(self, db_info, logger):
        try:
            self.type = db_info["type"]
            self.db = pymysql.connect(
                host=db_info['host'],
                user=db_info['id'],
                password=db_info['password'],
                db=db_info['db'],
                charset='utf8mb4',
            )
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
            self.logger = logger
        except Exception as e:
            self.logger.error(f"데이터베이스 연결 실패: {e}")
            raise

    def save_article_info(self, basic_article_info):
        query = f"""INSERT IGNORE INTO article (article_id, original_title, original_content, href, article_type, published_at, collected_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        values = (basic_article_info.article_id, basic_article_info.original_title, basic_article_info.original_content, basic_article_info.href, basic_article_info.article_type, basic_article_info.published_at, datetime.now().strftime("%y-%m-%d %H:%M:S"))
        self.cursor.execute(query, values)
        self.commit()

    def save_image_info(self, article_id, img_source, img_name, image_description):
        query = f"""INSERT IGNORE INTO image (image_source, image_name, image_description, article_sequence) VALUES (%s, %s, %s, (SELECT sequence FROM article WHERE article_id = %s))"""
        values = (img_source, img_name, image_description, article_id)
        self.cursor.execute(query, values)
        self.commit()

    def update_image_created(self, sequence):
        update_query = f"update article set image_created = true where sequence = (%s)"
        self.cursor.execute(update_query, sequence)
        self.commit()

    def get_one_article_by_date_range(self, date_range):
        now = datetime.now()
        start_date = now - timedelta(days=date_range - 1)
        end_date = now + timedelta(days=1)
        get_one_article_query = "select sequence, article_id, original_title, original_content, article_type from article where published_at between Date(%s) and Date(%s) and translate_content is null order by sequence desc"
        values = (start_date, end_date)
        return self.fetch_one(get_one_article_query, values)

    def get_all_article_by_date_range(self, date_range):
        now = datetime.now()
        start_date = now - timedelta(days=date_range - 1)
        end_date = now + timedelta(days=1)
        get_one_article_query = "select sequence, article_id, original_title, original_content, article_type from article where published_at between Date(%s) and Date(%s) and translate_content is null order by sequence desc "
        values = (start_date, end_date)
        return self.fetch_all(get_one_article_query, values)

    def get_all_article_image_not_created(self, date_range):
        now = datetime.now()
        start_date = now - timedelta(days=date_range - 1)
        end_date = now + timedelta(days=1)
        get_one_article_query = "select sequence, article_id, translate_content from article where published_at between Date(%s) and Date(%s) and translate_content is not null and image_created = false order by sequence desc "
        values = (start_date, end_date)
        return self.fetch_all(get_one_article_query, values)

    def get_images_by_article_sequence(self, sequence):
        select_query = "select image_name, image_description from image where article_sequence = (%s)"
        return self.fetch_all(select_query, sequence)
    
    # 키워드 하나만 포함된 이미지
    def get_images_by_keyword_list(self, keyword_list):
        sub_query = " OR ".join(["lower(image_name) LIKE %s"] * len(keyword_list))
        query = f"select * from image where {sub_query} limit 5"
        params = [f"%{keyword}%" for keyword in keyword_list]
        return self.fetch_all(query, params)

    # 키워드 2개 포함된 이미지 조합 생성
    def get_pair_images_by_keyword_list(self, keyword_list):
        keyword_pairs = list(combinations(keyword_list, 2))
        sub_queries = []
        params = []
        for pair in keyword_pairs:
            sub_queries.append("(lower(image_name) LIKE %s AND lower(image_name) LIKE %s)")
            params.extend([f"%{pair[0]}%", f"%{pair[1]}%"])
        query = f"select * from image where {' OR '.join(sub_queries)} limit 5"
        return self.fetch_all(query, params)

    def update_translate_content(self, sequence, translate_content):
        update_query = "update article set translate_content = (%s) where sequence = (%s)"
        values = (json.dumps(translate_content), sequence)
        self.cursor.execute(update_query, values)
        self.commit()

    def get_one_by_sequence(self, sequence):
        select_query = "select sequence, article_id, original_title, original_content, article_type, translate_content from article where sequence = (%s)"
        return self.fetch_one(select_query, sequence)

    def get_title_by_sequence(self, sequence):
        select_query = "select translate_content from article where sequence = (%s)"
        translate_content_str = self.fetch_one(select_query, sequence)["translate_content"]
        translate_content = json.loads(translate_content_str)
        return translate_content.get("attentionGrabbingTitle")

    def get_title_sequence_list(self, date_str):
        select_query = "select sequence, translate_content from article where Date(collected_at) = (%s) and translate_content is not null"
        find_all = self.fetch_all(select_query, date_str)
        sequence_title = [{"sequence":find.get("sequence"), "title":json.loads(find.get("translate_content")).get("attentionGrabbingTitle")} for find in find_all]
        return sequence_title

    def fetch_all(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def fetch_one(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
