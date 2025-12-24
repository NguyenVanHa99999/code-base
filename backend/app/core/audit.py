"""
Audit Helpers - Backward Compatible Exports.

File này giữ lại để backward compatible với code cũ.
Logic đã được chuyển sang services/audit_service.py
"""

# Re-export từ audit_service để backward compatible
from services.audit_service import (
    extract_client_info,
    log_action,
    log_auth_action,
    log_resource_action,
    log_failed_action
)

# Re-export từ audit_logger
from core.audit_logger import (
    log_audit_event,
    log_success,
    log_failure,
    log_info,
    log_warning,
    log_error
)

__all__ = [
    # From audit_service
    'extract_client_info',
    'log_action',
    'log_auth_action',
    'log_resource_action',
    'log_failed_action',
    # From audit_logger
    'log_audit_event',
    'log_success',
    'log_failure',
    'log_info',
    'log_warning',
    'log_error',
]
