from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import common,admin,auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
# 包含API路由
app.include_router(common.router,prefix="/common",tags=["通用实验"])
app.include_router(admin.router, prefix="/admin",tags=["管理员"])
app.include_router(auth.router, prefix="/auth",tags=["权限教研"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Projectuuuu"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=3008, reload=True)