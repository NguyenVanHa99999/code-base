"""
Audit Log Formatters.

Tách riêng các formatter để giảm complexity của audit_logger.py
và dễ dàng mở rộng format mới.
"""

import logging
import json
from datetime import datetime, timezone, timedelta

# Vietnam timezone (UTC+7)
VN_TZ = timezone(timedelta(hours=7))


class AuditLogFormatter(logging.Formatter):
    """Custom formatter for audit logs with structured JSON output"""
    
    def format(self, record):
        """Format log record with structured data"""
        # Base format with Vietnam timezone
        log_data = {
            'timestamp': datetime.now(VN_TZ).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        
        # Add extra fields if available
        extra_fields = ['user_email', 'action', 'resource_type', 'resource_id', 'ip_address', 'status_code']
        for field in extra_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredConsoleFormatter(logging.Formatter):
    """Colored formatter for console output with Vietnam timezone"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        """Format with colors for console"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Build message with color (Vietnam timezone)
        timestamp = datetime.now(VN_TZ).strftime('%Y-%m-%d %H:%M:%S')
        level = f"{color}[{record.levelname}]{reset}"
        
        # Extract audit info if available
        audit_info = ""
        if hasattr(record, 'user_email') and record.user_email:
            audit_info += f" user:{record.user_email}"
        if hasattr(record, 'action') and record.action:
            audit_info += f" action:{record.action}"
        if hasattr(record, 'status_code') and record.status_code:
            status_marker = "OK" if record.status_code < 400 else "FAIL"
            audit_info += f" [{status_marker}] {record.status_code}"
        
        message = f"{timestamp} {level} {record.getMessage()}{audit_info}"
        
        return message
