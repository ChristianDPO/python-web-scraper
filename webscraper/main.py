from fastapi import FastAPI
from webscraper.api.scrape import router as scrape_router

app = FastAPI(title="Web Scrapping API")

app.include_router(scrape_router)


@app.get("/")
def root():
    return {"message": "API is running"}
