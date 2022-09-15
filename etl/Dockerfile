FROM python:3.10-slim

ENV APP_HOME=/usr/src/app

# set work directory
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "$APP_HOME"

RUN pip install --upgrade pip

# install psycopg2 dependencies & curl
RUN apt-get update && apt-get -y install libpq-dev gcc

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
