import os
import sys
import pymysql
import json
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


class Database:
    def __init__(self, db_info):
        self.type = db_info["type"]
        self.db = pymysql.connect(
            host=db_info['host'],
            user=db_info['id'],
            password=db_info['password'],
            db=db_info['db'],
            charset='utf8mb4',
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.table = db_info.get('table', "")

    def execute(self, query, args=None):
        self.cursor.execute(query, args)

    def save_basic_article(self, basic_article_info):
        query = f"""INSERT INTO {self.table} (article_id, original_title, original_content, href, article_type) VALUES (%s,%s,%s,%s,%s)"""
        values = (basic_article_info.article_id, basic_article_info.original_title, basic_article_info.original_content, basic_article_info.href, basic_article_info.article_type)
        self.cursor.execute(query, values)
        self.commit()

    def save_article_image_info(self, article_id, img_source, img_name, image_description):
        query = f"""INSERT INTO image (image_source, image_name, image_description, article_id) VALUES (%s,%s,%s,%s)"""
        values = (img_source, img_name, image_description, article_id)
        self.cursor.execute(query, values)
        self.commit()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
