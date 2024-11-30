import pymysql
import json

class Database:
    def __init__(self, db_info, logger):
        self.db_info = db_info
        self.logger = logger
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.db = pymysql.connect(
                host=self.db_info['host'],
                user=self.db_info['id'],
                password=self.db_info['password'],
                db=self.db_info['db'],
                charset='utf8mb4',
            )
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
            self.logger.info("데이터베이스 연결 성공")
        except Exception as e:
            self.logger.error(f"데이터베이스 연결 실패: {e}")
            raise

    def ping(self):
        try:
            self.db.ping(reconnect = True)
            self.logger.info("Slack db 연결 해제 재연결 완료")
        except Exception as e:
            self.logger.info("Slack db Ping reconnection 에러")

    def get_title_sequence_list(self, date_str):
        select_query = "select sequence, translate_content from article where Date(image_created_at) = (%s)"
        find_all = self.fetch_all(select_query, date_str)
        sequence_title = [{"sequence": find.get("sequence"),
                           "title": json.loads(find.get("translate_content")).get("attentionGrabbingTitle")} for find in
                          find_all]
        return sequence_title

    def fetch_all(self, query, args=None):
        self.ping()
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def fetch_one(self, query, args=None):
        self.ping()
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
