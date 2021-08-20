from typing import Any, Union

import orjson
from pydantic.json import pydantic_encoder


def dumps(obj: Any, *, option: int = 0, decode=True, default=None) -> Union[bytes, str]:
    json = orjson.dumps(obj, default=default or pydantic_encoder, option=option)
    return json.decode('utf-8') if decode else json


loads = orjson.loads
