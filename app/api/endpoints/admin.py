from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.admin import create_admin, update_admin, delete_admin, get_admin_by_username, get_admin_by_id
from app.schemas.admin import AdminCreate, AdminUpdate, AdminSchema
from app.core.config import get_db
from app.utils.response_models import success_response, error_response
from app.core.auth import get_current_user # 导入 get_current_user

router = APIRouter()

@router.get("/username/{username}",summary="根据用户名查询用户接口")
def read_admin_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    try:
        admin = get_admin_by_username(db, username)
        if admin is None:
            return error_response(message="Admin not found", code=404)
        return success_response(data=admin)
    except Exception as e:
        return error_response(message=str(e))


@router.get("/id/{admin_id}",summary="根据用户id查询用户接口")
def read_admin_by_id(
    admin_id: int,
    db: Session = Depends(get_db)
):
    try:
        admin = get_admin_by_id(db, admin_id)
        if admin is None:
            return error_response(message="Admin not found", code=404)
        return success_response(data=admin)
    except Exception as e:
        return error_response(message=str(e))



@router.post("/add",summary="创建用户接口")
def create_new_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db)
):
    try:
        existing_admin = get_admin_by_username(db, admin.username)
        if existing_admin:
            return error_response(message=f"用户名 {admin.username} 已存在", code=400)
        
        created_admin = create_admin(db, admin)
        return success_response(data=AdminSchema.model_validate(created_admin), message="管理员创建成功")
    except Exception as e:
        return error_response(message=str(e))



@router.put("",summary="修改用户接口")
def update_existing_admin(
    admin: AdminUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated_admin = update_admin(db, admin.id, admin)
        if updated_admin is None:
            return error_response(message="Admin not found", code=404)
        # 将 SQLAlchemy Admin 模型实例转换为 AdminSchema Pydantic 模型实例
        return success_response(data=AdminSchema.model_validate(updated_admin), message="管理员更新成功")
    except Exception as e:
        return error_response(message=str(e))



@router.delete("/{admin_id}",summary="删除用户接口")
def delete_existing_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # 添加认证依赖
):
    try:
        print(current_user)
        if not delete_admin(db, admin_id):
            return error_response(message="Admin not found", code=404)
        return success_response(message="Admin deleted successfully")
    except Exception as e:
        return error_response(message=str(e))