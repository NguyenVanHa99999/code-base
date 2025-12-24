from models.audit_log import AuditAction


def map_request_to_action(method: str, path: str) -> AuditAction:
    """
    Map HTTP method and path to AuditAction enum.
    
    This comprehensive mapping ensures 100% coverage for all endpoints.
    Order matters - more specific patterns should come first!
    """
    # Health check endpoints (check first for performance)
    if path == "/health" or path == "/healthz" or "/health" in path:
        return AuditAction.HEALTH_CHECK
    
    # Auth endpoints
    if "/auth/" in path or path.startswith("/auth"):
        if "/login" in path:
            return AuditAction.LOGIN
        if "/logout" in path:
            return AuditAction.LOGOUT
        if "/create" in path:
            return AuditAction.REGISTER
        if "/check-email" in path:
            return AuditAction.EMAIL_CHECK
        return AuditAction.API_REQUEST
    
    # Document endpoints
    if "/documents" in path:
        if "/trash" in path:
            if "/cleanup" in path:
                return AuditAction.TRASH_CLEANUP
            return AuditAction.TRASH_VIEW
        if "/restore" in path:
            return AuditAction.DOCUMENT_RESTORE
        if "/move" in path:
            return AuditAction.DOCUMENT_MOVE
        if "/process" in path:
            return AuditAction.DOCUMENT_PROCESS
        if "/download" in path:
            if method == "DELETE":
                return AuditAction.CACHE_CLEAR
            return AuditAction.DOCUMENT_DOWNLOAD
        if method == "POST":
            if "/upload" in path:
                return AuditAction.DOCUMENT_UPLOAD
            return AuditAction.DOCUMENT_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.DOCUMENT_UPDATE
        elif method == "DELETE":
            return AuditAction.DOCUMENT_DELETE
        elif method == "GET":
            return AuditAction.DOCUMENT_VIEW
    
    # File endpoints
    if "/files" in path:
        if method == "POST" and "/upload" in path:
            return AuditAction.FILE_UPLOAD
        elif method == "GET" and "/list" in path:
            return AuditAction.FILE_LIST
        elif method == "DELETE":
            return AuditAction.FILE_DELETE
        elif method == "GET":
            return AuditAction.DOCUMENT_VIEW
    
    # Folder endpoints
    if "/folders" in path:
        if "/trash" in path:
            if "/cleanup" in path:
                return AuditAction.TRASH_CLEANUP
            return AuditAction.TRASH_VIEW
        if "/tree" in path:
            return AuditAction.FOLDER_VIEW
        if "/restore" in path:
            return AuditAction.FOLDER_RESTORE
        if "/move" in path:
            return AuditAction.FOLDER_MOVE
        if method == "POST":
            return AuditAction.FOLDER_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.FOLDER_UPDATE
        elif method == "DELETE":
            return AuditAction.FOLDER_DELETE
        elif method == "GET":
            return AuditAction.FOLDER_VIEW
    
    # Folder contents endpoints
    if "/contents" in path:
        return AuditAction.FOLDER_CONTENTS_VIEW
    
    # Calendar/Event endpoints
    if "/calendar" in path or "/events" in path:
        if "/check-overlap" in path:
            return AuditAction.EVENT_CHECK_OVERLAP
        if method == "POST":
            return AuditAction.EVENT_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.EVENT_UPDATE
        elif method == "DELETE":
            return AuditAction.EVENT_DELETE
        elif method == "GET":
            return AuditAction.EVENT_VIEW
    
    # User endpoints
    if "/users" in path:
        if method == "POST":
            return AuditAction.USER_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.USER_UPDATE
        elif method == "DELETE":
            return AuditAction.USER_DELETE
        elif method == "GET":
            return AuditAction.USER_VIEW
    
    # Notification endpoints
    if "/notifications" in path:
        if "/status" in path or "/respond-status" in path or "/general-status" in path:
            return AuditAction.NOTIFICATION_STATUS_UPDATE
        if "/stats" in path:
            return AuditAction.STATS_VIEW
        if method == "POST":
            return AuditAction.NOTIFICATION_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.NOTIFICATION_UPDATE
        elif method == "DELETE":
            return AuditAction.NOTIFICATION_DELETE
        elif method == "GET":
            return AuditAction.NOTIFICATION_READ
    
    # Template endpoints
    if "/templates" in path:
        if "/preview" in path:
            return AuditAction.TEMPLATE_PREVIEW
        if method == "POST":
            return AuditAction.TEMPLATE_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.TEMPLATE_UPDATE
        elif method == "DELETE":
            return AuditAction.TEMPLATE_DELETE
        elif method == "GET":
            return AuditAction.TEMPLATE_VIEW
    
    # Message endpoints
    if "/messages" in path:
        if "/search" in path:
            return AuditAction.MESSAGE_SEARCH
        if "/count" in path:
            return AuditAction.MESSAGE_READ
        if method == "POST":
            return AuditAction.MESSAGE_SEND
        elif method in ["PUT", "PATCH"]:
            return AuditAction.MESSAGE_UPDATE
        elif method == "DELETE":
            return AuditAction.MESSAGE_DELETE
        elif method == "GET":
            return AuditAction.MESSAGE_READ
    
    # Settings endpoints
    if "/settings" in path and method in ["PUT", "PATCH"]:
        return AuditAction.SETTINGS_UPDATE
    
    # Reminder endpoints
    if "/reminder" in path:
        if "/process" in path or "/send_reminder" in path:
            return AuditAction.REMINDER_PROCESS
        if method == "POST":
            return AuditAction.REMINDER_CREATE
        elif method in ["PUT", "PATCH"]:
            return AuditAction.REMINDER_UPDATE
        elif method == "DELETE":
            return AuditAction.REMINDER_DELETE
        elif method == "GET":
            return AuditAction.REMINDER_VIEW
    
    # Trash endpoints
    if "/trash" in path:
        if "/restore" in path.lower():
            return AuditAction.TRASH_RESTORE
        elif "/cleanup" in path:
            return AuditAction.TRASH_CLEANUP
        elif method == "DELETE":
            return AuditAction.TRASH_PERMANENT_DELETE
        elif method == "GET":
            return AuditAction.TRASH_VIEW
    
    # Statistics/Analytics endpoints
    if "/stats" in path or "/analytics" in path or "/report" in path:
        if method == "GET":
            return AuditAction.STATS_VIEW
        elif method == "POST":
            return AuditAction.REPORT_GENERATE
    
    # Audit log endpoints
    if "/audit" in path or "/audit-logs" in path:
        return AuditAction.AUDIT_VIEW
    
    # Info endpoints
    if "/info" in path or "/server-time" in path:
        return AuditAction.INFO_VIEW
    
    if "/clear-cache" in path:
        return AuditAction.CACHE_CLEAR
    
    if "/validate-file" in path:
        return AuditAction.FILE_VALIDATE
    
    # Root and version endpoints
    if path in ["/", "/version"]:
        return AuditAction.SYSTEM_ACCESS
    
    # Generic fallback
    return AuditAction.API_REQUEST
