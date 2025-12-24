from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from models.audit_log import AuditLog, AuditAction
from typing import List, Optional
from datetime import datetime, timedelta


def create_audit_log(
    db: Session,
    user_id: Optional[int],
    user_email: Optional[str],
    action: AuditAction,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    request_method: Optional[str] = None,
    request_path: Optional[str] = None,
    status_code: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None,
    error_message: Optional[str] = None
) -> AuditLog:
    """
    Create a new audit log entry
    
    Args:
        db: Database session
        user_id: ID of the user who performed the action
        user_email: Email of the user (denormalized for historical record)
        action: Type of action performed (from AuditAction enum)
        resource_type: Type of resource affected (optional)
        resource_id: ID of the resource (optional)
        request_method: HTTP method (optional)
        request_path: API endpoint path (optional)
        status_code: HTTP response status (optional)
        ip_address: Client IP address (optional)
        user_agent: Client user agent (optional)
        details: Additional JSON data (optional)
        error_message: Error message if action failed (optional)
        
    Returns:
        Created AuditLog object
    """
    audit_log = AuditLog(
        user_id=user_id,
        user_email=user_email,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        request_method=request_method,
        request_path=request_path,
        status_code=status_code,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        error_message=error_message
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log


def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    action: Optional[AuditAction] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[AuditLog]:
    """
    Get audit logs with optional filters
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        user_id: Filter by user ID
        action: Filter by action type
        resource_type: Filter by resource type
        resource_id: Filter by resource ID
        start_date: Filter by start date
        end_date: Filter by end date
        
    Returns:
        List of AuditLog objects
    """
    query = db.query(AuditLog)
    
    # Apply filters
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    
    if action is not None:
        query = query.filter(AuditLog.action == action)
    
    if resource_type is not None:
        query = query.filter(AuditLog.resource_type == resource_type)
    
    if resource_id is not None:
        query = query.filter(AuditLog.resource_id == resource_id)
    
    if start_date is not None:
        query = query.filter(AuditLog.created_at >= start_date)
    
    if end_date is not None:
        query = query.filter(AuditLog.created_at <= end_date)
    
    # Order by most recent first
    query = query.order_by(desc(AuditLog.created_at))
    
    # Pagination
    return query.offset(skip).limit(limit).all()


def get_audit_log_by_id(db: Session, audit_id: int) -> Optional[AuditLog]:
    """Get a specific audit log by ID"""
    return db.query(AuditLog).filter(AuditLog.id == audit_id).first()


def get_user_activity(db: Session, user_id: int, days: int = 30, limit: int = 100) -> List[AuditLog]:
    """
    Get recent activity for a specific user
    
    Args:
        db: Database session
        user_id: User ID
        days: Number of days to look back (default: 30)
        limit: Maximum number of records
        
    Returns:
        List of recent AuditLog entries for the user
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    return db.query(AuditLog).filter(
        and_(
            AuditLog.user_id == user_id,
            AuditLog.created_at >= start_date
        )
    ).order_by(desc(AuditLog.created_at)).limit(limit).all()


def get_resource_history(
    db: Session,
    resource_type: str,
    resource_id: int,
    limit: int = 100
) -> List[AuditLog]:
    """
    Get all actions performed on a specific resource
    
    Args:
        db: Database session
        resource_type: Type of resource
        resource_id: ID of the resource
        limit: Maximum number of records
        
    Returns:
        List of AuditLog entries for the resource
    """
    return db.query(AuditLog).filter(
        and_(
            AuditLog.resource_type == resource_type,
            AuditLog.resource_id == resource_id
        )
    ).order_by(desc(AuditLog.created_at)).limit(limit).all()


def get_failed_actions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None
) -> List[AuditLog]:
    """
    Get failed actions (status code >= 400)
    
    Args:
        db: Database session
        skip: Pagination offset
        limit: Maximum records
        user_id: Optional user filter
        
    Returns:
        List of failed audit log entries
    """
    query = db.query(AuditLog).filter(AuditLog.status_code >= 400)
    
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    
    return query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()


def get_audit_statistics(db: Session, days: int = 30) -> dict:
    """
    Get audit statistics for the specified period
    
    Args:
        db: Database session
        days: Number of days to analyze
        
    Returns:
        Dictionary with statistics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    total_actions = db.query(AuditLog).filter(
        AuditLog.created_at >= start_date
    ).count()
    
    failed_actions = db.query(AuditLog).filter(
        and_(
            AuditLog.created_at >= start_date,
            AuditLog.status_code >= 400
        )
    ).count()
    
    unique_users = db.query(AuditLog.user_id).filter(
        AuditLog.created_at >= start_date
    ).distinct().count()
    
    return {
        "period_days": days,
        "total_actions": total_actions,
        "failed_actions": failed_actions,
        "success_rate": ((total_actions - failed_actions) / total_actions * 100) if total_actions > 0 else 0,
        "unique_users": unique_users
    }
