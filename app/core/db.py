from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Study"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI 学习项目结构"
    PROJECT_DESCRIPTION: str = "FastAPI Project with SQLAlchemy and PostgreSQL"
    VERSION: str = "0.1.0"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()


