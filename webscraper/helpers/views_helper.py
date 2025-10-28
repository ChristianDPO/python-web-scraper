from fastapi.responses import JSONResponse

from webscraper.models.response_dto import BaseResponse


class ViewsHelper(object):
    """
    Helper class for API views.
    """

    @staticmethod
    def make_response(data=None, message=None, status="success", http_code=200):
        """
        Create a standardized JSON response.

        :param any data: The data to include in the response
        :param str message: Optional message to include in the response
        :param str status: Status of the response (default is "success")
        :param int http_code: HTTP status code for the response (default is 200)
        """
        return JSONResponse(
            content=BaseResponse(
                status=status, message=message, data=data
            ).model_dump(),
            status_code=http_code,
        )
