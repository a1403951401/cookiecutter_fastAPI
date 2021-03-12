from http import HTTPStatus
from typing import Optional


class BaseError(Exception):
    HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    code: Optional[int] = 500
    message: Optional[str] = '方法内部错误'

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class BaseValueError(BaseError):
    HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY
    code = 422
    message = '参数有误，请检查请求参数'


class ForbiddenError(BaseError):
    HTTPStatus = HTTPStatus.FORBIDDEN
    code = 403
    message = '用户权限不足，或尝试重新登录'


class AccessTokenExpire(BaseError):
    HTTPStatus = HTTPStatus.UNAUTHORIZED
    code = 401
    message = '用户认证失败'