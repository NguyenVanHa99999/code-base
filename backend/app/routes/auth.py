from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from services.auth_service import authenticate_user, login_for_access_token
from services.user_service import service_create_user
from services.lockout_service import (
    check_account_locked,
    record_failed_attempt,
    reset_failed_attempts,
    get_lockout_status,
    AccountLockout
)
from schemas.user import UserCreate, UserRead, Token
from dependencies.deps import get_db
from crud.user import get_user_by_email
from crud.role import get_role_by_name
from core.config import settings
from core.password_policy import validate_password, get_password_strength

router = APIRouter()

# Cookie configuration
COOKIE_NAME = "access_token"
COOKIE_MAX_AGE = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


def _login_with_role(
    response: Response,
    form_data: OAuth2PasswordRequestForm,
    db: Session,
    required_role: Optional[str] = None
) -> dict:
    """
    Login helper function với kiểm tra role và account lockout.
    
    Args:
        required_role: Tên role yêu cầu (admin/teacher/student). None = không check role.
    """
    email = form_data.username
    
    # Check account lockout TRƯỚC khi check password
    is_locked, remaining_seconds = check_account_locked(email)
    if is_locked:
        minutes = remaining_seconds // 60 + 1
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account is locked due to too many failed attempts. Try again in {minutes} minutes."
        )
    
    # Authenticate user
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        # Ghi nhận failed attempt
        failed_count, is_now_locked = record_failed_attempt(email)
        remaining = AccountLockout.MAX_FAILED_ATTEMPTS - failed_count
        
        if is_now_locked:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Account is now locked due to too many failed attempts. Try again in {AccountLockout.LOCKOUT_DURATION_MINUTES} minutes."
            )
        
        detail = "Incorrect email or password"
        if remaining > 0:
            detail += f" ({remaining} attempts remaining)"
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    
    # Login thành công - reset failed attempts
    reset_failed_attempts(email)
    
    # Kiểm tra role nếu có yêu cầu
    if required_role:
        user_role = user.role_name if user.role else None
        
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. This portal is for {required_role} only."
            )
    
    access_token = login_for_access_token(user)
    
    # Set HttpOnly cookie với SameSite=Strict (CSRF protection)
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="strict",  # Cải thiện: strict thay vì lax để chống CSRF
        path="/"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "user_code": user.user_code,
            "name": user.name,
            "email": user.email,
            "role": user.role_name
        }
    }


# LOGIN ENDPOINTS

@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login chung - không kiểm tra role (backward compatible)"""
    result = _login_with_role(response, form_data, db, required_role=None)
    return {"access_token": result["access_token"], "token_type": result["token_type"]}


@router.post("/login/admin")
def login_admin(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login cho Admin Portal - Chỉ admin được phép đăng nhập"""
    return _login_with_role(response, form_data, db, required_role="admin")


@router.post("/login/teacher")
def login_teacher(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login cho Teacher Portal - Chỉ teacher được phép đăng nhập"""
    return _login_with_role(response, form_data, db, required_role="teacher")


@router.post("/login/student")
def login_student(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login cho Student Portal - Chỉ student được phép đăng nhập"""
    return _login_with_role(response, form_data, db, required_role="student")


# LOGOUT

@router.post("/logout")
def logout(response: Response):
    """Clear the authentication cookie"""
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        httponly=True,
        secure=False,
        samesite="strict"
    )
    return {"message": "Logged out successfully"}


# REGISTER

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới.
    - Kiểm tra password policy
    - Mặc định role là 'student'
    - Admin có thể cập nhật role sau
    """
    # Validate password policy
    is_valid, errors = validate_password(user.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Password does not meet security requirements",
                "errors": errors
            }
        )
    
    # Check if email already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Nếu không có role_id, gán role student mặc định
    if user.role_id is None:
        student_role = get_role_by_name(db, "student")
        if student_role:
            user.role_id = student_role.id
    
    new_user = service_create_user(db, user)
    return UserRead.model_validate(new_user)


# Backward compatible alias
@router.post("/create", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Alias for /register (backward compatible)"""
    return register(user, db)


# UTILITIES

@router.get("/check-email/{email}")
def check_email_exists(email: str, db: Session = Depends(get_db)):
    """Check if email exists in database"""
    user = get_user_by_email(db, email)
    return {"exists": user is not None}


@router.get("/roles")
def get_available_roles(db: Session = Depends(get_db)):
    """Lấy danh sách roles để frontend hiển thị"""
    from crud.role import get_roles
    roles = get_roles(db)
    return [{"id": r.id, "name": r.name, "display_name": r.display_name} for r in roles]


@router.post("/validate-password")
def validate_password_strength(password: str):
    """
    Kiểm tra độ mạnh của mật khẩu.
    Có thể dùng ở frontend để hiển thị realtime.
    """
    is_valid, errors = validate_password(password)
    strength = get_password_strength(password)
    
    return {
        "is_valid": is_valid,
        "errors": errors,
        "strength": strength
    }


@router.get("/lockout-status/{email}")
def get_account_lockout_status(email: str):
    """
    Kiểm tra trạng thái lockout của tài khoản.
    (Chỉ dùng cho debug/admin)
    """
    return get_lockout_status(email)