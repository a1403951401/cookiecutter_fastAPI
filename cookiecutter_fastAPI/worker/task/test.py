from cookiecutter_fastAPI.lib.celery import celery_app


@celery_app.task
def message(message: str):
    return f'message: {message}'
