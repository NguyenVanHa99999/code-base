"""
Account lockout service.
Khóa tài khoản sau nhiều lần đăng nhập sai để chống brute-force.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
from cache.redis_client import get_cache, set_cache, delete_cache

logger = logging.getLogger(__name__)


class AccountLockout:
    """
    Account lockout configuration.
    """
    MAX_FAILED_ATTEMPTS = 5  # Số lần sai tối đa
    LOCKOUT_DURATION_MINUTES = 15  # Thời gian khóa (phút)
    RESET_ATTEMPTS_AFTER_MINUTES = 30  # Reset đếm sau bao lâu không có attempt mới


def _get_lockout_key(email: str) -> str:
    """Generate cache key cho lockout data"""
    return f"lockout:{email.lower()}"


def check_account_locked(email: str) -> Tuple[bool, Optional[int]]:
    """
    Kiểm tra tài khoản có bị khóa không.
    
    Args:
        email: Email cần kiểm tra
        
    Returns:
        Tuple (is_locked, remaining_seconds)
        - is_locked: True nếu tài khoản đang bị khóa
        - remaining_seconds: Số giây còn lại trước khi unlock (None nếu không khóa)
    """
    key = _get_lockout_key(email)
    data = get_cache(key)
    
    if not data:
        return False, None
    
    locked_until = data.get("locked_until")
    if locked_until:
        locked_until_dt = datetime.fromisoformat(locked_until)
        if datetime.now() < locked_until_dt:
            remaining = int((locked_until_dt - datetime.now()).total_seconds())
            return True, remaining
        else:
            # Lockout đã hết hạn, reset
            delete_cache(key)
            return False, None
    
    return False, None


def record_failed_attempt(email: str) -> Tuple[int, bool]:
    """
    Ghi nhận lần đăng nhập sai.
    
    Args:
        email: Email đăng nhập sai
        
    Returns:
        Tuple (failed_count, is_now_locked)
    """
    key = _get_lockout_key(email)
    data = get_cache(key) or {"failed_attempts": 0, "locked_until": None}
    
    # Tăng số lần sai
    data["failed_attempts"] = data.get("failed_attempts", 0) + 1
    data["last_attempt"] = datetime.now().isoformat()
    
    # Kiểm tra có đủ để khóa không
    is_locked = False
    if data["failed_attempts"] >= AccountLockout.MAX_FAILED_ATTEMPTS:
        lockout_until = datetime.now() + timedelta(minutes=AccountLockout.LOCKOUT_DURATION_MINUTES)
        data["locked_until"] = lockout_until.isoformat()
        is_locked = True
        logger.warning(f"Account locked: {email} - Too many failed attempts")
    
    # Lưu vào cache (ttl sau RESET_ATTEMPTS_AFTER_MINUTES)
    set_cache(key, data, ttl=AccountLockout.RESET_ATTEMPTS_AFTER_MINUTES * 60)
    
    return data["failed_attempts"], is_locked


def reset_failed_attempts(email: str) -> None:
    """
    Reset số lần đăng nhập sai sau khi login thành công.
    
    Args:
        email: Email cần reset
    """
    key = _get_lockout_key(email)
    delete_cache(key)
    logger.info(f"Reset failed attempts for: {email}")


def get_lockout_status(email: str) -> dict:
    """
    Lấy thông tin trạng thái lockout.
    
    Returns:
        dict với các thông tin lockout
    """
    key = _get_lockout_key(email)
    data = get_cache(key)
    
    if not data:
        return {
            "is_locked": False,
            "failed_attempts": 0,
            "remaining_attempts": AccountLockout.MAX_FAILED_ATTEMPTS,
            "locked_until": None,
            "remaining_seconds": None
        }
    
    is_locked, remaining_seconds = check_account_locked(email)
    failed_attempts = data.get("failed_attempts", 0)
    
    return {
        "is_locked": is_locked,
        "failed_attempts": failed_attempts,
        "remaining_attempts": max(0, AccountLockout.MAX_FAILED_ATTEMPTS - failed_attempts),
        "locked_until": data.get("locked_until"),
        "remaining_seconds": remaining_seconds
    }
