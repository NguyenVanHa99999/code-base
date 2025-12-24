from sqlalchemy.orm import Session
from typing import Optional

from crud.user import get_user_by_email
from core.security import verify_password, create_access_token
from models.user import User


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user by email and password.
    Returns User if valid, None otherwise.
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def login_for_access_token(user: User) -> str:
    """
    Generate access token for authenticated user.
    """
    return create_access_token(data={"sub": str(user.id)})