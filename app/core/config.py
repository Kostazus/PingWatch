from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    secret_key: str
    access_token_minutes: int = 30
    refresh_token_days: int = 7
    cors_origins: list[str] = []
    min_interval_seconds: int = 60
    max_monitors_per_user: int = 20
    check_timeout_seconds: int = 10
    max_concurrent_checks: int = 5
    results_retention_days: int = 30

settings = Settings()


