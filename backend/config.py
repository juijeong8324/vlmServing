from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Model server
    model_server_url: str = "http://localhost:8001"
    model_server_timeout: float = 120.0

    # Logging
    log_level: str = "INFO"


settings = Settings()
