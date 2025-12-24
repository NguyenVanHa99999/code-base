from database.session import SessionLocal
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from core.security import decode_access_token
from crud.user import get_user
from typing import Optional
from models.user import User

COOKIE_NAME = "access_token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _extract_token(request: Request, header_token: Optional[str] = None) -> Optional[str]:
    """Extract token from cookie first, then Authorization header"""
    # Priority 1: HttpOnly cookie
    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token:
        return cookie_token
    
    # Priority 2: Authorization header
    if header_token:
        return header_token
    
    return None


def get_current_user(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieves the current authenticated user based on JWT token from cookie or header.

    Args:
        request: The FastAPI request object to access cookies.
        header_token: The JWT token from Authorization header (optional).
        db: The database session dependency.

    Returns:
        The authenticated user object if the token is valid and the user exists.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist (status_code 401).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    
    token = _extract_token(request, header_token)
    if not token:
        raise credentials_exception
    
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    user = get_user(db, int(payload["sub"]))
    if user is None:
        raise credentials_exception
    return user


def get_current_user_optional(
    request: Request,
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Retrieves the current authenticated user based on JWT token from cookie or header.
    Returns None if authentication fails instead of raising an exception.

    Args:
        request: The FastAPI request object to access cookies.
        header_token: The JWT token from Authorization header (optional).
        db: The database session dependency.

    Returns:
        The authenticated user object if the token is valid and the user exists, None otherwise.
    """
    try:
        token = _extract_token(request, header_token)
        if not token:
            return None
        
        payload = decode_access_token(token)
        if payload is None or "sub" not in payload:
            return None
        user = get_user(db, int(payload["sub"]))
        return user
    except:
        return None


def get_optional_auth(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    Optional authentication from cookie or Authorization header.
    Returns None if no authentication is provided or if authentication fails.
    """
    # Try cookie first
    token = request.cookies.get(COOKIE_NAME)
    
    # Then try Authorization header
    if not token:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    token = None
            except:
                token = None
    
    if not token:
        return None
    
    try:
        payload = decode_access_token(token)
        if payload is None or "sub" not in payload:
            return None
            
        user = get_user(db, int(payload["sub"]))
        return user
    except:
        return None


# ROLE-BASED PERMISSION DEPENDENCIES

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency để yêu cầu user phải có role admin.
    Sử dụng: current_user = Depends(require_admin)
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


def require_teacher(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency để yêu cầu user phải có role teacher hoặc admin.
    Sử dụng: current_user = Depends(require_teacher)
    """
    if not current_user.has_any_role(["admin", "teacher"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher permission required"
        )
    return current_user


def require_teacher_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Alias cho require_teacher"""
    return require_teacher(current_user)


class RoleChecker:
    """
    Dependency class để kiểm tra role linh hoạt.
    
    Sử dụng:
        @router.get("/admin-only")
        def admin_endpoint(user: User = Depends(RoleChecker(["admin"]))):
            ...
        
        @router.get("/teacher-or-admin")
        def teacher_endpoint(user: User = Depends(RoleChecker(["admin", "teacher"]))):
            ...
    """
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_any_role(self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required roles: {', '.join(self.allowed_roles)}"
            )
        return current_user