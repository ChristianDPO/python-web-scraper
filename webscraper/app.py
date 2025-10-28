from fastapi import FastAPI
from webscraper.views.scrape import router as scrape_router
from webscraper.config import Settings


def create_app():

    app = FastAPI(title="Web Scrapping API")

    # Routing
    app.include_router(scrape_router)

    # Configuration
    app.state.settings = Settings()

    return app
