from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str

    class Config:
        orm_mode = True