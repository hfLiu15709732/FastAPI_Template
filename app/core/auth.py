import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session # 导入 Session
from app.utils.security import verify_password, create_access_token, ALGORITHM, SECRET_KEY
from datetime import timedelta
from app.core.config import get_db # 导入 get_db
from app.crud.admin import get_admin_by_username # 导入 get_admin_by_username

# OAuth2认证方案配置，指定登录URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def authenticate_user(
    username: str, 
    password: str,
    db: Session = Depends(get_db) # 添加 db 依赖
):
    """
    验证用户身份并返回用户对象
    
    参数:
        username (str): 用户名
        password (str): 明文密码
        
    返回:
        User | None: 验证成功返回用户对象，失败返回None
    """
    # 从数据库中获取用户
    user = get_admin_by_username(db, username) # 使用同步的 get_admin_by_username
    # 验证用户存在且密码匹配
    if user and verify_password(password, user.password_hash): # 修改为 user.password_hash
        return user
    return None



def create_token_response(username: str):
    """
    创建包含JWT访问令牌的响应
    
    参数:
        username (str): 用户名
        
    返回:
        dict: 包含访问令牌和令牌类型的字典
    """
    # 设置令牌过期时间
    access_token_expires = timedelta(minutes=30)
    # 创建JWT令牌，将用户名作为subject
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    # 返回标准的OAuth2响应格式
    return {"access_token": access_token, "token_type": "bearer"}



async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db) # 添加 db 依赖
):
    """
    从JWT令牌中解析并验证用户身份，返回当前登录用户

    参数:
        token (str): HTTP请求头中的Bearer令牌，自动从请求中获取

    返回:
        User: 当前登录用户的数据库对象

    异常:
        401: 令牌无效、过期或签名验证失败
        404: 令牌中的用户不存在（可能已被删除）
    """
    try:
        # 验证并解码JWT令牌（pyjwt与jose的API兼容）
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}  # 显式验证过期时间
        )

        # 从令牌负载中获取用户名（sub字段）
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="认证失败")

    except jwt.InvalidTokenError as e:
        # 处理各种JWT验证错误（签名无效、过期等）
        raise HTTPException(status_code=401, detail=f"令牌无效: {str(e)}")

    # 根据用户名从数据库中获取用户对象
    user = get_admin_by_username(db, username) # 使用同步的 get_admin_by_username
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user