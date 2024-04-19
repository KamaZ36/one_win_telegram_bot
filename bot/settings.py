import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    load_dotenv()

    bot_token: str = os.getenv('BOT_TOKEN')

    sqlalchemy_logging: bool = True
    use_webhook: bool = False
    skip_updating: bool = True
    use_redis: bool = False

    redis_host: str = os.getenv('REDIS_HOST')

    postgres_host: str = os.getenv('POSTGRES_HOST')
    postgres_database: str = os.getenv('POSTGRES_DATABASE')
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')

    id_private_channel: int = os.getenv('ID_PRIVATE_CHANNEL')
    id_admin: int = os.getenv('ID_ADMIN')

    throttle_time_spin: int = 5
    throttle_time_other: int = 3

    # webhook_path: str = os.getenv('WEBHOOK_PATH')
    # webhook_host: str = os.getenv('WEBHOOK_HOST')
    # webhook_url: str = f'{webhook_host}{webhook_path}'
    # webapp_host: str = os.getenv('WEBAPP_HOST')
    # webapp_port: int = os.getenv('WEBAPP_PORT')
    # webhook_secret: str = os.getenv('WEBAPP_SECRET')

    def create_dsn_postgresql(self):
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.postgres_host}/{self.postgres_database}'
        )


settings = Settings()
