import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    TG_TOKEN: str
    AI_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

load_dotenv()

settings = Settings()
