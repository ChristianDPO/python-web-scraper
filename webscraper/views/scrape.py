import pydantic
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
        422: {"description": "Invalid CNPJ format"},
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

    try:
        message = ScrapeJobMessageDTO(cnpj=cnpj)
    except pydantic.ValidationError:
        return ViewsHelper.make_response(
            message="Invalid CNPJ format",
            status="error",
            http_code=422,
        )

    rabbitmq_client = request.app.state.rabbitmq_client

    try:
        await rabbitmq_client.publish(message)
    except Exception as e:
        return ViewsHelper.make_response(
            message=f"Failed to create scraping job: {str(e)}",
            status="error",
            http_code=500,
        )

    return ViewsHelper.make_response(data=message)
