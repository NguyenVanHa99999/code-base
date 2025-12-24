# Backend API

FastAPI backend với MySQL, Redis và JWT authentication.

## Yêu cầu

- Docker & Docker Compose
- Port 8000 trống

## Khởi động

### macOS / Linux

```bash
cd backend
chmod +x run-dev.sh    # Cấp quyền chạy (chỉ cần 1 lần)
./run-dev.sh
```

### Windows (Git Bash / WSL)

```bash
cd backend
./run-dev.sh
```

> Script sẽ tự động:
> - Khởi động MySQL, Redis, API containers
> - Tạo bảng database
> - Seed dữ liệu mặc định

## Dừng server

```bash
./run-dev.sh  # Chạy lại để dừng
```

## API Endpoints

| Endpoint | Mô tả |
|----------|-------|
| `GET /` | Health check |
| `POST /auth/login` | Đăng nhập |
| `POST /auth/register` | Đăng ký |
| `GET /api/users/me` | Thông tin user (JWT) |

**API Docs:** http://localhost:8000/docs

## Cấu trúc thư mục

```
app/
├── core/          # Config, Middleware, JWT
├── routes/        # API endpoints
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
├── crud/          # Database operations
└── main.py        # Entry point
```

## Environment Variables

| Biến | Mô tả |
|------|-------|
| `DB_HOST` | MySQL host |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `SECRET_KEY` | JWT secret key |
| `REDIS_HOST` | Redis host |

## Ports

| Service | Port |
|---------|------|
| API | 8000 |
| MySQL | 3306 |
| Redis | 6379 |
