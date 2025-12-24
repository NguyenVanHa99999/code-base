from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.session import Base
import secrets
import string


def generate_user_code() -> str:
    """
    Generate a unique 10-character user code.
    Format: 2 letters + 8 alphanumeric characters (uppercase + digits)
    Example: AB1234CDEF
    """
    letters = string.ascii_uppercase
    alphanumeric = string.ascii_uppercase + string.digits
    
    # 2 chữ cái đầu + 8 ký tự alphanumeric
    code = ''.join(secrets.choice(letters) for _ in range(2))
    code += ''.join(secrets.choice(alphanumeric) for _ in range(8))
    return code


class User(Base):
    """
    User Model - Core user account information
    
    Fields:
    - id: Primary key
    - user_code: Unique 10-char identifier (auto-generated)
    - name: Display name
    - email: Unique email for authentication
    - hashed_password: Bcrypt hashed password
    - role_id: Foreign key to Role table
    - created_at: Account creation timestamp
    
    Relationships:
    - role: Many-to-one with Role
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_code = Column(String(10), unique=True, index=True, nullable=False, default=generate_user_code)
    name = Column(String(64), index=True)
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(256))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Relationship với Role
    role = relationship("Role", back_populates="users")
    
    @property
    def role_name(self) -> str:
        """Trả về tên role của user, mặc định là 'student' nếu chưa gán"""
        return self.role.name if self.role else "student"
    
    @property
    def is_admin(self) -> bool:
        """Kiểm tra user có phải admin không"""
        return self.role_name == "admin"
    
    @property
    def is_teacher(self) -> bool:
        """Kiểm tra user có phải teacher không"""
        return self.role_name == "teacher"
    
    @property
    def is_student(self) -> bool:
        """Kiểm tra user có phải student không"""
        return self.role_name == "student"
    
    def has_role(self, role_name: str) -> bool:
        """Kiểm tra user có role cụ thể không"""
        return self.role_name == role_name
    
    def has_any_role(self, role_names: list) -> bool:
        """Kiểm tra user có bất kỳ role nào trong danh sách không"""
        return self.role_name in role_names