from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from app.core.config import settings
from app.api.endpoints import common


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    SQLModel.metadata.create_all(settings.engine)
    yield
    # 关闭时可以添加清理代码


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


def get_session():
    with Session(settings.engine) as session:
        yield session

# 包含API路由
app.include_router(common.router,prefix="/common")
# app.include_router(student.router, prefix="/student")




@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Projectssss"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=3008, reload=True)