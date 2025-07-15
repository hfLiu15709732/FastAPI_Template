from fastapi import FastAPI
# from app.api.v1.endpoints import student
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 包含API路由
# app.include_router(user.router, prefix=settings.API_V1_STR)
# app.include_router(item.router, prefix=settings.API_V1_STR)
# app.include_router(common.router, prefix="/common")
# app.include_router(student.router, prefix="/student")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Projectssss"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=3008, reload=True)