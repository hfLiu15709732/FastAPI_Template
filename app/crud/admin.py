from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.utils.security import get_password_hash

def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

def get_admin_by_id(db: Session, id: int):
    return db.query(Admin).filter(Admin.id == id).first()

def create_admin(db: Session, admin: AdminCreate):
    # 检查用户名是否已存在
    existing_admin = get_admin_by_username(db, admin.username)
    if existing_admin:
        raise ValueError(f"用户名 {admin.username} 已存在")
        
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        username=admin.username,
        password_hash=hashed_password,
        email=admin.email,
        full_name=admin.full_name
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin: AdminUpdate):
    db_admin = get_admin_by_id(db, admin_id)
    if db_admin is None:
        return None
    
    update_data = admin.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_admin, key, value)
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = get_admin_by_id(db, admin_id)
    if db_admin is None:
        return False
    
    db.delete(db_admin)
    db.commit()
    return True