from typing import Any, Type

from cookiecutter_fastAPI.models.base.base_model import BaseModel


class BaseResponse(BaseModel):
    code: int = 200
    message: str = 'ok'
    data: Any = None


def format_response(cls: Type[BaseModel]) -> Type[Type[BaseResponse]]:
    response_name = cls.__name__
    cls.__name__ += "Data"

    class T(BaseResponse):
        data: cls = None

    def __init__(self, **kwargs):
        if not ("code" or "message" or "data") in kwargs:
            kwargs = {"data": kwargs}
        super(T, self).__init__(**kwargs)

    t = type(response_name, (T,), {"__init__": __init__})
    return t
