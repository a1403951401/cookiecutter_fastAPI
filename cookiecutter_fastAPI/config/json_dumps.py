import pydantic.json

# 序列化json
pydantic.json.ENCODERS_BY_TYPE.update({
    set: lambda obj: list(obj),
    bytes: lambda obj: obj.decode('utf-8'),
    BaseException: lambda obj: f"Exception: {obj}",
    type: lambda obj: f"Type: {obj}",
})
