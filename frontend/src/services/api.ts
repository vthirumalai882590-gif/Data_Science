// FIREGUARD X - Centralized API Service Layer

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

const API_BASE = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
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

    return await res.json();
  } catch (err: any) {
    console.error(`API Call failed: ${endpoint}`, err);
    throw err;
  }
}

export const api = {
  // 1. Health check
  async getHealth(): Promise<{ status: string; model_loaded: boolean; selected_model: string }> {
    return request("/health");
  },

  // 2. Command Center Dashboard
  async getDashboard(): Promise<DashboardData> {
    return request("/dashboard");
  },

  // 3. Zones & Digital Twin
  async getZones(): Promise<Zone[]> {
    return request("/zones");
  },

  async getZone(zoneId: string): Promise<Zone> {
    return request(`/zones/${zoneId}`);
  },

  async getForecast(zoneId: string): Promise<ZoneForecast> {
    return request(`/forecast/${zoneId}`);
  },

  // 4. ML Prediction & XAI
  async predictRisk(payload: PredictionInput): Promise<PredictionResult> {
    return request("/predict", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async getPredictionHistory(limit: number = 25): Promise<PredictionHistoryItem[]> {
    return request(`/predictions/history?limit=${limit}`);
  },

  // 5. Counterfactual What-If
  async runWhatIf(baseline: PredictionInput, modifications: PredictionInput): Promise<WhatIfResult> {
    return request("/what-if", {
      method: "POST",
      body: JSON.stringify({ baseline, modifications }),
    });
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
    return request("/simulation", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  // 7. Model Laboratory & Metrics
  async getModelMetrics(): Promise<ModelMetricsSummary> {
    return request("/model/metrics");
  },

  async getModelFeatures(): Promise<{ total_features: number; features: any[] }> {
    return request("/model/features");
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
    return request("/reports/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async getReportsList(): Promise<any[]> {
    return request("/reports");
  },
};
