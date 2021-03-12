from functools import singledispatch


@singledispatch
def dumps_default(obj):
    raise TypeError(obj)


@dumps_default.register(bytes)
def obj_to_decode(obj: bytes):
    return obj.decode('utf-8')


@dumps_default.register(set)
def obj_to_decode(obj: set):
    return list(obj)
