FROM python:3.8

COPY . /crud-api
WORKDIR /crud-api

ENV PYTHONPATH /crud-api

RUN pip install -r requirements.txt

EXPOSE 8000