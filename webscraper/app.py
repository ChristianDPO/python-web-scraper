from fastapi import FastAPI
from webscraper.views.scrape import router as scrape_router

from webscraper.config import Settings

from webscraper.clients.rabbitmq import AsyncRabbitMQClient

from webscraper.helpers.log import Log


def create_app():

    app = FastAPI(title="Web Scrapping API")

    # Routing
    app.include_router(scrape_router)

    # Configuration
    app.state.settings = Settings()

    # Logging
    Log.setup(app.state.settings.log_level)

    # Clients
    rabbitmq_client = AsyncRabbitMQClient(
        app.state.settings.rabbitmq_url, app.state.settings.rabbitmq_queue
    )
    app.state.rabbitmq_client = rabbitmq_client

    return app
