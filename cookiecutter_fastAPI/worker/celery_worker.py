from loguru import logger

from cookiecutter_fastAPI.lib import import_paths
from cookiecutter_fastAPI.lib.celery import *

# 载入默认视图
for view in config.TASK_PATH.split(','):
    logger.debug(f"import view models: {config.PACKAGE}.{view.replace('/', '.')}")
    import_paths(*(view.split('/')))
