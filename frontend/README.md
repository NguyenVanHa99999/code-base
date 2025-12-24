# Frontend

Vue 3 + Vite + PrimeVue frontend.

## Yêu cầu

- Docker & Docker Compose
- Port 5174 trống

## Khởi động

### macOS / Linux

```bash
cd frontend
chmod +x run-dev.sh    # Cấp quyền chạy (chỉ cần 1 lần)
./run-dev.sh
```

### Windows (Git Bash / WSL)

```bash
cd frontend
./run-dev.sh
```

> Frontend sẽ chạy tại: http://localhost:5174

## Dừng server

```bash
./run-dev.sh  # Chạy lại để dừng
```

## Tech Stack

| Công nghệ | Mô tả |
|-----------|-------|
| Vue 3 | Framework |
| Vite | Build tool |
| PrimeVue | UI Components |
| Pinia | State management |
| Vue Router | Routing |
| Axios | HTTP client |

## Cấu trúc thư mục

```
src/
├── api/           # API calls
├── assets/        # Static files
├── composables/   # Vue composables
├── layouts/       # Page layouts
├── plugins/       # Vue plugins
├── router/        # Routes config
├── stores/        # Pinia stores
├── utils/         # Helper functions
└── views/         # Page components
```

## Environment Variables

| Biến | Mô tả |
|------|-------|
| `VITE_API_URL` | Backend API URL |

## Scripts

```bash
npm run dev      # Dev server
npm run build    # Production build
npm run lint     # Lint code
npm run format   # Format code
```
