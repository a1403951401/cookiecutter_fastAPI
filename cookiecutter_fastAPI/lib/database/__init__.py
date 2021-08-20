from abc import ABC
from contextvars import ContextVar
from functools import wraps
from typing import Optional

from loguru import logger
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as BaseAsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from cookiecutter_fastAPI.config import config

database_context_var = ContextVar('database', default=None)

engine = create_async_engine(
    config.DB_URL,
    echo=config.DB_ECHO,
    pool_size=5,
    max_overflow=20,
    pool_timeout=10,
    pool_recycle=1800
)
base = declarative_base()


class DataBase:
    """ 数据库 session
    将数据库 session 注入到协程上下文中
    """

    class AsyncSession(BaseAsyncSession, ABC):
        async def __aenter__(self) -> 'AsyncSession':
            database.session = self
            return self

    session_maker = sessionmaker(
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    @property
    def session(self) -> Optional[AsyncSession]:
        if database_context_var.get() is None:
            raise DisconnectionError('session not init')
        return database_context_var.get()

    @session.setter
    def session(self, s: AsyncSession):
        database_context_var.set(s)


database = DataBase()


def database_rollback(func) -> callable:
    """ 提交失败回滚装饰器 """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            await database.session.commit()
            return result
        except Exception as e:
            await database.session.rollback()
            logger.exception(e)
            raise e

    return wrapper
