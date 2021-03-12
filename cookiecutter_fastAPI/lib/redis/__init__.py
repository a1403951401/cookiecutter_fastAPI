from aioredis import create_redis_pool, Redis as BaseRedis

from cookiecutter_fastAPI.config import config


class Redis:
    _connection: BaseRedis

    async def init(self):
        self._connection = await create_redis_pool(
            (config.REDIS_HOST, config.REDIS_PORT),
            db=config.REDIS_DB,
            password=config.REDIS_PASSWORD,
            timeout=config.REDIS_SOCKET_TIMEOUT,
        )

    @property
    def client(self) -> BaseRedis:
        """
        使用方法类似 redis 包，但是需要加上 await
        https://asyncio-redis.readthedocs.io/en/latest/pages/reference.html#connection-pool
        :return:
        """
        if not self._connection:
            raise UnboundLocalError("uninitialized redis -> await init()")
        return self._connection


redis = Redis()
