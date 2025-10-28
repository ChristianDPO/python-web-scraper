FROM python:3.14-slim

WORKDIR /project

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY ./webscraper ./webscraper
COPY setup.py ./setup.py
RUN rm -rf *.egg-info

# Lynter
COPY flake8.cfg .
RUN flake8 --config flake8.cfg ./webscraper

# Install project package
RUN pip install -e .