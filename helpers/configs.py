from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    
    APP_NAME: str
    APP_VERSION: str
    
    FILE_ALLOWED_TYPES: List[str]
    FILE_MAX_SIZE_MB: int
    FILE_CHUNK_SIZE_BYTES: int

    class Config:
        env_file = '.env'
        

def get_settings():
    return Settings()