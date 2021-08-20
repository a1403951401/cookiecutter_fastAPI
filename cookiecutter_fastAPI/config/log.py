import sys

from loguru import logger

from cookiecutter_fastAPI.lib.json import dumps

FORMAT_MSG = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | " \
             "<level>{level: <8}</level> | " \
             "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
EXTRA = " | {extra}"

FORMAT_TO_JSON = True


def formatter(record):
    if record["extra"]:
        if FORMAT_TO_JSON and isinstance(record["extra"], (list, dict)):
            record["extra"] = dumps(record["extra"])
        return f"{FORMAT_MSG}{EXTRA}\n"
    return f"{FORMAT_MSG}\n"


def remove_config(level="INFO"):
    logger.remove()
    logger.add(sys.stderr, level=level, format=formatter)
