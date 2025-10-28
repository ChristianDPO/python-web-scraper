from fastapi import APIRouter, Request

from webscraper.models.message_dto import ScrapeJobMessageDTO

from webscraper.helpers.views_helper import ViewsHelper

router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/")
async def scrape(
    request: Request,
    cnpj: str,
):

    message = ScrapeJobMessageDTO(cnpj=cnpj)

    rabbitmq_client = request.app.state.rabbitmq_client

    await rabbitmq_client.publish(message)

    return ViewsHelper.make_response(data=message)
