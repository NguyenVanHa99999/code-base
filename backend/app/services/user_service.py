from sqlalchemy.orm import Session
from typing import Optional, List

from crud.user import get_user, create_user, get_users
from schemas.user import UserCreate
from models.user import User


def service_create_user(db: Session, user: UserCreate) -> User:
    """
    Tạo user mới.
    Returns User model.
    """
    return create_user(db, user)


def service_get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Lấy user theo ID.
    Returns User hoặc None nếu không tìm thấy.
    """
    return get_user(db, user_id)


def service_get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    """
    Lấy danh sách users với phân trang.
    """
    return get_users(db, skip=skip, limit=limit)