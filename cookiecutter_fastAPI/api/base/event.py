from time import time
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response

from cookiecutter_fastAPI.api.base.app import app
from cookiecutter_fastAPI.api.base.exceptions import exception_handler
from cookiecutter_fastAPI.lib.log import logger
from cookiecutter_fastAPI.lib.postgresql import postgresql
from cookiecutter_fastAPI.lib.redis import redis


@app.on_event("startup")
async def startup():
    await redis.init()


@app.on_event("shutdown")
async def shutdown():
    redis.client.close()
    await redis.client.wait_closed()


@app.middleware("http")
async def close_session(request: Request, call_next):
    # 记录请求时间
    before = time()
    # 添加日志 traceId 跟踪
    with logger.bin(Ts_Request_Id=request.headers.get('Ts-Request-Id', uuid4())):
        # 注入 sql Session
        async with postgresql.session_maker():
            # 序列化异常
            try:
                response: Response = await call_next(request)
            except Exception as e:
                response: Response = await exception_handler(request, e)

    response.headers["X-Response-Time"] = str(time() - before)
    return response
