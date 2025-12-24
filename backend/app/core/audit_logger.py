"""
Audit Logger Setup.

Setup logger với multiple handlers: Console, File, iCloud.
Sử dụng formatters từ audit_formatters.py
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta
from pathlib import Path

from core.audit_formatters import AuditLogFormatter, ColoredConsoleFormatter, VN_TZ


def setup_audit_logger() -> logging.Logger:
    """
    Setup audit logger with multiple handlers.
    
    Handlers:
    1. Console (colored output)
    2. Local file (JSON format, rotating)
    3. iCloud file (optional, for Mac)
    4. Error-only file (critical failures)
    
    Returns:
        logging.Logger: Configured audit logger
    """
    # Create logger
    logger = logging.getLogger('audit')
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory structure
    logs_dir = Path('/app/logs')  # In Docker container
    audit_logs_dir = logs_dir / 'audit'
    
    # For local development (outside Docker)
    if not logs_dir.exists():
        logs_dir = Path(__file__).parent.parent.parent / 'logs'
        audit_logs_dir = logs_dir / 'audit'
    
    # Create directories
    audit_logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for iCloud path (Mac local development)
    use_icloud = False
    icloud_path = Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'AI-Teaching-Assistant-Logs' / 'audit'
    if Path.home().exists() and not os.environ.get('DOCKER_CONTAINER'):
        try:
            icloud_path.mkdir(parents=True, exist_ok=True)
            use_icloud = True
        except Exception:
            use_icloud = False
    
    # 1. Console Handler (colored output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredConsoleFormatter())
    logger.addHandler(console_handler)
    
    # 2. Local File Handler (JSON format, rotating)
    local_log_file = audit_logs_dir / f'audit_{datetime.now(VN_TZ).strftime("%Y%m%d")}.log'
    file_handler = RotatingFileHandler(
        local_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB per file
        backupCount=30,  # Keep 30 days
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(AuditLogFormatter())
    logger.addHandler(file_handler)
    
    # 3. iCloud File Handler (if available)
    if use_icloud:
        icloud_log_file = icloud_path / f'audit_{datetime.now(VN_TZ).strftime("%Y%m%d")}.log'
        icloud_handler = RotatingFileHandler(
            icloud_log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=30,
            encoding='utf-8'
        )
        icloud_handler.setLevel(logging.INFO)
        icloud_handler.setFormatter(AuditLogFormatter())
        logger.addHandler(icloud_handler)
        logger.info(f"iCloud logging enabled: {icloud_path}")
    
    # 4. Error-only Handler
    error_log_file = audit_logs_dir / 'audit_errors.log'
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=10,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(AuditLogFormatter())
    logger.addHandler(error_handler)
    
    logger.info(f"Audit logging initialized: {audit_logs_dir}")
    
    return logger


def log_audit_event(
    action: str,
    user_email: str = None,
    resource_type: str = None,
    resource_id: int = None,
    ip_address: str = None,
    status_code: int = 200,
    message: str = None,
    level: str = 'INFO'
):
    """
    Log an audit event with structured data.
    
    Args:
        action: Action performed
        user_email: Email of user who performed action
        resource_type: Type of resource affected
        resource_id: ID of resource
        ip_address: Client IP address
        status_code: HTTP status code
        message: Custom message
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger = logging.getLogger('audit')
    
    # Create log record with extra fields
    extra = {
        'action': action,
        'user_email': user_email,
        'resource_type': resource_type,
        'resource_id': resource_id,
        'ip_address': ip_address,
        'status_code': status_code
    }
    
    # Build message
    if not message:
        message = f"Audit: {action}"
        if user_email:
            message += f" by {user_email}"
        if resource_type:
            message += f" on {resource_type}"
            if resource_id:
                message += f"#{resource_id}"
    
    # Log with appropriate level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, message, extra=extra)


# Initialize logger on module import
audit_logger = setup_audit_logger()


# Convenience functions
def log_info(message: str, **kwargs):
    """Log info level audit event"""
    log_audit_event(message=message, level='INFO', **kwargs)


def log_warning(message: str, **kwargs):
    """Log warning level audit event"""
    log_audit_event(message=message, level='WARNING', **kwargs)


def log_error(message: str, **kwargs):
    """Log error level audit event"""
    log_audit_event(message=message, level='ERROR', **kwargs)


def log_success(action: str, user_email: str = None, **kwargs):
    """Log successful action"""
    log_audit_event(
        action=action,
        user_email=user_email,
        status_code=kwargs.pop('status_code', 200),
        message=f"{action} completed successfully",
        level='INFO',
        **kwargs
    )


def log_failure(action: str, user_email: str = None, error: str = None, **kwargs):
    """Log failed action"""
    message = f"{action} failed"
    if error:
        message += f": {error}"
    
    log_audit_event(
        action=action,
        user_email=user_email,
        status_code=kwargs.pop('status_code', 500),
        message=message,
        level='ERROR',
        **kwargs
    )
