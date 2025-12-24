# Code Base

Full-stack web application với FastAPI backend và Vue 3 frontend.

## Tổng quan

```
code-base/
├── backend/    # FastAPI + MySQL + Redis
└── frontend/   # Vue 3 + Vite + PrimeVue
```

## Yêu cầu hệ thống

- Docker & Docker Compose
- Ports trống: 8000, 5174, 3306, 6379

## Quick Start

### 1. Khởi động Backend

#### macOS / Linux

```bash
cd backend
chmod +x run-dev.sh    # Cấp quyền chạy (chỉ cần 1 lần)
./run-dev.sh
```

#### Windows (Git Bash / WSL)

```bash
cd backend
./run-dev.sh
```

> API: http://localhost:8000  
> Docs: http://localhost:8000/docs

### 2. Khởi động Frontend

#### macOS / Linux

```bash
cd frontend
chmod +x run-dev.sh    # Cấp quyền chạy (chỉ cần 1 lần)
./run-dev.sh
```

#### Windows (Git Bash / WSL)

```bash
cd frontend
./run-dev.sh
```

> App: http://localhost:5174

## Dừng servers

```bash
# Trong mỗi thư mục, chạy lại script để dừng
./run-dev.sh
```

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **MySQL** - Database
- **Redis** - Caching
- **JWT** - Authentication

### Frontend
- **Vue 3** - JavaScript framework
- **Vite** - Build tool
- **PrimeVue** - UI components
- **Pinia** - State management

## Ports

| Service | Port |
|---------|------|
| Backend API | 8000 |
| Frontend | 5174 |
| MySQL | 3306 |
| Redis | 6379 |

## Chi tiết

- [Backend README](./backend/app/README.md)
- [Frontend README](./frontend/README.md)
