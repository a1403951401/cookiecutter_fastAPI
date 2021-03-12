import time
from functools import singledispatch
from typing import Union


@singledispatch
def format_time(t: Union[str, int, float], fmt: str = None):
    raise ValueError(f"Unknown time type, {type(t)}")


@format_time.register(str)
def _(t: str, fmt: str = None):
    if not fmt:
        _date = ""
        _time = ""
        if c := t.count("-"):
            _date = "%Y-%m-%d" if c == 2 else "%Y-%m"
        elif c := t.count("/"):
            _date = "%Y/%m/%d" if c == 2 else "%Y/%m"
        if c := t.count(":"):
            _time = "%H:%M:%S" if c == 2 else "%H:%M"
        fmt = _date + (" " if " " in t else "") + _time
    return int(time.mktime(time.strptime(t, fmt)))


@format_time.register(int)
@format_time.register(float)
def _(timestamp: Union[int, float], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return time.strftime(fmt, time.localtime(timestamp))
