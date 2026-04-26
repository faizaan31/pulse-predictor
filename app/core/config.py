from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "PulsePredictor"
    environment: str = Field("local", env="ENVIRONMENT")
    host: str = Field("0.0.0.0", env="APP_HOST")
    port: int = Field(8000, env="APP_PORT")

    postgres_host: str = Field("postgres", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("ml_service", env="POSTGRES_DB")
    postgres_user: str = Field("ml_user", env="POSTGRES_USER")
    postgres_password: str = Field("ml_password", env="POSTGRES_PASSWORD")

    model_dir: Path = Field(Path("artifacts"), env="MODEL_DIR")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
