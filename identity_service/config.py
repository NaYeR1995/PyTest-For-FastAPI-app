from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore'
    )
    DATABASE_URL: str
    DATABASE_URL_TESTING: str
    POOL_SIZE: str
    MAX_OVERFLOW: str
    POOL_TIMEOUT: str
    POOL_RECYCLE: str
    
    TESTING_MODE: bool


settings = Settings()
