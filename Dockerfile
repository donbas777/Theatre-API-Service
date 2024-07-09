FROM python:3.11
LABEL maintainer="renary34@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /Theatre_API_Service

COPY . .
RUN pip install -r requirements.txt

COPY . /Theatre_API_Service/

