import pydantic
from fastapi import APIRouter, Request
from webscraper.models.message_dto import ScrapeJobMessageDTO
from webscraper.services.scrape import ScrapeService
from webscraper.helpers.views_helper import ViewsHelper
from webscraper.models.response_dto import BaseResponse

router = APIRouter(prefix="/results", tags=["results"])


@router.get(
    "/{task_id}",
    response_model=BaseResponse,
    responses={
        200: {"description": "Returns scraping results successfully"},
        422: {"description": "Invalid CNPJ format"},
        500: {"description": "Internal server error"},
    },
)
async def results(
    request: Request,
    task_id: str,
):
    """
    Endpoint to retrieve scraping results for a given task ID.
    The task ID is a cnpj in this context.
    """

    try:
        message = ScrapeJobMessageDTO(cnpj=task_id)
    except pydantic.ValidationError:
        return ViewsHelper.make_response(
            message="Invalid CNPJ format",
            status="error",
            http_code=422,
        )

    service = ScrapeService(
        request.app.state.settings.scrape_url,
        request.app.state.redis_client,
    )

    data = await service.get_cache(cnpj=message.cnpj)

    if not data:
        return ViewsHelper.make_response(
            message=f"No job found for CNPJ {message.cnpj}",
            status="error",
            http_code=404,
        )

    return ViewsHelper.make_response(data=data)
