"""
Audit Service.

Business logic layer cho Audit Log.
Gộp các helper functions từ core/audit.py theo đúng pattern service layer.
"""

from sqlalchemy.orm import Session
from fastapi import Request
from typing import Optional, Dict, Any
import logging

from models.audit_log import AuditAction
from models.user import User
from crud.audit_log import create_audit_log
from core.audit_logger import log_audit_event, log_success, log_failure

logger = logging.getLogger(__name__)


def extract_client_info(request: Request) -> tuple:
    """
    Extract client IP and user agent from request.
    
    Handles proxy headers (X-Forwarded-For, X-Real-IP).
    
    Args:
        request: FastAPI Request object
        
    Returns:
        Tuple of (ip_address, user_agent)
    """
    # Get client IP - handle proxy headers
    ip_address = None
    if request.client:
        ip_address = request.client.host
    
    # Check for X-Forwarded-For header (proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[0].strip()
    
    # Check for X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        ip_address = real_ip
    
    # Get user agent
    user_agent = request.headers.get("User-Agent", "Unknown")
    
    return ip_address, user_agent


def log_action(
    db: Session,
    request: Request,
    action: AuditAction,
    user: Optional[User] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 200,
    error_message: Optional[str] = None
) -> None:
    """
    Log a user action to the audit log (DB + File).
    
    Args:
        db: Database session
        request: FastAPI Request object
        action: Type of action (from AuditAction enum)
        user: User who performed the action (None for anonymous)
        resource_type: Type of resource affected
        resource_id: ID of the resource
        details: Additional context as JSON
        status_code: HTTP status code
        error_message: Error message if action failed
    """
    try:
        # Extract client info
        ip_address, user_agent = extract_client_info(request)
        
        # Create audit log entry in DB
        create_audit_log(
            db=db,
            user_id=user.id if user else None,
            user_email=user.email if user else None,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            request_method=request.method,
            request_path=str(request.url.path),
            status_code=status_code,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            error_message=error_message
        )
        
        # Log to file with structured data
        if status_code < 400:
            log_success(
                action=action.value,
                user_email=user.email if user else None,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                status_code=status_code
            )
        else:
            log_failure(
                action=action.value,
                user_email=user.email if user else None,
                error=error_message,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                status_code=status_code
            )
        
    except Exception as e:
        # Don't fail the main operation if audit logging fails
        logger.error(f"Failed to create audit log: {e}")


def log_auth_action(
    db: Session,
    request: Request,
    action: AuditAction,
    email: str,
    success: bool = True,
    error_message: Optional[str] = None
) -> None:
    """
    Log authentication-related actions (login, logout, register).
    
    Args:
        db: Database session
        request: FastAPI Request object
        action: Auth action type
        email: User email
        success: Whether the action succeeded
        error_message: Error message if failed
    """
    ip_address, user_agent = extract_client_info(request)
    
    try:
        create_audit_log(
            db=db,
            user_id=None,  # User might not be authenticated yet
            user_email=email,
            action=action,
            request_method=request.method,
            request_path=str(request.url.path),
            status_code=200 if success else 401,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"success": success},
            error_message=error_message
        )
        
        # Log authentication events
        if success:
            log_success(
                action=action.value,
                user_email=email,
                ip_address=ip_address,
                status_code=200
            )
        else:
            log_failure(
                action=action.value,
                user_email=email,
                error=error_message,
                ip_address=ip_address,
                status_code=401
            )
        
    except Exception as e:
        logger.error(f"Failed to log auth action: {e}")


def log_resource_action(
    db: Session,
    request: Request,
    user: User,
    action: AuditAction,
    resource_type: str,
    resource_id: int,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Convenient helper for logging resource-specific actions.
    
    Args:
        db: Database session
        request: FastAPI Request object
        user: User performing the action
        action: Action type
        resource_type: Type of resource
        resource_id: ID of the resource
        details: Additional context
    """
    log_action(
        db=db,
        request=request,
        action=action,
        user=user,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details
    )


def log_failed_action(
    db: Session,
    request: Request,
    action: AuditAction,
    user: Optional[User],
    error_message: str,
    status_code: int = 500
) -> None:
    """
    Log a failed action.
    
    Args:
        db: Database session
        request: FastAPI Request object
        action: Action that failed
        user: User who attempted the action
        error_message: Error description
        status_code: HTTP error code
    """
    log_action(
        db=db,
        request=request,
        action=action,
        user=user,
        status_code=status_code,
        error_message=error_message
    )
