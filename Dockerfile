FROM python:3.14-slim

WORKDIR /project

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Lynter
COPY flake8.cfg .
RUN flake8 --config flake8.cfg ./app