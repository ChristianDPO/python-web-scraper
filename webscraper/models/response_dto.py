from pydantic import BaseModel
from typing import Any, Optional


class BaseResponse(BaseModel):
    """
    Base DTO for API responses.

    :param status: Status of the response (e.g., 'success', 'error')
    :param message: Optional message providing additional information
    :param data: Optional data payload of the response
    """

    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
