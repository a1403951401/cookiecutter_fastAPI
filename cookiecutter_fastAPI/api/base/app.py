import typing

from fastapi import FastAPI as BaseFastAPI
from fastapi.datastructures import Default
from fastapi.responses import Response

from cookiecutter_fastAPI.lib.json import dumps


class ORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return dumps(content, decode=False)


class FastAPI(BaseFastAPI):
    pass


app = FastAPI(
    default_response_class=Default(ORJSONResponse),
)
