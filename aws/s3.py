import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from io import BytesIO
import requests as re

class S3Manager:

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = "f1pipelinebucket"
        self.upload_path = "after_processing_image"


    def upload_image(self, image, upload_path, article_id, image_name):
        try:
            buffer = BytesIO()
            image.save(buffer, format('JPEG'))
            buffer.seek(0)
            today = datetime.now().strftime('%Y/%m/%d')
            key = f"{upload_path}/{today}/{article_id}/{image_name}"
            self.s3.upload_fileobj(
                buffer,
                self.bucket,
                key,
                ExtraArgs={
                    'ContentType': 'image/jpeg'
                }
            )
            return key
        except ClientError as e:
            print(f"S3 Upload Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None

    def upload_image_url(self, img_source, upload_path, img_name):
        try:
            image_response = re.get(img_source)
            if image_response.status_code == 200:
                s3_key = f"{upload_path}/{img_name}"
                self.s3.upload_fileobj(
                    BytesIO(image_response.content),
                    self.bucket,
                    s3_key,
                    ExtraArgs={'ContentType': 'image/jpeg'}
                )
                return s3_key
            else:
                print(f"URL 이미지 다운로드 실패. Status code: {image_response.status_code}")
                return None
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def get_all_today_image(self):
        try:
            today = datetime.now().strftime('%Y/%m/%d')
            prefix = f"{self.upload_path}/{today}/"
            response = self.s3.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix,
            )
            if 'Contents' not in response:
                return []

            image_list = {}
            for obj in response['Contents']:
                sequence = obj['Key'].split('/')[-2]
                file_name = obj['Key'].split('/')[-1]
                url = f"https://{self.bucket}.s3.amazonaws.com/{obj['Key']}"
                if sequence not in image_list:
                    image_list[sequence] = []
                image_list[sequence].append({
                    'name': file_name,
                    'url': url
                })
            return image_list
        except ClientError as e:
            print(f"S3 List Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []

    def get_image_url(self, key, expires_in = 3600):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': key
                },
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            print(f"URL Generation Error: {e}")
            return None

    def get_article_images(self, article_seq, date_str):
        try:
            formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y/%m/%d')
            prefix = f"{self.upload_path}/{formatted_date}/{article_seq}/"
            response = self.s3.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            if 'Contents' not in response:
                return []
            images = []
            for obj in response['Contents']:
                file_name = obj['Key'].split('/')[-1]
                url = f"https://{self.bucket}.s3.amazonaws.com/{obj['Key']}"
                images.append({
                    'name': file_name,
                    'url': url
                })
            images.sort(key=lambda x: x['name'])
            return images
        except ClientError as e:
            print(f"S3 List Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []