import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    load_dotenv()

    session_name: str = os.getenv('SESSION_NAME')
    api_hash: str = os.getenv('API_HASH')
    api_id: str = os.getenv('API_ID')

    chat_one_win: str | int = os.getenv('CHAT_ONE_WIN')
    chat_in_moderating: str | int = os.getenv('CHAT_IN_MODERATING')

    postgres_host: str = os.getenv('POSTGRES_HOST')
    postgres_database: str = os.getenv('POSTGRES_DATABASE')
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')

    def create_dsn_postgresql(self):
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.postgres_host}/{self.postgres_database}'
        )


config = Config()
