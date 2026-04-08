from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    openai_api_key: str = ""
    database_url: str = "sqlite:///./forex_analysis.db"
    debug: bool = True
    log_level: str = "INFO"
    cache_ttl: int = 3600
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
