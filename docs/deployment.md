# FIREGUARD X — Deployment Guide

## Local Development Execution

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Backend Service
```bash
# Clone and enter directory
cd c:/Users/WELCOME/datascienceDS

# Install Python requirements
pip install -r requirements.txt

# Run dataset preparation & model training
python scripts/prepare_dataset.py
python ml/train.py

# Launch FastAPI development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- API Health: `http://localhost:8000/api/health`
- Swagger UI: `http://localhost:8000/docs`

### 2. Frontend Application
```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

## Containerized Deployment (Docker & Compose)

```bash
# Build and run containers
docker-compose up --build -d

# Check running status
docker-compose ps

# Stop containers
docker-compose down
```

---

## Production Cloud Deployment Recommendation
- **Frontend**: Deploy static bundle (`frontend/dist`) to Vercel, Netlify, or AWS S3 + CloudFront.
- **Backend**: Deploy containerized FastAPI application to Render, Railway, Google Cloud Run, or AWS ECS.
- **Database**: Set `DATABASE_URL=postgresql://user:password@host:5432/fireguard` in environment variables for managed PostgreSQL.
