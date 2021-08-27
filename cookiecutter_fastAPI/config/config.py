#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from fastapi import HTTPException as FHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseSettings
from starlette.exceptions import HTTPException as SHTTPException

from cookiecutter_fastAPI.lib.json import dumps
from cookiecutter_fastAPI.models.base.base_error import AccessTokenExpire


class Config(BaseSettings):
    DEBUG: bool = True
    DB_ECHO: bool = False
    ENVIRONMENTS: str = "base"
    PROJECT_NAME: str = 'cookiecutter_fastAPI'
    PACKAGE: str = __package__.split('.')[0]
    PROJECT_PATH: Path = Path(__file__).parent.parent.resolve()
    RELEASE: str
    TAG: str
    # 默认的视图载入路径，使用支持逗号分割 [xxx/xxx, xxx/xxx]
    VIEW_PATH = 'api/views'
    # 默认的task载入路径，使用支持逗号分割 [xxx/xxx, xxx/xxx]
    TASK_PATH = 'worker/task'

    # database
    DB_HOST: str = 'postgres'
    DB_PORT: int = 5432
    DB_USERNAME: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_TABLE: str = 'cookiecutter_fastAPI'
    DB_URL: str
    DB_COMMIT: int = 100

    # redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = None
    REDIS_SOCKET_TIMEOUT: str = None

    # rabbitmq
    RABBIT_MQ_HOST: str = 'rabbit_mq'
    RABBIT_MQ_PORT: int = 5672
    RABBIT_MQ_USERNAME: str = 'rabbitmq'
    RABBIT_MQ_PASSWORD: str = 'rabbitmq'
    RABBIT_MQ_VHOST: str = ''

    # 最大任务池大小
    POOL_SIZE: int = 10

    # 异常处理
    LOG_PASS_EXCEPTION = (AccessTokenExpire)
    EXCEPTION_LOG_HANDLER = [Exception, FHTTPException, SHTTPException, RequestValidationError]

    class Config:
        json_dumps = dumps
        extra = 'allow'

    def get(self, item, default=None) -> Any:
        return getattr(self, item, default)

    def __setitem__(self, key, value) -> None:
        return self.__poertysetattr__(key, value)

    def __getitem__(self, item) -> Any:
        return getattr(self, item)

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://" \
               f"{quote_plus(self.DB_USERNAME)}:{quote_plus(self.DB_PASSWORD)}@" \
               f"{quote_plus(self.DB_HOST)}:{quote_plus(str(self.DB_PORT))}/" \
               f"{quote_plus(str(self.DB_TABLE))}"

    @property
    def SQLALCHEMY_URL(self) -> str:
        return f"postgresql+psycopg2://" \
               f"{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/" \
               f"{self.DB_TABLE}"

    @property
    def RABBIT_MQ_URL(self) -> str:
        return f'amqp://{self.RABBIT_MQ_USERNAME}:{self.RABBIT_MQ_PASSWORD}@' \
               f'{self.RABBIT_MQ_HOST}:{self.RABBIT_MQ_PORT}/' \
               f'{self.RABBIT_MQ_VHOST}'

    @property
    def CELERY_SQLALCHEMY_URL(self):
        return f'db+postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@' \
               f'{self.DB_HOST}:{self.DB_PORT}/' \
               f'{self.DB_TABLE}'

    @property
    def RELEASE(self) -> str:
        release_file = self.PROJECT_PATH.parent.resolve().joinpath('RELEASE')
        if release_file.is_file():
            with open(release_file, 'r') as f:
                return f.read()
        return "1.0.0"
