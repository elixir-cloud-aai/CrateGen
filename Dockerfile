# Dockerfile for wrroc-ga4gh-cloud-converter
FROM python:3.11.6
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt