# FIREGUARD X — Architecture & System Design

```
+---------------------------------------------------------------------------------+
|                                 USER INTERFACE                                  |
|            React 18 + TypeScript + Vite + Tailwind CSS + Lucide Icons           |
|                                                                                 |
|  [Command Center] [Interactive Map] [Predictor] [Forecast] [What-If] [ModelLab] |
+---------------------------------------------------------------------------------+
                                      |
                               (HTTP REST API)
                                      v
+---------------------------------------------------------------------------------+
|                                FASTAPI BACKEND                                  |
|                                                                                 |
|  [Prediction Router]   [Zones Router]     [Simulation Router] [Reports Router]  |
|  [Dashboard Router]    [Models Router]    [Health Router]                       |
+---------------------------------------------------------------------------------+
          |                                  |                        |
          v                                  v                        v
+-----------------------+          +-------------------+    +-------------------+
|  ML & XAI ENGINE      |          | DATA QUALITY &    |    |  SQLITE DATABASE  |
|  - XGBoost Champion   |          | ANOMALY DETECTOR  |    |  (SQLAlchemy 2.0) |
|  - Multi-Model Bench  |          | - Physical Bounds |    |  - predictions    |
|  - SHAP Explainer     |          | - IsolationForest |    |  - zones          |
|  - Preprocessor Pipe  |          | - Multi Z-Scores  |    |  - simulations    |
|  - Cellular Automaton |          +-------------------+    |  - reports        |
+-----------------------+                                   +-------------------+
```

## Component Architecture
1. **Frontend Client**: SPA structured around responsive tabs and modular components. Uses Leaflet for spatial GIS visualization and Recharts for interactive ROC curves, feature importance, and forecasting trends.
2. **Backend Gateway**: FastAPI with typed Pydantic models, request validation, CORS middleware, error sanitization, and automatic Swagger docs at `/docs`.
3. **Data Science Core**: Model Registry singleton pre-warming models on startup, eliminating per-request loading latency.
4. **Relational Storage**: SQLite with SQLAlchemy ORM abstraction, allowing zero-config local demos while retaining drop-in compatibility for PostgreSQL in production.
