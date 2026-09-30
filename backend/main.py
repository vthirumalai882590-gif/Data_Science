"""
FIREGUARD X - Main Application Entrypoint
FastAPI Backend orchestrating Data Science pipelines, spatial digital twin,
counterfactual what-if simulations, and explainable AI services.
"""

import os
import sys
from contextlib import asynccontextmanager

# Ensure repository root and backend directory are in sys.path
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURR_DIR)
for path in [CURR_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

BASE_DIR = PARENT_DIR if os.path.exists(os.path.join(PARENT_DIR, "models")) else CURR_DIR

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.database.database import engine, Base, SessionLocal
from backend.database.repository import seed_zones_if_empty
from ml.model_registry import get_registry

# Import API Routers
from backend.api.health import router as health_router
from backend.api.dashboard import router as dashboard_router
from backend.api.prediction import router as prediction_router
from backend.api.zones import router as zones_router
from backend.api.simulation import router as simulation_router
from backend.api.models import router as models_router
from backend.api.reports import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence:
    print("[FIREGUARD X] Initializing SQLite database schema...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("[FIREGUARD X] Seeding spatial forest zones...")
        seed_zones_if_empty(db)
    finally:
        db.close()

    print("[FIREGUARD X] Pre-warming machine learning models into memory...")
    registry = get_registry()
    print(f"[FIREGUARD X] Loaded primary model: {registry.metadata.get('model_name', 'XGBoost')}")
    print("[FIREGUARD X] System ready for intelligence requests.")
    yield
    print("[FIREGUARD X] Shutting down application gracefully.")

app = FastAPI(
    title="FIREGUARD X - Forest Fire Risk Intelligence Platform",
    description="Explainable Forest Fire Risk Intelligence, Prediction & Simulation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Sub-Routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
app.include_router(zones_router, prefix="/api")
app.include_router(simulation_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(reports_router, prefix="/api")

# Mount reports/figures static directory for direct visualization access
figures_dir = os.path.join(BASE_DIR, "reports", "figures")
if not os.path.exists(figures_dir):
    alt_figures = os.path.join(CURR_DIR, "reports", "figures")
    if os.path.exists(alt_figures):
        figures_dir = alt_figures
os.makedirs(figures_dir, exist_ok=True)
app.mount("/static/figures", StaticFiles(directory=figures_dir), name="figures")

@app.get("/")
def read_root():
    return {
        "platform": "FIREGUARD X",
        "tagline": "Predict. Explain. Simulate. Monitor.",
        "status": "OPERATIONAL",
        "api_docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
