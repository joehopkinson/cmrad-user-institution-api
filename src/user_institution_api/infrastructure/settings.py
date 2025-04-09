import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    database_url: str = "sqlite:///./database.db"


settings = Settings()
