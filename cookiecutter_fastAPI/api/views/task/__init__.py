from uuid import UUID

from cookiecutter_fastAPI.api.base.router import task_router
from cookiecutter_fastAPI.lib.celery import celery_app
from cookiecutter_fastAPI.models.base.base_model import BaseModel
from cookiecutter_fastAPI.models.base.base_response import format_response


@format_response
class TaskResponse(BaseModel):
    task_id: UUID
    data: str = None


@task_router.get("/",
                 summary="创建任务",
                 response_model=TaskResponse)
async def task(message: str = ''):
    """ http://127.0.0.1:8000/task?message=123 """
    from cookiecutter_fastAPI.worker.task.test import message as m
    return TaskResponse(task_id=m.delay(message).id)


@task_router.get("/{task_id}",
                 summary="查询任务",
                 response_model=TaskResponse)
async def get_task(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return TaskResponse(task_id=task_id, data=task.result)
