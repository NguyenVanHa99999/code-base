from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from database.session import SessionLocal
from core.audit import extract_client_info
from core.audit_action_mapping import map_request_to_action
from crud.audit_log import create_audit_log
from core.audit_logger import log_audit_event
import logging
import time

logger = logging.getLogger(__name__)


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically audit all HTTP requests
    
    This middleware:
    1. Captures request details (method, path, IP, user agent)
    2. Tracks response status code
    3. Records timing information
    4. Logs to audit_logs table
    """
    
    # Paths to skip auditing (reduces noise)
    SKIP_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/static",
        "/favicon.ico",
    ]
    
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Check if path should be skipped
        if any(request.url.path.startswith(path) for path in self.SKIP_PATHS):
            return await call_next(request)
        
        # Start timing
        start_time = time.time()
        
        # Extract client info
        ip_address, user_agent = extract_client_info(request)
        
        # Get user info if available (set by JWTAuthMiddleware)
        user_id = None
        user_email = None
        if hasattr(request.state, 'user') and request.state.user:
            user_id = request.state.user.id
            user_email = request.state.user.email
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Create audit log entry
        try:
            self._log_request(
                request=request,
                response=response,
                user_id=user_id,
                user_email=user_email,
                ip_address=ip_address,
                user_agent=user_agent,
                duration_ms=duration_ms
            )
        except Exception as e:
            # Don't fail the request if audit logging fails
            logger.error(f"Audit middleware error: {e}")
        
        return response
    
    def _log_request(
        self,
        request: Request,
        response,
        user_id: int,
        user_email: str,
        ip_address: str,
        user_agent: str,
        duration_ms: float
    ):
        """Log request to database and audit logger"""
        db = SessionLocal()
        try:
            # Map HTTP method to action
            action = map_request_to_action(request.method, request.url.path)
            
            # Create audit log in database
            create_audit_log(
                db=db,
                user_id=user_id,
                user_email=user_email,
                action=action,
                request_method=request.method,
                request_path=str(request.url.path),
                status_code=response.status_code,
                ip_address=ip_address,
                user_agent=user_agent,
                details={"duration_ms": round(duration_ms, 2)}
            )
            
            # Log to audit logger (console + file + iCloud)
            log_audit_event(
                action=action.value,
                user_email=user_email,
                ip_address=ip_address,
                status_code=response.status_code,
                message=f"{request.method} {request.url.path} ({duration_ms:.2f}ms)",
                level='INFO' if response.status_code < 400 else 'WARNING'
            )
        finally:
            db.close()
