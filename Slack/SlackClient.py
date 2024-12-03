from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

class SlackClient:

    def __init__(self, database, account_info, logger):
        self.database = database
        self.logger = logger
        self.account_info = account_info
        self.instagram_upload_channel_id = account_info.get('slack').get("instagram_upload_channel_id")
        self.batch_channel_id = account_info.get('slack').get("batch_channel_id")
        self.slack_client = WebClient(token=account_info.get('slack').get("slack_bot_token"))

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
