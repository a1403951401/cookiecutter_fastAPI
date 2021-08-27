from celery import Celery

from cookiecutter_fastAPI.config import config

celery_app = Celery(
    config.PROJECT_NAME,
    broker=config.RABBIT_MQ_URL,
    backend=config.CELERY_SQLALCHEMY_URL,
)
