import pymysql
from functools import wraps
import time

def handle_operational_error(logger, max_retries=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except pymysql.err.OperationalError as e:
                    retries += 1
                    logger.warning(f"OperationalError 발생: {e}. 재시도 중... ({retries}/{max_retries})")
                    time.sleep(delay)
                    self.connect()
                except Exception as e:
                    logger.error(f"예상치 못한 에러 발생: {e}")
                    raise
            logger.error(f"최대 재시도 횟수를 초과하여 실패: {func.__name__}")
            raise pymysql.err.OperationalError(f"최대 재시도 횟수를 초과하여 {func.__name__} 작업 실패.")
        return wrapper
    return decorator