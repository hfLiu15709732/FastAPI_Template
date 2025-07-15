from pydantic_settings import BaseSettings
from sqlmodel import create_engine

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Study"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI 学习项目结构"
    PROJECT_DESCRIPTION: str = "FastAPI Project"
    VERSION: str = "0.1.0"
    
    # 数据库配置
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str = "walt-work"
    DATABASE_URL: str = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    @property
    def engine(self):
        return create_engine(self.DATABASE_URL)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()


