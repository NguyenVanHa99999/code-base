"""
Password validation utilities.
Đảm bảo mật khẩu đủ mạnh để bảo vệ tài khoản.
"""

import re
from typing import Tuple, List


class PasswordPolicy:
    """
    Password policy configuration.
    Có thể điều chỉnh các thông số tùy theo yêu cầu bảo mật.
    """
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = False  # Optional - có thể bật khi cần
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"


def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password theo policy.
    
    Args:
        password: Mật khẩu cần kiểm tra
        
    Returns:
        Tuple (is_valid, list_of_errors)
        
    Example:
        >>> is_valid, errors = validate_password("weak")
        >>> is_valid
        False
        >>> errors
        ['Password must be at least 8 characters long', ...]
    """
    errors = []
    
    # Check length
    if len(password) < PasswordPolicy.MIN_LENGTH:
        errors.append(f"Password must be at least {PasswordPolicy.MIN_LENGTH} characters long")
    
    if len(password) > PasswordPolicy.MAX_LENGTH:
        errors.append(f"Password must not exceed {PasswordPolicy.MAX_LENGTH} characters")
    
    # Check uppercase
    if PasswordPolicy.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check lowercase
    if PasswordPolicy.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check digit
    if PasswordPolicy.REQUIRE_DIGIT and not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    # Check special characters (optional)
    if PasswordPolicy.REQUIRE_SPECIAL:
        pattern = f'[{re.escape(PasswordPolicy.SPECIAL_CHARS)}]'
        if not re.search(pattern, password):
            errors.append("Password must contain at least one special character")
    
    # Check common weak passwords
    weak_passwords = [
        'password', '12345678', '123456789', 'qwerty123', 
        'admin123', 'letmein', 'welcome', 'password1'
    ]
    if password.lower() in weak_passwords:
        errors.append("Password is too common. Please choose a stronger password")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def get_password_strength(password: str) -> dict:
    """
    Đánh giá độ mạnh của mật khẩu.
    
    Returns:
        dict với score (0-100) và level (weak/medium/strong/very_strong)
    """
    score = 0
    
    # Length score
    length = len(password)
    if length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    
    # Character variety
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'\d', password):
        score += 15
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 15
    
    # Determine level
    if score < 40:
        level = "weak"
    elif score < 60:
        level = "medium"
    elif score < 80:
        level = "strong"
    else:
        level = "very_strong"
    
    return {
        "score": min(score, 100),
        "level": level
    }
