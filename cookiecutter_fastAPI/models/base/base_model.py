from pydantic import BaseModel as Model

from cookiecutter_fastAPI.lib.json import loads, dumps


class BaseModel(Model):
    class Config:
        json_loads: loads
        json_dumps: dumps
