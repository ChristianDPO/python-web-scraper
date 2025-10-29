from pydantic import BaseModel


class CacheMessageDTO(BaseModel):
    """
    DTO for cache messages.

    :param status: Status of the operation
    :param data: Data associated with the cache operation
    """

    status: str
    data: dict = {}
