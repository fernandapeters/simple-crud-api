FROM python:3.8
#ENV PYTHONUNBUFFERRED 1

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8000