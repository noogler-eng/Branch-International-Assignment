import os

class Config:
    """Base configuration shared across all environments."""
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/microloans",
    )
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    DEBUG: bool = False
    TESTING: bool = False


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "debug"


class StagingConfig(Config):
    DEBUG = False
    LOG_LEVEL = "info"


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "error"
