from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError
from core.security import decode_access_token
from crud.user import get_user
from database.session import SessionLocal
import logging

logger = logging.getLogger(__name__)

COOKIE_NAME = "access_token"

# Paths that don't require authentication
IGNORE_PATHS = [
    "/api/docs",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/openapi.json",
    "/static",
    "/favicon.ico",
]


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT Authentication Middleware
    
    - Validates JWT token from HttpOnly cookie or Authorization header
    - Sets request.state.user for authenticated requests
    - Returns 401 for invalid/missing tokens
    """
    
    def __init__(self, app):
        super().__init__(app)

    def _get_token(self, request: Request) -> str | None:
        """Get token from cookie first, then Authorization header"""
        # Priority 1: HttpOnly cookie
        cookie_token = request.cookies.get(COOKIE_NAME)
        if cookie_token:
            return cookie_token
        
        # Priority 2: Authorization header (backward compatible)
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization.split(" ")[1]
        
        return None

    def _should_skip_auth(self, path: str) -> bool:
        """Check if path should skip authentication"""
        return any(path.startswith(ignore_path) for ignore_path in IGNORE_PATHS)

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for certain paths
        if self._should_skip_auth(request.url.path):
            return await call_next(request)
        
        # Get token
        token = self._get_token(request)
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
            )
        
        # Decode token
        payload = decode_access_token(token)
        if payload is None or "sub" not in payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"},
            )
        
        # Get user from database with proper session handling
        db = SessionLocal()
        try:
            user = get_user(db, int(payload["sub"]))
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )
        finally:
            db.close()
        
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User not found"},
            )
        
        # Set user in request state for use in routes
        request.state.user = user
        return await call_next(request)