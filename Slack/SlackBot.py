import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from MyMetaData.metadata import MetaData
from Db import SlackDb
from instagram.instagram_uploader import InstagramUploader
from util.logger import LogManager, LogType
import json

class SlackBot:
    def __init__(self, account_info, instagram_uploader, database, logger):
        self.app = App(token=account_info.get('slack').get("slack_bot_token"))
        self.slack_client = WebClient(token=account_info.get('slack').get("slack_bot_token"))
        self.socket_handler = SocketModeHandler(self.app,account_info.get('slack').get("socket_mode_token"))
        self.instagram_uploader = instagram_uploader
        self.database = database
        self.logger = logger
        self.instagram_upload_channel_id = account_info.get('slack').get("instagram_upload_channel_id")
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.event("app_mention")
        def handle_mention(event, say):
            if "upload" in event["text"].lower():
                say("인스타그램 업로드를 시작합니다")
                self.send_date_select()

        @self.app.action("select_date")
        def handle_date_selection(ack, body):
            ack()
            selected_date = body["actions"][0]["selected_date"]
            title_sequence_list = self.database.get_title_sequence_list(selected_date)
            if title_sequence_list:
                self.send_sequence_select(selected_date, title_sequence_list)
            else:
                self.slack_client.chat_postMessage(
                    channel=self.instagram_upload_channel_id,
                    text=f"{selected_date}에 해당하는 sequence가 없습니다."
                )

        @self.app.action("select_sequence")
        def handle_selection(ack, body):
            ack()
            value_str = body["actions"][0]["selected_option"]["value"]
            value = json.loads(value_str)
            sequence = value.get("sequence")
            title = value.get("title")
            date = value.get("date")
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Sequence {sequence}를 선택하셨습니다. 업로드하시겠습니까?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "업로드"
                            },
                            "style": "primary",
                            "value": f"""{{"title":"{title}", "sequence" : "{str(sequence)}", "date":"{date}"}}""",
                            "action_id": "confirm_upload"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "취소"
                            },
                            "style": "danger",
                            "action_id": "cancel_upload"
                        }
                    ]
                }
            ]

            self.slack_client.chat_postMessage(
                channel=body["channel"]["id"],
                blocks=blocks,
                text=f"Sequence {sequence} 업로드 확인"
            )

        @self.app.action("confirm_upload")
        def handle_upload(ack, body):
            ack()
            value_str = body["actions"][0]["value"]
            value = json.loads(value_str)
            sequence = value.get("sequence")
            title = value.get("title")
            date = value.get("date")
            post_id = self.instagram_uploader.publish_post_from_s3(sequence, date, title)
            if post_id is not None:
                self.slack_client.chat_postMessage(channel=self.instagram_upload_channel_id, text=f"{sequence} 포스팅 성공")
            else:
                self.slack_client.chat_postMessage(channel=self.instagram_upload_channel_id, text=f"{sequence} 포스팅 실패")
        @self.app.action("cancel_upload")
        def handle_cancel(ack, body):
            ack()
            self.slack_client.chat_postMessage(
                channel=body["channel"]["id"],
                text="업로드가 취소되었습니다."
            )

    def send_date_select(self):
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "날짜 선택"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "datepicker",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "날짜선택"
                            },
                            "action_id": "select_date"
                        }
                    ]
                }
            ]
            self.slack_client.chat_postMessage(channel=self.instagram_upload_channel_id, blocks=blocks, text="날짜 선택")
        except Exception as e:
            self.logger.info(f"날짜 선택 에러: {e}")

    def send_sequence_select(self, selected_date, title_sequence_list):
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "인스타그램에 업로드할 sequence를 선택하세요:"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Sequence 선택"
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"Sequence : {title_sequence.get('sequence')},  {title_sequence.get('title')}"
                                    },
                                    "value": f"""{{"title":"{title_sequence.get('title')}", "sequence":"{str(title_sequence.get('sequence'))}", "date":"{selected_date}"}}"""
                                } for title_sequence in title_sequence_list
                            ],
                            "action_id": "select_sequence"
                        }
                    ]
                }
            ]
            self.slack_client.chat_postMessage(channel=self.instagram_upload_channel_id, blocks=blocks,text="인스타그램 업로드 sequence 선택")
        except Exception as e:
            self.logger.info(f"슬랙 인스타 업로드 시퀀스 선택 에러: {e}")

    def start(self):
        self.socket_handler.start()

    def stop(self):
        self.socket_handler.close()

def start_slack_bot(logger):
    meta_data = MetaData(config_dir="../MyMetaData")
    slack_db = SlackDb.Database(meta_data.db_info.get("mysql"), logger)
    instagram_uploader = InstagramUploader(meta_data.account_info, logger)
    slack_bot = SlackBot(meta_data.account_info, instagram_uploader, slack_db, logger)
    slack_bot.start()
    return slack_bot

def main():
    try:
        log_manager = LogManager("./logs")
        logger = log_manager.get_logger("main", LogType.SLACK_BOT)
        slack_bot = start_slack_bot(logger)
        logger.info("SLACK BOT 실행")
    except (KeyboardInterrupt, SystemExit):
        logger.info("SLACK BOT 종료")
    except Exception as e:
        logger.info(e)
        logger.info("SLACK BOT 에러발생 종료")
    finally:
        slack_bot.stop()

if __name__ == "__main__":
    main()