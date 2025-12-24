from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Route imports
from routes import auth
from routes.api import user

# Middleware imports
from core.jwt_middleware import JWTAuthMiddleware
from core.rate_limit import RateLimitMiddleware
from core.audit_middleware import AuditMiddleware


# APP INITIALIZATION

app = FastAPI(title="Backend API", version="1.0.0")

protected_app = FastAPI(
    title="Protected API",
    description="JWT-protected endpoints",
    version="1.0.0",
    docs_url="/docs",
)



# MIDDLEWARE CONFIGURATION

# CORS settings - 3 Frontend Portals
ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Admin
    "http://localhost:5174",   # Teacher
    "http://localhost:5175",   # Student
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

# Apply middlewares (order matters: first added = outermost)
# Protected app: JWT → Audit → RateLimit → CORS
protected_app.add_middleware(JWTAuthMiddleware)
protected_app.add_middleware(AuditMiddleware)
protected_app.add_middleware(RateLimitMiddleware, requests_per_second=20)
protected_app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main app: Audit → RateLimit → CORS
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_second=20)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTER MOUNTING

# Protected routes (require JWT)
protected_app.include_router(user.router, prefix="/users", tags=["users"])

# Public routes (no JWT required)
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Mount protected app under /api
app.mount("/api", protected_app)


# ROOT ENDPOINT

@app.get("/")
def read_root():
    return {"message": "Backend API - Ready", "version": "1.0.0"}