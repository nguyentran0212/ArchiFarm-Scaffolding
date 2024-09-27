from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prototyping Tools API"
    DEBUG: bool = False

settings = Settings()