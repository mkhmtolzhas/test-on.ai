from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    alembic_url: str = ""


    def model_post_init(self, __context):
        self.alembic_url = self.database_url.replace("+aiosqlite", "")

    class Config:
        env_file = ".env"

settings = Settings()