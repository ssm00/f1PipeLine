from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
from instagram.instagram_uploader import InstagramUploader
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

class SlackManager:

    def __init__(self, database, account_info, logger):
        self.database = database
        self.logger = logger
        self.instagram_upload_channel_id = account_info.get('slack').get("instagram_upload_channel_id")
        self.batch_channel_id = account_info.get('slack').get("batch_channel_id")
        #인스타그램 업로더
        self.instagram_uploader = InstagramUploader(account_info, logger)

        #일반 slack client
        self.slack_client = WebClient(token=account_info.get('slack').get("slack_bot_token"))

        #bot 멘션
        self.app = App(token=account_info.get('slack').get("slack_bot_token"))
        self.socket_mode_handler = SocketModeHandler(self.app, account_info.get('slack').get("socket_mode_token"))
        self.setup_handlers()

    def show_image_list(self, image_list):
        try:
            self.slack_client.chat_postMessage(
                channel=self.batch_channel_id,
                text=f"{datetime.now().strftime('%Y-%m-%d')}"
            )
            for sequence, images in image_list.items():
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Sequence: {sequence}*"
                        }
                    }
                ]
                for image in images:
                    blocks.extend([
                        {
                            "type": "image",
                            "image_url": image['url'],
                            "alt_text": image['name']
                        }
                    ])
                self.slack_client.chat_postMessage(
                    channel=self.batch_channel_id,
                    blocks=blocks,
                    text=f"Sequence {sequence} images"
                )
        except SlackApiError as e:
            self.logger.info(f"슬랙 이미지 보여 주기 에러: {e.response['error']}")

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
            self.slack_client.chat_postMessage(channel=self.instagram_upload_channel_id, blocks=blocks, text="인스타그램 업로드 sequence 선택")
        except Exception as e:
            self.logger.info(f"슬랙 인스타 업로드 시퀀스 선택 에러: {e}")

    def socket_mode_start(self):
        self.socket_mode_handler.start()

    def socket_mode_end(self):
        self.socket_mode_handler.close()

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
            value_str = body["actions"][0]["selected_option"]["value"]
            value = json.loads(value_str)
            sequence = value.get("sequence")
            title = value.get("title")
            date = value.get("date")
            self.instagram_uploader.publish_post_from_s3(sequence, date, title)


        @self.app.action("cancel_upload")
        def handle_cancel(ack, body):
            ack()
            self.slack_client.chat_postMessage(
                channel=body["channel"]["id"],
                text="업로드가 취소되었습니다."
            )