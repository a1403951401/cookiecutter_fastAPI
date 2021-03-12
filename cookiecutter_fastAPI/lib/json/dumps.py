#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Callable, Any, Union

import orjson

from cookiecutter_fastAPI.lib.json.dumps_default import dumps_default


def dumps(
        obj: Any,
        *,
        default: Callable[..., Union[str, int, float, list, dict]] = dumps_default,
        option: int = 0) -> str:
    return orjson.dumps(obj, default=default, option=option).decode('utf-8')


loads = orjson.loads
