import React, { useState } from "react";
import { Zone, PredictionInput, PredictionResult } from "../types";
import { RiskGauge } from "../components/RiskGauge";
import { RiskBadge } from "../components/RiskBadge";
import { FeatureContributionChart } from "../components/FeatureContributionChart";
import { DataQualityCard } from "../components/DataQualityCard";
import { AnomalyCard } from "../components/AnomalyCard";
import { LoadingState } from "../components/States";
import { Flame, Sparkles, RefreshCw, FileText, CheckCircle2 } from "lucide-react";

interface PredictionPageProps {
  selectedZone: Zone | null;
  onPredict: (input: PredictionInput) => Promise<PredictionResult>;
  onGenerateReport: (result: PredictionResult, inputs: PredictionInput) => void;
}

export const PredictionPage: React.FC<PredictionPageProps> = ({
  selectedZone,
  onPredict,
  onGenerateReport,
}) => {
  const [formData, setFormData] = useState<PredictionInput>({
    Temperature: selectedZone?.temperature ?? 36.0,
    RH: selectedZone?.humidity ?? 30.0,
    Ws: selectedZone?.wind ?? 18.0,
    Rain: selectedZone?.rainfall ?? 0.0,
    FFMC: selectedZone?.ffmc ?? 88.0,
    DMC: selectedZone?.dmc ?? 22.0,
    DC: selectedZone?.dc ?? 65.0,
    ISI: selectedZone?.isi ?? 8.5,
    BUI: selectedZone?.bui ?? 24.0,
    FWI: selectedZone?.fwi ?? 14.0,
    Region: selectedZone?.region_id ?? 0,
    zone_id: selectedZone?.id ?? "Custom Area",
  });

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [showAdvanced, setShowAdvanced] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await onPredict(formData);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyPreset = (preset: "bandipur" | "simlipal" | "corbett" | "safe") => {
    if (preset === "simlipal") {
      setFormData({
        Temperature: 41.5,
        RH: 21.0,
        Ws: 24.0,
        Rain: 0.0,
        FFMC: 95.0,
        DMC: 44.0,
        DC: 175.0,
        ISI: 17.5,
        BUI: 49.0,
        FWI: 33.0,
        Region: 2,
        zone_id: "Simlipal Biosphere Reserve (Odisha, India)",
      });
    } else if (preset === "bandipur") {
      setFormData({
        Temperature: 36.5,
        RH: 34.0,
        Ws: 18.0,
        Rain: 0.0,
        FFMC: 91.2,
        DMC: 32.5,
        DC: 115.0,
        ISI: 12.4,
        BUI: 35.0,
        FWI: 24.2,
        Region: 2,
        zone_id: "Bandipur Tiger Reserve (Karnataka, India)",
      });
    } else if (preset === "corbett") {
      setFormData({
        Temperature: 37.0,
        RH: 31.0,
        Ws: 19.0,
        Rain: 0.0,
        FFMC: 90.8,
        DMC: 31.0,
        DC: 118.0,
        ISI: 11.5,
        BUI: 34.0,
        FWI: 22.8,
        Region: 2,
        zone_id: "Jim Corbett Reserve (Uttarakhand, India)",
      });
    } else {
      setFormData({
        Temperature: 25.0,
        RH: 78.0,
        Ws: 11.0,
        Rain: 4.5,
        FFMC: 55.0,
        DMC: 4.0,
        DC: 12.0,
        ISI: 1.0,
        BUI: 3.5,
        FWI: 0.5,
        Region: 2,
        zone_id: "Wayanad Sanctuary (Kerala, India) - Post Rain",
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Flame className="w-5 h-5 text-red-600" />
            Forest Fire Risk Prediction & Explainability Engine
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Calibrated multi-variate environmental inference powered by champion XGBoost architecture with SHAP attributions.
          </p>
        </div>

        {/* Presets */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs">
          <span className="font-semibold text-slate-500">India Hotspot Presets:</span>
          <button
            type="button"
            onClick={() => handleApplyPreset("bandipur")}
            className="px-2.5 py-1 rounded bg-amber-50 text-amber-900 border border-amber-300 hover:bg-amber-100 font-medium text-[11px]"
          >
            🐅 Bandipur (Karnataka)
          </button>
          <button
            type="button"
            onClick={() => handleApplyPreset("simlipal")}
            className="px-2.5 py-1 rounded bg-red-50 text-red-900 border border-red-300 hover:bg-red-100 font-medium text-[11px]"
          >
            🔥 Simlipal Heatwave (Odisha)
          </button>
          <button
            type="button"
            onClick={() => handleApplyPreset("corbett")}
            className="px-2.5 py-1 rounded bg-orange-50 text-orange-900 border border-orange-300 hover:bg-orange-100 font-medium text-[11px]"
          >
            🌲 Jim Corbett (Uttarakhand)
          </button>
          <button
            type="button"
            onClick={() => handleApplyPreset("safe")}
            className="px-2.5 py-1 rounded bg-emerald-50 text-emerald-900 border border-emerald-300 hover:bg-emerald-100 font-medium text-[11px]"
          >
            🟢 Wayanad Post-Rain
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form: Inputs */}
        <div className="lg:col-span-5 bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex justify-between items-center border-b border-slate-100 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                1. Meteorological Inputs
              </span>
              <span className="text-[11px] font-mono text-slate-400">
                {formData.zone_id}
              </span>
            </div>

            {/* Temperature */}
            <div>
              <label className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Ambient Air Temperature (°C):</span>
                <span className="font-mono text-slate-900">{formData.Temperature}°C</span>
              </label>
              <input
                type="number"
                step="0.5"
                min="10"
                max="55"
                value={formData.Temperature}
                onChange={(e) =>
                  setFormData({ ...formData, Temperature: parseFloat(e.target.value) || 0 })
                }
                className="w-full text-xs font-mono p-2 border border-slate-300 rounded focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
                required
              />
            </div>

            {/* Relative Humidity */}
            <div>
              <label className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Relative Humidity (%):</span>
                <span className="font-mono text-slate-900">{formData.RH}%</span>
              </label>
              <input
                type="number"
                step="1"
                min="1"
                max="100"
                value={formData.RH}
                onChange={(e) =>
                  setFormData({ ...formData, RH: parseFloat(e.target.value) || 0 })
                }
                className="w-full text-xs font-mono p-2 border border-slate-300 rounded focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
                required
              />
            </div>

            {/* Wind Velocity */}
            <div>
              <label className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Wind Speed (km/h):</span>
                <span className="font-mono text-slate-900">{formData.Ws} km/h</span>
              </label>
              <input
                type="number"
                step="0.5"
                min="0"
                max="90"
                value={formData.Ws}
                onChange={(e) =>
                  setFormData({ ...formData, Ws: parseFloat(e.target.value) || 0 })
                }
                className="w-full text-xs font-mono p-2 border border-slate-300 rounded focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
                required
              />
            </div>

            {/* Rainfall */}
            <div>
              <label className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Precipitation Rainfall (mm):</span>
                <span className="font-mono text-slate-900">{formData.Rain} mm</span>
              </label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="150"
                value={formData.Rain}
                onChange={(e) =>
                  setFormData({ ...formData, Rain: parseFloat(e.target.value) || 0 })
                }
                className="w-full text-xs font-mono p-2 border border-slate-300 rounded focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
                required
              />
            </div>

            {/* Advanced FWI Toggles */}
            <div className="pt-2">
              <button
                type="button"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="text-xs text-emerald-700 hover:text-emerald-800 font-semibold underline underline-offset-2"
              >
                {showAdvanced ? "Hide FWI System Indices ▲" : "Show Advanced FWI System Indices ▼"}
              </button>

              {showAdvanced && (
                <div className="grid grid-cols-2 gap-2 mt-3 p-3 bg-slate-50 border border-slate-200 rounded-md text-xs">
                  <div>
                    <label className="text-slate-500 font-medium">FFMC (Fuel Moisture):</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.FFMC ?? 85.0}
                      onChange={(e) =>
                        setFormData({ ...formData, FFMC: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full p-1 border border-slate-300 rounded font-mono text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-slate-500 font-medium">DMC (Duff Moisture):</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.DMC ?? 16.0}
                      onChange={(e) =>
                        setFormData({ ...formData, DMC: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full p-1 border border-slate-300 rounded font-mono text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-slate-500 font-medium">DC (Drought Code):</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.DC ?? 45.0}
                      onChange={(e) =>
                        setFormData({ ...formData, DC: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full p-1 border border-slate-300 rounded font-mono text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-slate-500 font-medium">ISI (Spread Index):</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.ISI ?? 6.5}
                      onChange={(e) =>
                        setFormData({ ...formData, ISI: parseFloat(e.target.value) || 0 })
                      }
                      className="w-full p-1 border border-slate-300 rounded font-mono text-xs"
                    />
                  </div>
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs uppercase tracking-wider transition-all shadow-xs flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Calculating Prediction...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Run Risk Prediction
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Output: Results & Explainability */}
        <div className="lg:col-span-7 space-y-4">
          {loading ? (
            <LoadingState message="Executing inference pipeline & SHAP explainer..." />
          ) : result ? (
            <>
              {/* Primary Prediction Output Card */}
              <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
                  <div>
                    <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">
                      Inference Outcome
                    </span>
                    <div className="text-lg font-black text-slate-900 tracking-tight flex items-center gap-2 mt-0.5">
                      <RiskBadge level={result.risk_level} size="lg" />
                    </div>
                  </div>

                  <button
                    onClick={() => onGenerateReport(result, formData)}
                    className="px-3 py-1.5 rounded bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs"
                  >
                    <FileText className="w-3.5 h-3.5" /> Generate Audit Report
                  </button>
                </div>

                <div className="mb-4">
                  <RiskGauge score={result.risk_score} level={result.risk_level} />
                </div>

                {/* Metric Summary Tiers */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                  <div>
                    <div className="text-slate-500 text-[11px] font-semibold uppercase">
                      Risk Score
                    </div>
                    <div className="text-2xl font-black text-slate-900 font-mono">
                      {result.risk_score}
                      <span className="text-xs text-slate-400 font-normal">/100</span>
                    </div>
                  </div>

                  <div>
                    <div className="text-slate-500 text-[11px] font-semibold uppercase">
                      Model Probability
                    </div>
                    <div className="text-2xl font-black text-slate-900 font-mono">
                      {result.probability_percent}%
                    </div>
                  </div>

                  <div>
                    <div className="text-slate-500 text-[11px] font-semibold uppercase">
                      Data Quality
                    </div>
                    <div className="text-2xl font-black text-emerald-700 font-mono">
                      {result.data_quality.percentage}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Explainable AI Component (SHAP) */}
              <FeatureContributionChart
                drivers={result.drivers}
                narrative={result.narrative}
              />

              {/* Anomaly & Data Quality Badges */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <AnomalyCard anomaly={result.anomaly} />
                <DataQualityCard quality={result.data_quality} />
              </div>
            </>
          ) : (
            <div className="p-12 text-center bg-white rounded-lg border border-dashed border-slate-300 text-slate-400 text-xs">
              Configure environmental variables on the left and click <b>Run Risk Prediction</b> to calculate scores and local SHAP explanations.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
