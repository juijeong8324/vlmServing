from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Model
    model_name: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    model_device: str = "cuda"
    model_dtype: Literal["float16", "bfloat16", "float32"] = "float16"
    max_new_tokens: int = 1024
    temperature: float = 0.1

    # Server
    host: str = "0.0.0.0"
    port: int = 8001

    # Logging
    log_level: str = "INFO"


settings = Settings()
