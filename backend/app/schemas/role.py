from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    """Base schema cho Role"""
    name: str
    display_name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema để tạo role mới"""
    pass


class RoleUpdate(BaseModel):
    """Schema để update role"""
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RoleRead(RoleBase):
    """Schema để đọc role"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RoleSimple(BaseModel):
    """Schema đơn giản cho role (dùng trong User response)"""
    id: int
    name: str
    display_name: str

    class Config:
        from_attributes = True
