from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_token_response
from app.core.config import get_db
from app.schemas.auth import UserOut, UserCreate
from app.utils.response_models import error_response, success_response
from app.utils.security import get_password_hash
from app.crud.admin import get_admin_by_username, create_admin

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(admin: UserCreate, db: Session = Depends(get_db)):
    if get_admin_by_username(db, admin.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    admin_obj = create_admin(
        db,
        username=admin.username,
        password=get_password_hash(admin.password)
    )
    return admin_obj

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # 尝试认证用户
        user = await authenticate_user(form_data.username, form_data.password,db)

        # 认证失败处理
        if not user:
            return error_response(message="用户名或密码错误", code=401)

        # 认证成功，生成令牌
        token_data = create_token_response(user.username)
        return success_response(data=token_data, message="登录成功")

    except Exception as e:
        # 处理意外异常
        return error_response(message=f"登录过程发生错误: {str(e)}", code=500)