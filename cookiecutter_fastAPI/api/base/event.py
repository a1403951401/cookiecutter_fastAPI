from time import time
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response

from cookiecutter_fastAPI.api.base.app import app
from cookiecutter_fastAPI.api.base.exceptions import exception_handler
from loguru import logger
from cookiecutter_fastAPI.lib.database import database
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
    # trace 信息
    before = time()
    trace_data = {
        'Ts-Request-Id': request.headers.get('Ts-Request-Id', str(uuid4())),
    }
    with logger.contextualize(**trace_data):
        # 注入 sql Session
        async with database.session_maker():
            # 序列化异常
            try:
                response: Response = await call_next(request)
            except Exception as e:
                response: Response = await exception_handler(request, e)
    after = time()
    response.headers.update({
        'X-Request-After': str(after),
        'X-Request-Before': str(before),
        'X-Response-Time': str(after - before),
        **trace_data
    })
    return response
