import time
from datetime import datetime

from sqlalchemy import func, select

from cookiecutter_fastAPI.api.base.router import index_router
from cookiecutter_fastAPI.config import config
from cookiecutter_fastAPI.lib.postgresql import postgresql
from cookiecutter_fastAPI.lib.redis import redis
from cookiecutter_fastAPI.models.base.base_model import BaseModel
from cookiecutter_fastAPI.models.base.base_response import format_response


@format_response
class IndexResponse(BaseModel):
    now: datetime


@index_router.get("/",
                  summary="首页",
                  response_model=IndexResponse)
async def index():
    now_select = await postgresql.session.execute(
        select(func.now())
    )
    now: datetime = now_select.scalar_one()
    await redis.client.set(
        f'{config.PROJECT_NAME}_index',
        time.mktime(now.timetuple()),
        expire=60 * 10
    )
    return IndexResponse(now=now)
