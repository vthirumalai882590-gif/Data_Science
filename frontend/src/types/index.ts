// FIREGUARD X - Core TypeScript Definitions

export interface Zone {
  id: string;
  zone_name: string;
  latitude: float;
  longitude: float;
  region_id: number;
  risk_score: number;
  risk_level: "LOW" | "MODERATE" | "ELEVATED" | "HIGH" | "CRITICAL";
  temperature: number;
  humidity: number;
  wind: number;
  rainfall: number;
  ffmc: number;
  dmc: number;
  dc: number;
  isi: number;
  bui: number;
  fwi: number;
  historical_fire_count: number;
  country?: string;
}

export type float = number;

export interface DashboardSummary {
  current_risk: number;
  active_zones: number;
  high_risk_zones_count: number;
  critical_risk_zones_count: number;
  anomalies_count: number;
  model_f1: number;
  model_name: string;
  data_mode: string;
}

export interface DashboardData {
  summary: DashboardSummary;
  top_risk_zones: {
    id: string;
    zone_name: string;
    risk_score: number;
    risk_level: string;
    temperature: number;
    humidity: number;
    wind: number;
    rainfall: number;
    historical_fire_count: number;
  }[];
  anomalous_zones: {
    zone_id: string;
    zone_name: string;
    status: string;
    badge: string;
    score: number;
    narrative: string;
  }[];
  risk_distribution: {
    LOW: number;
    MODERATE: number;
    ELEVATED: number;
    HIGH: number;
    CRITICAL: number;
  };
  system_status: string;
}

export interface PredictionInput {
  Temperature: number;
  RH: number;
  Ws: number;
  Rain: number;
  FFMC?: number;
  DMC?: number;
  DC?: number;
  ISI?: number;
  BUI?: number;
  FWI?: number;
  Region?: number;
  zone_id?: string;
}

export interface FeatureDriver {
  feature: string;
  label: string;
  raw_value: any;
  display_value: string;
  contribution: number;
  abs_contribution: number;
  direction: string;
  is_positive: boolean;
  description: string;
}

export interface AnomalyInfo {
  status: string;
  badge: string;
  anomaly_score: number;
  is_anomaly: boolean;
  deviations: {
    feature: string;
    current_value: number;
    historical_normal: number;
    z_score: number;
    direction: string;
    severity: string;
  }[];
  narrative: string;
}

export interface DataQualityInfo {
  score: number;
  percentage: number;
  missing_fields: string[];
  invalid_fields: { field: string; value: any; expected: string }[];
  is_acceptable: boolean;
  notes: string;
}

export interface PredictionResult {
  risk_score: number;
  risk_level: string;
  risk_badge: string;
  risk_color: string;
  model_probability: number;
  probability_percent: number;
  environmental_vulnerability: number;
  data_quality: DataQualityInfo;
  anomaly: AnomalyInfo;
  drivers: FeatureDriver[];
  narrative: string;
  model_name: string;
  timestamp: string;
}

export interface ForecastPoint {
  hours: number;
  label: string;
  period: string;
  temperature: number;
  rh: number;
  ws: number;
  rain: number;
  risk_score: number;
  risk_level: string;
  risk_color: string;
  risk_badge: string;
  probability: number;
}

export interface ZoneForecast {
  zone_id: string;
  zone_name: string;
  baseline: {
    hours: number;
    label: string;
    temperature: number;
    rh: number;
    ws: number;
    rain: number;
    risk_score: number;
    risk_level: string;
    risk_color: string;
  };
  forecast: ForecastPoint[];
  is_escalating: boolean;
  score_delta: number;
  escalation_warning: string;
  methodology: string;
}

export interface WhatIfImpact {
  feature: string;
  baseline_value: number;
  modified_value: number;
  direction: string;
  reason: string;
}

export interface WhatIfResult {
  baseline_risk: number;
  baseline_level: string;
  modified_risk: number;
  modified_level: string;
  risk_delta: number;
  delta_direction: string;
  baseline_probability: number;
  modified_probability: number;
  primary_drivers_of_change: WhatIfImpact[];
  disclaimer: string;
}

export interface CellState {
  row: number;
  col: number;
  state: "SAFE" | "AT_RISK" | "SIMULATED_FIRE" | "AFFECTED";
  intensity: number;
}

export interface SimulationStep {
  time_label: string;
  hours: number;
  cells: CellState[];
  active_fire_count: number;
  affected_count: number;
  at_risk_count: number;
}

export interface SimulationResult {
  start_zone: string;
  wind_speed: number;
  wind_direction: string;
  dryness: number;
  duration_hours: number;
  grid_dimension: number;
  steps: SimulationStep[];
  disclaimer: string;
}

export interface ModelMetricsSummary {
  models: Record<
    string,
    {
      model_name: string;
      accuracy: number;
      precision: number;
      recall: number;
      f1: number;
      roc_auc: number;
      pr_auc: number;
      confusion_matrix: number[][];
      true_negatives: number;
      false_positives: number;
      false_negatives: number;
      true_positives: number;
      false_negative_rate: number;
      false_positive_rate: number;
      safety_notes: string;
    }
  >;
  selected_model: string;
  best_metrics: any;
  features: string[];
  test_size: number;
  train_size: number;
  timestamp: string;
}

export interface PredictionHistoryItem {
  id: number;
  timestamp: string;
  zone_id: string;
  risk_score: number;
  risk_level: string;
  probability: number;
  data_quality: number;
  input_data: Record<string, any>;
}
