from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database.session import Base


class Role(Base):
    """
    Role Model - Định nghĩa các vai trò trong hệ thống
    
    Roles:
    - admin: Quản trị viên - Full quyền hệ thống
    - teacher: Giảng viên - Quản lý nội dung, sinh viên
    - student: Sinh viên - Xem nội dung, nộp bài
    
    Fields:
    - id: Primary key
    - name: Tên role (unique, e.g., 'admin', 'teacher', 'student')
    - display_name: Tên hiển thị (e.g., 'Quản trị viên', 'Giảng viên')
    - description: Mô tả chi tiết về role
    - is_active: Role có đang hoạt động không
    - created_at: Thời gian tạo
    
    Relationships:
    - users: One-to-many với User
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Relationship với User
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


# Default roles để seed vào database
DEFAULT_ROLES = [
    {
        "name": "admin",
        "display_name": "Quản trị viên",
        "description": "Full quyền quản lý hệ thống, users, và tất cả tài nguyên"
    },
    {
        "name": "teacher", 
        "display_name": "Giảng viên",
        "description": "Quản lý nội dung giảng dạy, theo dõi sinh viên, tạo bài tập"
    },
    {
        "name": "student",
        "display_name": "Sinh viên", 
        "description": "Xem nội dung học tập, nộp bài tập, tham gia lớp học"
    }
]
