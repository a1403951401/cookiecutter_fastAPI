from fastapi import APIRouter as Router

routers = []


class APIRouter(Router):
    def __init__(self, *args, **kwargs):
        super(APIRouter, self).__init__(*args, **kwargs)
        routers.append(self)


index_router = APIRouter(
    prefix="",
    tags=["index"]
)
