from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from models.audit_log import AuditAction


class AuditLogBase(BaseModel):
    """Base audit log schema"""
    action: AuditAction
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log (internal use)"""
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    request_method: Optional[str] = None
    request_path: Optional[str] = None
    status_code: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    error_message: Optional[str] = None


class AuditLogRead(AuditLogBase):
    """Schema for reading an audit log"""
    id: int
    user_id: Optional[int]
    user_email: Optional[str]
    request_method: Optional[str]
    request_path: Optional[str]
    status_code: Optional[int]
    ip_address: Optional[str]
    user_agent: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AuditLogFilter(BaseModel):
    """Schema for filtering audit logs"""
    user_id: Optional[int] = None
    action: Optional[AuditAction] = None
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class AuditLogStatistics(BaseModel):
    """Schema for audit log statistics"""
    period_days: int
    total_actions: int
    failed_actions: int
    success_rate: float
    unique_users: int
