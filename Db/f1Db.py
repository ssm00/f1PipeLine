import os
import sys
import pymysql
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from datetime import datetime
from datetime import timedelta

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
        query = f"""INSERT IGNORE INTO {self.table} (article_id, original_title, original_content, href, article_type, published_at, collected_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        values = (basic_article_info.article_id, basic_article_info.original_title, basic_article_info.original_content, basic_article_info.href, basic_article_info.article_type, basic_article_info.published_at, datetime.now().strftime("%y-%m-%d %H:%M:S"))
        self.cursor.execute(query, values)
        self.commit()

    def save_article_image_info(self, article_id, img_source, img_name, image_description):
        query = f"""INSERT IGNORE INTO image (image_source, image_name, image_description, article_id) VALUES (%s,%s,%s,%s)"""
        values = (img_source, img_name, image_description, article_id)
        self.cursor.execute(query, values)
        self.commit()

    def get_one_article(self, date_range):
        now = datetime.now()
        start_date = now - timedelta(days=date_range - 1)
        end_date = now + timedelta(days=1)
        get_one_article_query = "select * from article where published_at between Date(%s) and Date(%s)"
        values = (start_date, end_date)
        return self.cursor.fetchone(get_one_article_query, values)

    def fetch_all(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
