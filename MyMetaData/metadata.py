import json
from pathlib import Path

class MetaData:

    def __init__(self, config_dir='./MyMetaData'):
        self.image_generator_info = None
        self.prompt = None
        self.key = None
        self.topic_modeling_properties = None
        self.crawler_properties = None
        self.db_info = None
        self.scheduler_info = None
        self.account_info = None
        self.image_save_path = None
        self.config_dir = Path(config_dir)
        self.load_all_json()

    def load_json(self, file_name):
        file_path = self.config_dir / file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


    def load_all_json(self):
        self.db_info = self.load_json('db_info.json')
        self.crawler_properties = self.load_json('crawler_properties.json')
        self.topic_modeling_properties = self.load_json('topic_modeling_properties.json')
        self.key = self.load_json('key.json')
        self.prompt = self.load_json('prompt.json')
        self.image_generator_info = self.load_json('image_generator_info.json')
        self.scheduler_info = self.load_json('scheduler_info.json')
        self.account_info = self.load_json('account_info.json')
        self.image_save_path = self.load_json('image_save_path.json')

