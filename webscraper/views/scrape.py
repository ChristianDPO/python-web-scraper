from fastapi import APIRouter, Request
from webscraper.models.message_dto import ScrapeJobMessageDTO
from webscraper.helpers.views_helper import ViewsHelper
from webscraper.models.response_dto import BaseResponse

router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post(
    "/",
    response_model=BaseResponse,
    responses={
        200: {"description": "Scraping job created successfully"},
        500: {"description": "Internal server error"},
    },
)
async def scrape(
    request: Request,
    cnpj: str,
):
    """
    Endpoint to create a scraping job for a given CNPJ.
    Sends a message to RabbitMQ to initiate the scraping process.
    """
    message = ScrapeJobMessageDTO(cnpj=cnpj)

    rabbitmq_client = request.app.state.rabbitmq_client

    await rabbitmq_client.publish(message)

    return ViewsHelper.make_response(data=message)
