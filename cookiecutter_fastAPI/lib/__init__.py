import pkgutil
from importlib import import_module

from loguru import logger

from cookiecutter_fastAPI.config import config


def import_paths(*module_list: str):
    for filefiner, name, ispkg in pkgutil.iter_modules([config.PROJECT_PATH.joinpath(*module_list)]):
        import_paths(*module_list, name)
        if import_module(".".join([config.PACKAGE, *module_list, name])):
            logger.debug(f"import {'.'.join([config.PACKAGE, *module_list, name])}")
