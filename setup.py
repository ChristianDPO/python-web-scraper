from setuptools import setup

setup(
    name="webscraper",
    version="0.1.0",
    packages=[
        "webscraper",
        "webscraper/views",
        "webscraper/worker",
        "webscraper/services",
        "webscraper/clients",
        "webscraper/models",
        "webscraper/helpers",
    ],
)
