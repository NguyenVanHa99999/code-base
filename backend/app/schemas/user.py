from pydantic import BaseModel
from typing import Optional
from schemas.role import RoleSimple


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None  # Mặc định sẽ là student


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None


class UserRead(UserBase):
    id: int
    user_code: str  # Mã định danh unique (10 ký tự)
    role_id: Optional[int] = None
    role: Optional[RoleSimple] = None

    class Config:
        from_attributes = True


class UserWithRole(UserRead):
    """User response với đầy đủ thông tin role"""
    role_name: Optional[str] = None
    is_admin: bool = False
    is_teacher: bool = False
    is_student: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int