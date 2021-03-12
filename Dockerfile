ARG TAG
ARG NO_DEV

FROM python:3.8-slim-buster

MAINTAINER 1403951401@qq.com

ENV TAG=${TAG}
ENV NO_DEV=${NO_DEV}

COPY ./ /app

WORKDIR /app

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install $(test "${NO_DEV}" && echo "--no-dev") --no-root

CMD uvicorn cookiecutter_fastAPI.api.rule:app --host 0.0.0.0 --port 8000 --workers 4