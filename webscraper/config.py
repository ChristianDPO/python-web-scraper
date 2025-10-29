from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    It is created by getting all env variables declared in a .env file.

    :param scrape_url: URL of the page to be scraped
    :param rabbitmq_url: URL of the RabbitMQ server
    :param rabbitmq_queue: Name of the RabbitMQ queue for publishing/consuming messages
    :param redis_url: URL of the Redis server
    :param log_level: Logging level for the application. Defaults to "INFO"
    """

    # Scrape URL
    scrape_url: str

    # RabbitMQ
    rabbitmq_url: str
    rabbitmq_queue: str

    # Redis
    redis_url: str

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
