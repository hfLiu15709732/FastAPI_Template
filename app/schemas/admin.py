from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class AdminBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(AdminBase):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None

class AdminSchema(AdminBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True