# syntax=docker/dockerfile:1
FROM python:latest AS BACKEND
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY . /backend/
RUN pip install -r requirements.txt