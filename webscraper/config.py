from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Scrape URL
    scrape_url: str

    # RabbitMQ
    rabbitmq_url: str
    rabbitmq_queue: str

    # Redis
    redis_url: str
    redis_queue: str

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
