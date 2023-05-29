# pull official base image
FROM python:3.9.6-alpine

RUN mkdir /usr/src/app

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY .. .
WORKDIR /usr/src/app/todo_list