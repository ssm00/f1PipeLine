import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from typing import List, Optional, Dict
from io import BytesIO
import requests as re

class S3Manager:

    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = "f1pipelinebucket"

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

    def upload_image_url(self, upload_path, img_source, img_name, bucket_name):
        try:
            image_response = re.get(img_source)
            if image_response.status_code == 200:
                s3_key = f"{upload_path}/{img_name}.png"
                self.s3.upload_fileobj(
                    BytesIO(image_response.content),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': 'image/png'}
                )
                return f"s3://{bucket_name}/{s3_key}"
            else:
                print(f"URL 이미지 다운로드 실패. Status code: {image_response.status_code}")
                return None
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def get_images_by_date(self, date_str: str, user_id: Optional[str] = None) -> List[Dict]:
        """
        특정 날짜의 이미지 목록 조회

        Args:
            date_str (str): 조회할 날짜 (YYYY-MM-DD 형식)
            user_id (Optional[str]): 특정 사용자의 이미지만 조회할 경우 사용자 ID

        Returns:
            List[Dict]: 이미지 정보 리스트 [{key: str, last_modified: datetime, size: int}]
        """
        try:
            # 날짜 형식 변환 (YYYY-MM-DD -> YYYY/MM/DD)
            formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y/%m/%d')

            # 검색할 prefix 설정
            prefix = f"{formatted_date}/"
            if user_id:
                prefix = f"{formatted_date}/{user_id}/"

            # S3 객체 리스트 조회
            response = self.s3.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )

            if 'Contents' not in response:
                return []

            # 결과 가공
            images = [{
                'key': obj['Key'],
                'last_modified': obj['LastModified'],
                'size': obj['Size']
            } for obj in response['Contents']]

            return images

        except ClientError as e:
            print(f"S3 List Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []

    def get_image_url(self, key: str, expires_in: int = 3600) -> Optional[str]:
        """
        이미지 임시 URL 생성

        Args:
            key (str): S3 객체 키
            expires_in (int): URL 유효 시간(초)

        Returns:
            Optional[str]: 성공시 서명된 URL, 실패시 None
        """
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