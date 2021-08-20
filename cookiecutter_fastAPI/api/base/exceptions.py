from http import HTTPStatus

from fastapi import Request, Response, HTTPException as FHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as SHTTPException

from cookiecutter_fastAPI.config import config
from cookiecutter_fastAPI.lib.json import dumps
from loguru import logger
from cookiecutter_fastAPI.models.base.base_error import AccessTokenExpire, BaseError, BaseValueError
from cookiecutter_fastAPI.models.base.base_response import BaseResponse


async def exception_handler(request: Request, e: Exception) -> Response:
    if isinstance(e, (SHTTPException, FHTTPException)):
        return Response(
            BaseResponse(
                code=e.status_code,
                message=e.detail
            ).json(include={'code', 'message', 'data'}, ensure_ascii=False).encode("utf-8"),
            status_code=e.status_code,
            media_type="application/json"
        )
    debug = bool(request.headers.get('debug') or config.DEBUG)

    data = {
        "path": request.url.path,
        "body": None,
        "error": str(e)
    }

    if isinstance(e, BaseError):
        http_status = HTTPStatus(getattr(e, 'HTTPStatus', HTTPStatus.INTERNAL_SERVER_ERROR))
        response: BaseResponse = BaseResponse(
            code=e.code,
            message=http_status.phrase + " | " + e.message
        )
    elif isinstance(e, RequestValidationError):
        data['body'] = e.body
        new_e = BaseValueError()
        http_status = HTTPStatus(new_e.HTTPStatus)
        response: BaseResponse = BaseResponse(
            code=new_e.code,
            message=new_e.HTTPStatus.phrase + " | " + new_e.message
        )
        if debug:
            data['errors'] = e.errors()
    else:
        http_status = HTTPStatus(HTTPStatus.INTERNAL_SERVER_ERROR)
        response: BaseResponse = BaseResponse(
            code=http_status.value,
            message=http_status.phrase + " | " + str(e) if debug else BaseError.message
        )

    data.update({
        "code": response.code,
        "message": response.message,
        "scope": request.scope,
    })

    if not isinstance(e, config.LOG_PASS_EXCEPTION):
        logger.exception(
            "path={path} code={code} message={message}\n"
            "scope={scope}\n"
            "body={body}",
            **{k: dumps(v, default=str) if isinstance(v, dict) else v for k, v in data.items()}
        )
    if debug:
        response.data = {k: v for k, v in data.items() if k not in ['code', 'message', 'path']}

    response: Response = Response(
        dumps(response.dict(include={'code', 'message', 'data'}), default=str),
        status_code=http_status.value,
        media_type="application/json"
    )

    if isinstance(e, AccessTokenExpire):
        response.delete_cookie("token")
        response.delete_cookie("username")

    return response
