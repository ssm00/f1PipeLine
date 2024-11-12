import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from multiprocessing import Process, freeze_support
from apscheduler.triggers.date import DateTrigger
from Db import jobDb, f1Db
from MyMetaData.metadata import MetaData
from main import F1Main
from util.logger import LogManager, LogType
import traceback
from instagram.instagram_uploader import InstagramUploader
from Slack.SlackClient import SlackBot

class JobExecutor:

    def __init__(self, meta_data, log_manager):
        self.meta_data = meta_data
        self.log_manager = log_manager
        self.logger = log_manager.get_logger("job_executor", LogType.BATCH)
        self.job_db = None

    def creat_job_db(self):
        return jobDb.Database(self.meta_data.db_info.get("mysql"), self.logger)

    def stop_running_jobs(self):
        try:
            if not self.job_db:
                self.job_db = self.creat_job_db()
            running_jobs = self.job_db.get_all_running_job()
            end_time = datetime.now()
            for job in running_jobs:
                duration = (end_time - job.get("start_time")).total_seconds()
                formatted_duration = self.format_duration(duration)
                self.job_db.stop_job(job.get("id"), end_time, duration, formatted_duration)
        except Exception as e:
            self.logger.error(f"실행 중인 작업 상태 업데이트 실패: {str(e)} {traceback.format_exc()}")
        finally:
            if self.job_db:
                self.job_db.close()

    def format_duration(self, duration_seconds):
        if duration_seconds is None:
            return "알 수 없음"
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = duration_seconds % 60
        parts = []
        if hours > 0:
            parts.append(f"{hours}시간")
        if minutes > 0:
            parts.append(f"{minutes}분")
        if seconds > 0 or not parts:
            parts.append(f"{seconds:.3f}초")
        return " ".join(parts)

    def execute_f1_daily_work(self):
        start_time = datetime.now()
        self.job_db = self.creat_job_db()
        try:
            job_id = self.job_db.create_job("F1 일일 기사 생성")
            f1_log = self.log_manager.get_logger("f1_program", LogType.PROGRAM)
            f1_db = f1Db.Database(self.meta_data.db_info.get("mysql"), f1_log)
            try:
                f1_main = F1Main(f1_db, self.meta_data, f1_log)
                f1_main.daily_work()
                status = 'SUCCESS'
                error_msg = None
            except Exception as e:
                status = 'FAILED'
                error_msg = str(e)
                raise
            finally:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                formatted_duration = self.format_duration(duration)
                self.job_db.update_job_status(job_id, status, duration, formatted_duration, end_time, error_msg)
                f1_db.close()

        except Exception as e:
            self.logger.error(f"F1 크롤링 작업 실패: {str(e)}")
            raise
        finally:
            if self.job_db:
                self.job_db.close()


class Scheduler:

    def __init__(self, meta_data):
        self.meta_data = meta_data
        self.log_manager = LogManager("./logs")
        self.logger = self.log_manager.get_logger("scheduler", LogType.BATCH)
        self.job_executor = JobExecutor(meta_data, self.log_manager)
        self.scheduler = self._init_scheduler()

    def _init_scheduler(self):
        scheduler_info = self.meta_data.scheduler_info

        jobstores = {
            'default': SQLAlchemyJobStore(url=scheduler_info.get("job_store_url"))
        }

        executors = {
            'default': ThreadPoolExecutor(scheduler_info.get("max_threads")),
            'processpool': ProcessPoolExecutor(scheduler_info.get("max_processes"))
        }

        scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            timezone='Asia/Seoul'
        )

        return scheduler

    def add_jobs(self):
        self.scheduler.add_job(
            self.job_executor.execute_f1_daily_work,
            trigger=CronTrigger(**self.meta_data.scheduler_info['jobs']['daily_f1_work']['schedule']),
            #trigger=DateTrigger(run_date=datetime.now()),
            id='f1_daily_job',
            name='F1_daily_create_article',
            replace_existing=True,
        )

    def start(self):
        try:
            self.add_jobs()
            self.scheduler.start()
            self.logger.info("스케줄러가 시작되었습니다.")
        except Exception as e:
            self.logger.error(f"스케줄러 시작 실패: {e}")
            raise

    def shutdown(self):
        self.job_executor.stop_running_jobs()
        self.scheduler.shutdown()
        self.logger.info("스케줄러가 종료되었습니다.")

def start_slack_bot(meta_data, logger):
    f1db = f1Db.Database(meta_data.db_info.get("mysql"), logger)
    instagram_uploader = InstagramUploader(meta_data.account_info, logger)
    slack_bot = SlackBot(meta_data.account_info, instagram_uploader, f1db, logger)
    slack_bot.start()
    return slack_bot

def main():
    try:
        print("start")
        log_manager = LogManager("./logs")
        logger = log_manager.get_logger("main", LogType.BATCH)
        meta_data = MetaData()

        # 스케줄러 스레드 시작
        scheduler = Scheduler(meta_data)
        scheduler_thread = threading.Thread(target=scheduler.start)
        scheduler_thread.start()

        # Slack 봇 스레드 시작
        slack_bot = start_slack_bot(meta_data, logger)

        # 메인 스레드를 통한 유지 관리 (대기)
        try:
            while scheduler_thread.is_alive():
                time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            slack_bot.stop()

    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {traceback.format_exc()}")


if __name__ == '__main__':
    freeze_support()
    main()
