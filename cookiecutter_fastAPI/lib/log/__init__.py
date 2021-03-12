from contextvars import ContextVar
from functools import singledispatch
from typing import Any, Dict

import loguru

from cookiecutter_fastAPI.lib.json import dumps
from cookiecutter_fastAPI.models.base.base_model import BaseModel

logger_globals_context_var = ContextVar('logger', default=dict())


@singledispatch
def log_args_default(obj):
    return str(obj)


@log_args_default.register(dict)
@log_args_default.register(list)
@log_args_default.register(tuple)
def obj_to_decode(obj: Any):
    return dumps(obj)


@log_args_default.register(BaseModel)
def obj_to_decode(obj: BaseModel):
    return obj.json()


class BaseLogger:
    @property
    def globals(self) -> Dict[str, Any]:
        return logger_globals_context_var.get()

    def __setitem__(self, key, value) -> None:
        self.globals[key] = value

    def __getitem__(self, key) -> Any:
        return self.globals[key]

    class bin:
        kwargs: Dict[str, Any]

        def __init__(self, **kwargs):
            self.kwargs = kwargs
            logger.globals.update(kwargs)

        def __enter__(self, **kwargs):
            return logger

        def __exit__(self, exc_type, exc, tb):
            for k in self.kwargs.keys():
                del logger.globals[k]

    def format_message(self, __message: str, *args: Any, **kwargs: Any) -> str:
        if not isinstance(__message, str):
            __message = str(__message)
        for value in args:
            __message += f" {log_args_default(value)}"
        for key, value in {**self.globals, **kwargs}.items():
            __message += f" {key}={log_args_default(value)}"
        return __message

    def log(self, __level: str, __message: str, *args: Any, **kwargs: Any) -> None:
        if __message:
            return loguru.logger.log(__level, self.format_message(__message, *args, **kwargs))

    def exception(self, __message: str, *args: Any, **kwargs: Any) -> None:
        if __message:
            return loguru.logger.exception(self.format_message(__message, *args, **kwargs))

    def _log(self, __level: str, *args: Any, **kwargs: Any) -> None:
        return self.log(__level, *args, **kwargs)

    def __getattr__(self, item) -> callable:
        return lambda *args, **kwargs: self._log(item.upper(), *args, **kwargs)


logger = BaseLogger()
