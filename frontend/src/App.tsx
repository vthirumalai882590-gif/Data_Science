import React, { useState, useEffect } from "react";
import { Navbar, TabType } from "./components/Navbar";
import { CommandCenter } from "./pages/CommandCenter";
import { PredictionPage } from "./pages/PredictionPage";
import { RiskMapPage } from "./pages/RiskMapPage";
import { ForecastPage } from "./pages/ForecastPage";
import { WhatIfPage } from "./pages/WhatIfPage";
import { SimulationPage } from "./pages/SimulationPage";
import { ModelLabPage } from "./pages/ModelLabPage";
import { ReportsPage } from "./pages/ReportsPage";
import { AboutPage } from "./pages/AboutPage";
import { api } from "./services/api";

// Import embedded data directly so it is ALWAYS available on Vercel with zero network round-trips
import {
  EMBEDDED_ZONES,
  getEmbeddedDashboardData,
  getEmbeddedModelMetrics,
  runEmbeddedSimulation,
} from "./services/embeddedFireGuard";

import {
  DashboardData,
  Zone,
  PredictionInput,
  PredictionResult,
  WhatIfResult,
  SimulationResult,
  ModelMetricsSummary,
} from "./types";

// Pre-compute embedded defaults at module load time (synchronous, zero latency)
const DEFAULT_DASHBOARD: DashboardData = getEmbeddedDashboardData();
const DEFAULT_ZONES: Zone[] = EMBEDDED_ZONES;
const DEFAULT_METRICS: ModelMetricsSummary = getEmbeddedModelMetrics();
const DEFAULT_SIM: SimulationResult = runEmbeddedSimulation({
  start_zone: "zone-bej-01",
  wind_speed: 20.0,
  wind_direction: "NE",
  dryness: 75.0,
  duration_hours: 24,
  grid_size: 9,
});

export function App() {
  const [currentTab, setCurrentTab] = useState<TabType>("command_center");

  // Initialize ALL state with embedded defaults immediately — no loading spinner required
  const [dashboardData, setDashboardData] = useState<DashboardData>(DEFAULT_DASHBOARD);
  const [zones, setZones] = useState<Zone[]>(DEFAULT_ZONES);
  const [selectedZone, setSelectedZone] = useState<Zone | null>(DEFAULT_ZONES[0] ?? null);
  const [metricsData, setMetricsData] = useState<ModelMetricsSummary>(DEFAULT_METRICS);
  const [simulationData, setSimulationData] = useState<SimulationResult>(DEFAULT_SIM);
  const [simLoading, setSimLoading] = useState<boolean>(false);
  const [systemStatus] = useState<string>("OPERATIONAL");

  // Optionally try to upgrade data from external backend (silently, in background)
  useEffect(() => {
    async function tryUpgradeFromBackend() {
      try {
        const [dashRes, zonesRes, metricsRes] = await Promise.allSettled([
          api.getDashboard(),
          api.getZones(),
          api.getModelMetrics(),
        ]);

        if (dashRes.status === "fulfilled" && dashRes.value) {
          setDashboardData(dashRes.value);
        }
        if (
          zonesRes.status === "fulfilled" &&
          Array.isArray(zonesRes.value) &&
          zonesRes.value.length > 0
        ) {
          setZones(zonesRes.value);
          setSelectedZone(zonesRes.value[0]);
        }
        if (metricsRes.status === "fulfilled" && metricsRes.value) {
          setMetricsData(metricsRes.value);
        }
      } catch {
        // Backend unavailable — already have embedded defaults, nothing to do
      }
    }

    tryUpgradeFromBackend();
  }, []);

  // Handlers
  const handlePredict = async (input: PredictionInput): Promise<PredictionResult> => {
    const res = await api.predictRisk(input);
    // Refresh dashboard stats after a prediction
    api.getDashboard().then(setDashboardData).catch(() => {});
    return res;
  };

  const handleWhatIf = async (
    baseline: PredictionInput,
    modifications: PredictionInput
  ): Promise<WhatIfResult> => {
    return await api.runWhatIf(baseline, modifications);
  };

  const handleSimulation = async (params: {
    start_zone: string;
    wind_speed: number;
    wind_direction: string;
    dryness: number;
    duration_hours: number;
  }) => {
    setSimLoading(true);
    try {
      const res = await api.runSimulation({ ...params, grid_size: 9 });
      setSimulationData(res);
    } catch (err) {
      console.error("Simulation error:", err);
    } finally {
      setSimLoading(false);
    }
  };

  const handleGenerateReport = async (
    result: PredictionResult,
    inputs: PredictionInput
  ) => {
    try {
      const rep = await api.generateReport({
        zone_name: inputs.zone_id || "Custom Observation",
        region: "India / Algeria Forest Reserves",
        inputs: inputs,
        risk_score: result.risk_score,
        risk_level: result.risk_level,
        probability: result.model_probability,
        drivers: result.drivers,
        anomaly_status: result.anomaly.status,
        notes: result.narrative,
      });
      window.open(rep.download_url, "_blank");
    } catch (err) {
      console.error("Report generation failed:", err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8fafc] text-slate-900 font-sans">
      {/* Navigation Header */}
      <Navbar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        systemStatus={systemStatus}
        dataMode={dashboardData?.summary.data_mode || "Embedded AI Engine (Vercel Edge)"}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <>
          {currentTab === "command_center" && (
            <CommandCenter
              dashboardData={dashboardData}
              zones={zones}
              selectedZone={selectedZone}
              onSelectZone={setSelectedZone}
              onNavigateTab={setCurrentTab}
            />
          )}

          {currentTab === "risk_map" && (
            <RiskMapPage
              zones={zones}
              selectedZone={selectedZone}
              onSelectZone={setSelectedZone}
              onNavigateTab={setCurrentTab}
            />
          )}

          {currentTab === "prediction" && (
            <PredictionPage
              selectedZone={selectedZone}
              onPredict={handlePredict}
              onGenerateReport={handleGenerateReport}
            />
          )}

          {currentTab === "forecast" && (
            <ForecastPage
              zones={zones}
              selectedZone={selectedZone}
              onSelectZone={setSelectedZone}
              onFetchForecast={(id) => api.getForecast(id)}
            />
          )}

          {currentTab === "what_if" && (
            <WhatIfPage onRunWhatIf={handleWhatIf} />
          )}

          {currentTab === "simulation" && (
            <SimulationPage
              simulationData={simulationData}
              isLoading={simLoading}
              onRunSimulation={handleSimulation}
            />
          )}

          {currentTab === "model_lab" && (
            <ModelLabPage metricsData={metricsData} />
          )}

          {currentTab === "reports" && (
            <ReportsPage
              onFetchHistory={() => api.getPredictionHistory(50)}
              onFetchReportsList={() => api.getReportsList()}
            />
          )}

          {currentTab === "about" && <AboutPage />}
        </>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-xs text-slate-500 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-800">FIREGUARD X</span>
            <span>• Explainable Forest Fire Risk Intelligence Platform</span>
          </div>
          <div className="text-[11px] text-slate-400">
            UCI Machine Learning Repository • Algerian Forest Fires Dataset • Embedded XGBoost AI Engine
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
