from sqlalchemy.orm import Session
from typing import List, Optional
from models.role import Role, DEFAULT_ROLES
from schemas.role import RoleCreate, RoleUpdate


def get_role(db: Session, role_id: int) -> Optional[Role]:
    """Lấy role theo ID"""
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    """Lấy role theo tên"""
    return db.query(Role).filter(Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    """Lấy danh sách roles"""
    return db.query(Role).filter(Role.is_active == True).offset(skip).limit(limit).all()


def get_all_roles(db: Session) -> List[Role]:
    """Lấy tất cả roles (bao gồm inactive)"""
    return db.query(Role).all()


def create_role(db: Session, role: RoleCreate) -> Role:
    """Tạo role mới"""
    db_role = Role(
        name=role.name,
        display_name=role.display_name,
        description=role.description
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
    """Cập nhật role"""
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    
    if role_update.display_name is not None:
        db_role.display_name = role_update.display_name
    if role_update.description is not None:
        db_role.description = role_update.description
    if role_update.is_active is not None:
        db_role.is_active = role_update.is_active
    
    db.commit()
    db.refresh(db_role)
    return db_role


def seed_default_roles(db: Session) -> List[Role]:
    """
    Seed các roles mặc định vào database.
    Chỉ tạo nếu chưa tồn tại.
    """
    created_roles = []
    
    for role_data in DEFAULT_ROLES:
        existing = get_role_by_name(db, role_data["name"])
        if not existing:
            role = Role(
                name=role_data["name"],
                display_name=role_data["display_name"],
                description=role_data["description"]
            )
            db.add(role)
            created_roles.append(role)
    
    if created_roles:
        db.commit()
        for role in created_roles:
            db.refresh(role)
    
    return created_roles


def get_default_role(db: Session) -> Optional[Role]:
    """Lấy role mặc định (student) cho user mới"""
    return get_role_by_name(db, "student")
