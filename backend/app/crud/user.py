from sqlalchemy.orm import Session
from typing import List, Optional
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash
from crud.role import get_default_role, get_role


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email address"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Lấy danh sách users với phân trang"""
    return db.query(User).offset(skip).limit(limit).all()


def get_users_by_role(db: Session, role_id: int, skip: int = 0, limit: int = 100) -> List[User]:
    """Lấy danh sách users theo role"""
    return db.query(User).filter(User.role_id == role_id).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Tạo user mới.
    Nếu không có role_id, sẽ gán role 'student' mặc định.
    """
    hashed_password = get_password_hash(user.password)
    
    # Lấy role_id từ request hoặc dùng role mặc định (student)
    role_id = user.role_id
    if role_id is None:
        default_role = get_default_role(db)
        role_id = default_role.id if default_role else None
    
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role_id=role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Cập nhật thông tin user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.role_id is not None:
        db_user.role_id = user_update.role_id
    
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_role(db: Session, user_id: int, role_id: int) -> Optional[User]:
    """Cập nhật role cho user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Verify role exists
    role = get_role(db, role_id)
    if not role:
        return None
    
    db_user.role_id = role_id
    db.commit()
    db.refresh(db_user)
    return db_user