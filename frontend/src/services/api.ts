// FIREGUARD X - Centralized API Service Layer with Automatic Embedded AI Engine
// Seamlessly delegates to embedded in-browser machine learning and analytics engine
// when deployed on Vercel or when the backend service is offline.

import {
  DashboardData,
  Zone,
  ZoneForecast,
  PredictionInput,
  PredictionResult,
  WhatIfResult,
  SimulationResult,
  ModelMetricsSummary,
  PredictionHistoryItem,
} from "../types";

import {
  EMBEDDED_ZONES,
  getEmbeddedDashboardData,
  runEmbeddedPrediction,
  getEmbeddedForecast,
  runEmbeddedWhatIf,
  runEmbeddedSimulation,
  getEmbeddedModelMetrics,
  generateEmbeddedReport,
  getEmbeddedReportsList,
  getPredictionHistoryFromStorage,
} from "./embeddedFireGuard";

const API_BASE = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!res.ok) {
    let errorMsg = `Server error (${res.status})`;
    try {
      const errJson = await res.json();
      if (errJson.detail) errorMsg = errJson.detail;
    } catch {
      // use fallback
    }
    throw new Error(errorMsg);
  }

  // Guard against SPA returning index.html for unknown /api routes
  const contentType = res.headers.get("content-type");
  if (contentType && contentType.includes("text/html")) {
    throw new Error("HTML response received instead of JSON (backend endpoint unavailable on Vercel).");
  }

  return await res.json();
}

export const api = {
  // 1. Health check
  async getHealth(): Promise<{ status: string; model_loaded: boolean; selected_model: string; mode: string }> {
    try {
      const res = await request<{ status: string; model_loaded: boolean; selected_model: string }>("/health");
      return { ...res, mode: "Connected to External Backend" };
    } catch {
      return {
        status: "OPERATIONAL",
        model_loaded: true,
        selected_model: "XGBoost (In-Browser Embedded AI)",
        mode: "Vercel Standalone Edge",
      };
    }
  },

  // 2. Command Center Dashboard
  async getDashboard(): Promise<DashboardData> {
    try {
      return await request<DashboardData>("/dashboard");
    } catch (err) {
      console.info("Using embedded dashboard data engine for Vercel deployment.");
      return getEmbeddedDashboardData();
    }
  },

  // 3. Zones & Digital Twin
  async getZones(): Promise<Zone[]> {
    try {
      const zones = await request<Zone[]>("/zones");
      if (Array.isArray(zones) && zones.length > 0) return zones;
      return EMBEDDED_ZONES;
    } catch {
      return EMBEDDED_ZONES;
    }
  },

  async getZone(zoneId: string): Promise<Zone> {
    try {
      return await request<Zone>(`/zones/${zoneId}`);
    } catch {
      const found = EMBEDDED_ZONES.find((z) => z.id === zoneId);
      if (found) return found;
      return EMBEDDED_ZONES[0];
    }
  },

  async getForecast(zoneId: string): Promise<ZoneForecast> {
    try {
      return await request<ZoneForecast>(`/forecast/${zoneId}`);
    } catch {
      return getEmbeddedForecast(zoneId);
    }
  },

  // 4. ML Prediction & XAI
  async predictRisk(payload: PredictionInput): Promise<PredictionResult> {
    try {
      return await request<PredictionResult>("/predict", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch (err) {
      console.info("Executing prediction via embedded XGBoost engine.");
      return runEmbeddedPrediction(payload);
    }
  },

  async getPredictionHistory(limit: number = 25): Promise<PredictionHistoryItem[]> {
    try {
      const res = await request<PredictionHistoryItem[]>(`/predictions/history?limit=${limit}`);
      if (Array.isArray(res) && res.length > 0) return res;
      return getPredictionHistoryFromStorage(limit);
    } catch {
      return getPredictionHistoryFromStorage(limit);
    }
  },

  // 5. Counterfactual What-If
  async runWhatIf(baseline: PredictionInput, modifications: PredictionInput): Promise<WhatIfResult> {
    try {
      return await request<WhatIfResult>("/what-if", {
        method: "POST",
        body: JSON.stringify({ baseline, modifications }),
      });
    } catch {
      return runEmbeddedWhatIf(baseline, modifications);
    }
  },

  // 6. Educational Fire Spread Simulator
  async runSimulation(payload: {
    start_zone: string;
    wind_speed: number;
    wind_direction: string;
    dryness: number;
    duration_hours: number;
    grid_size?: number;
  }): Promise<SimulationResult> {
    try {
      return await request<SimulationResult>("/simulation", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch {
      return runEmbeddedSimulation(payload);
    }
  },

  // 7. Model Laboratory & Metrics
  async getModelMetrics(): Promise<ModelMetricsSummary> {
    try {
      return await request<ModelMetricsSummary>("/model/metrics");
    } catch {
      return getEmbeddedModelMetrics();
    }
  },

  async getModelFeatures(): Promise<{ total_features: number; features: any[] }> {
    try {
      return await request("/model/features");
    } catch {
      return {
        total_features: 16,
        features: [
          { name: "Temperature", description: "Ambient temperature in °C" },
          { name: "RH", description: "Relative humidity percentage" },
          { name: "Ws", description: "Wind speed in km/h" },
          { name: "Rain", description: "Precipitation in mm" },
          { name: "FFMC", description: "Fine Fuel Moisture Code" },
          { name: "DMC", description: "Duff Moisture Code" },
          { name: "DC", description: "Drought Code" },
          { name: "ISI", description: "Initial Spread Index" },
          { name: "BUI", description: "Buildup Index" },
          { name: "FWI", description: "Fire Weather Index" },
          { name: "Region", description: "Geographic region indicator" },
          { name: "temp_rh_ratio", description: "Temperature to Humidity Ratio" },
          { name: "dryness_index", description: "Atmospheric Dryness Index" },
          { name: "wind_temp_interaction", description: "Wind-Temperature Convective Interaction" },
          { name: "rain_deficit", description: "Inverse Rain Deficit Index" },
          { name: "ffmc_isi_ratio", description: "Initial Spread to Fine Fuel Ratio" },
        ],
      };
    }
  },

  // 8. Reports Generation
  async generateReport(payload: {
    zone_name: string;
    region: string;
    inputs: Record<string, any>;
    risk_score: number;
    risk_level: string;
    probability: number;
    drivers: any[];
    anomaly_status: string;
    notes?: string;
  }): Promise<{ id: number; report_html: string; download_url: string; disclaimer: string }> {
    try {
      return await request("/reports/generate", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch {
      return generateEmbeddedReport(payload);
    }
  },

  async getReportsList(): Promise<any[]> {
    try {
      const reps = await request<any[]>("/reports");
      if (Array.isArray(reps) && reps.length > 0) return reps;
      return getEmbeddedReportsList();
    } catch {
      return getEmbeddedReportsList();
    }
  },
};
