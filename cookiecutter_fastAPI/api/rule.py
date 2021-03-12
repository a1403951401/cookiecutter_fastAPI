import pkgutil
from importlib import import_module

from fastapi import HTTPException as FHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as SHTTPException

from cookiecutter_fastAPI.api.base.event import app
from cookiecutter_fastAPI.api.base.exceptions import exception_handler
from cookiecutter_fastAPI.api.base.router import routers
from cookiecutter_fastAPI.config import config
from cookiecutter_fastAPI.lib.log import logger

error = [
    Exception, FHTTPException, SHTTPException, RequestValidationError
]


def import_paths(*module_list: str):
    for filefiner, name, ispkg in pkgutil.iter_modules([config.PROJECT_PATH.joinpath(*module_list)]):
        import_paths(*module_list, name)
        if import_module(".".join([config.PACKAGE, *module_list, name])):
            logger.debug(f"import {'.'.join([config.PACKAGE, *module_list, name])}")


# 载入包
for view in [
    ['api', "views"]
]:
    import_paths(*view)

# 载入异常处理
for e in error:
    app.add_exception_handler(e, exception_handler)
    logger.debug(f"add exception handler {e.__name__}")

# 载入路由
for router in routers:
    app.include_router(router)
    logger.debug(f"include router {router.prefix}")

logger.debug(f'debug : {config.DEBUG}, init service success')
logger.debug(f'config : {config.json()}')
