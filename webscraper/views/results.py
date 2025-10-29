from fastapi import APIRouter, Request
from webscraper.services.scrape import ScrapeService
from webscraper.helpers.views_helper import ViewsHelper
from webscraper.models.response_dto import BaseResponse

router = APIRouter(prefix="/results", tags=["results"])


@router.get(
    "/{task_id}",
    response_model=BaseResponse,
    responses={
        200: {"description": "Returns scraping results successfully"},
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

    service = ScrapeService(
        request.app.state.settings.scrape_url,
        request.app.state.redis_client,
    )

    data = await service.get_cache(cnpj=task_id)

    if not data:
        return ViewsHelper.make_response(
            message="NOT FOUND", status="error", http_code=404
        )

    return ViewsHelper.make_response(data=data)
