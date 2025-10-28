from fastapi import APIRouter, Request
from webscraper.services.scrape import ScrapeService


router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/")
async def scrape(
    request: Request,
    cnpj: str,
):

    config = request.app.state.settings

    scraper_service = ScrapeService(
        scrape_url=config.scrape_url,
        rabbitmq_url=config.rabbitmq_url,
        rabbitmq_queue=config.rabbitmq_queue,
    )

    job = await scraper_service.create_scrape_job(cnpj=cnpj)
    return job
