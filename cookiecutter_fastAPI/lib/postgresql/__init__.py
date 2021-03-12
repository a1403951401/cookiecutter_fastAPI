from contextvars import ContextVar
from functools import wraps
from typing import Optional

from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as BaseAsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from cookiecutter_fastAPI.config import config
from cookiecutter_fastAPI.lib.log import logger


class AsyncSession(BaseAsyncSession):
    async def __aenter__(self) -> 'AsyncSession':
        postgresql.session = self
        return self


postgresql_context_var = ContextVar('postgresql', default=None)

engine = create_async_engine(
    config.DB_URL,
    echo=config.DB_ECHO,
    pool_size=5,
    max_overflow=20,
    pool_timeout=10,
    pool_recycle=1800
)
base = declarative_base()


class Postgresql:
    session_maker = sessionmaker(
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    @property
    def session(self) -> Optional[AsyncSession]:
        if postgresql_context_var.get() is None:
            raise DisconnectionError('session not init')
        return postgresql_context_var.get()

    @session.setter
    def session(self, s: AsyncSession):
        postgresql_context_var.set(s)


postgresql = Postgresql()


def database_rollback(func) -> callable:
    """ 提交失败回滚装饰器 """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            await postgresql.session.commit()
            return result
        except Exception as e:
            await postgresql.session.rollback()
            logger.exception(e)
            raise e

    return wrapper
