from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database.session import Base
from datetime import datetime, timezone, timedelta
import enum

# Vietnam timezone (UTC+7)
VN_TZ = timezone(timedelta(hours=7))


class AuditAction(str, enum.Enum):
    """Enum for audit action types"""
    # Authentication actions
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    REGISTER = "REGISTER"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    
    # User actions
    USER_CREATE = "USER_CREATE"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
    USER_VIEW = "USER_VIEW"
    
    # Document actions
    DOCUMENT_CREATE = "DOCUMENT_CREATE"
    DOCUMENT_UPDATE = "DOCUMENT_UPDATE"
    DOCUMENT_DELETE = "DOCUMENT_DELETE"
    DOCUMENT_VIEW = "DOCUMENT_VIEW"
    DOCUMENT_DOWNLOAD = "DOCUMENT_DOWNLOAD"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    DOCUMENT_RESTORE = "DOCUMENT_RESTORE"
    
    # Folder actions
    FOLDER_CREATE = "FOLDER_CREATE"
    FOLDER_UPDATE = "FOLDER_UPDATE"
    FOLDER_DELETE = "FOLDER_DELETE"
    FOLDER_VIEW = "FOLDER_VIEW"
    
    # Event/Calendar actions
    EVENT_CREATE = "EVENT_CREATE"
    EVENT_UPDATE = "EVENT_UPDATE"
    EVENT_DELETE = "EVENT_DELETE"
    EVENT_VIEW = "EVENT_VIEW"
    
    # Notification actions
    NOTIFICATION_CREATE = "NOTIFICATION_CREATE"
    NOTIFICATION_READ = "NOTIFICATION_READ"
    NOTIFICATION_DELETE = "NOTIFICATION_DELETE"
    
    # Template actions
    TEMPLATE_CREATE = "TEMPLATE_CREATE"
    TEMPLATE_UPDATE = "TEMPLATE_UPDATE"
    TEMPLATE_DELETE = "TEMPLATE_DELETE"
    TEMPLATE_USE = "TEMPLATE_USE"
    
    # Message actions
    MESSAGE_SEND = "MESSAGE_SEND"
    MESSAGE_READ = "MESSAGE_READ"
    MESSAGE_DELETE = "MESSAGE_DELETE"
    
    # System actions
    SETTINGS_UPDATE = "SETTINGS_UPDATE"
    EXPORT_DATA = "EXPORT_DATA"
    IMPORT_DATA = "IMPORT_DATA"
    
    # Access control
    PERMISSION_GRANT = "PERMISSION_GRANT"
    PERMISSION_REVOKE = "PERMISSION_REVOKE"
    
    # Reminder actions
    REMINDER_CREATE = "REMINDER_CREATE"
    REMINDER_UPDATE = "REMINDER_UPDATE"
    REMINDER_DELETE = "REMINDER_DELETE"
    REMINDER_VIEW = "REMINDER_VIEW"
    REMINDER_PROCESS = "REMINDER_PROCESS"
    
    # Trash actions
    TRASH_VIEW = "TRASH_VIEW"
    TRASH_RESTORE = "TRASH_RESTORE"
    TRASH_PERMANENT_DELETE = "TRASH_PERMANENT_DELETE"
    TRASH_CLEANUP = "TRASH_CLEANUP"
    
    # Statistics/Analytics actions
    STATS_VIEW = "STATS_VIEW"
    REPORT_GENERATE = "REPORT_GENERATE"
    
    # System access and health
    SYSTEM_ACCESS = "SYSTEM_ACCESS"
    HEALTH_CHECK = "HEALTH_CHECK"
    
    # Notification extended actions
    NOTIFICATION_UPDATE = "NOTIFICATION_UPDATE"
    NOTIFICATION_STATUS_UPDATE = "NOTIFICATION_STATUS_UPDATE"
    
    # Document extended actions
    DOCUMENT_MOVE = "DOCUMENT_MOVE"
    DOCUMENT_PROCESS = "DOCUMENT_PROCESS"
    
    # Folder extended actions
    FOLDER_RESTORE = "FOLDER_RESTORE"
    FOLDER_MOVE = "FOLDER_MOVE"
    
    # Message extended actions
    MESSAGE_UPDATE = "MESSAGE_UPDATE"
    MESSAGE_SEARCH = "MESSAGE_SEARCH"
    
    # Template extended actions
    TEMPLATE_VIEW = "TEMPLATE_VIEW"
    TEMPLATE_PREVIEW = "TEMPLATE_PREVIEW"
    
    # File actions
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_LIST = "FILE_LIST"
    FILE_DELETE = "FILE_DELETE"
    
    # Audit actions
    AUDIT_VIEW = "AUDIT_VIEW"
    
    # Info/Cache actions
    INFO_VIEW = "INFO_VIEW"
    CACHE_CLEAR = "CACHE_CLEAR"
    FILE_VALIDATE = "FILE_VALIDATE"
    
    # Auth extended actions
    EMAIL_CHECK = "EMAIL_CHECK"
    
    # Event extended actions
    EVENT_CHECK_OVERLAP = "EVENT_CHECK_OVERLAP"
    
    # Folder contents
    FOLDER_CONTENTS_VIEW = "FOLDER_CONTENTS_VIEW"
    
    # Generic fallback - captures ALL unmapped requests for 100% coverage
    API_REQUEST = "API_REQUEST"


class AuditLog(Base):
    """
    Audit Log table - Immutable record of all user actions
    
    Fields:
    - id: Primary key
    - user_id: Who performed the action (nullable for system actions)
    - action: What action was performed (enum)
    - resource_type: Type of resource affected (document, user, event, etc.)
    - resource_id: ID of the affected resource
    - details: Additional JSON data about the action
    - ip_address: Client IP address
    - user_agent: Browser/client user agent
    - request_method: HTTP method (GET, POST, PUT, DELETE)
    - request_path: API endpoint path
    - status_code: HTTP response status code
    - error_message: Error message if action failed
    - created_at: Timestamp of the action
    """
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # WHO - User information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    user_email = Column(String(120), nullable=True)  # Denormalized for historical record
    
    # WHAT - Action information
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    resource_type = Column(String(50), nullable=True, index=True)  # document, user, event, etc.
    resource_id = Column(Integer, nullable=True)
    
    # HOW - Technical details
    request_method = Column(String(10), nullable=True)  # GET, POST, PUT, DELETE
    request_path = Column(String(255), nullable=True)
    status_code = Column(Integer, nullable=True)
    
    # WHERE - Client information
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    
    # Additional context
    details = Column(JSON, nullable=True)  # Flexible JSON field for action-specific data
    error_message = Column(Text, nullable=True)  # For failed actions
    
    # WHEN - Timestamp (Vietnam timezone UTC+7)
    created_at = Column(DateTime, default=lambda: datetime.now(VN_TZ), nullable=False, index=True)
    
    # Relationship
    user = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, user={self.user_email}, action={self.action}, resource={self.resource_type}:{self.resource_id})>"
