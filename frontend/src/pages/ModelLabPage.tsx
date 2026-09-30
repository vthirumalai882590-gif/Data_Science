import React, { useState } from "react";
import { ModelMetricsSummary } from "../types";
import { ModelComparisonTable } from "../components/ModelComparisonTable";
import { BarChart3, Database, ShieldAlert, Image as ImageIcon } from "lucide-react";

export const ModelLabPage: React.FC<{ metricsData: ModelMetricsSummary | null }> = ({
  metricsData,
}) => {
  const [activeTab, setActiveTab] = useState<"benchmark" | "figures" | "dataset">("benchmark");

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-emerald-700" />
            Machine Learning Laboratory & Model Comparison
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Transparent empirical evaluation across candidate architectures trained on stratified holdout test partitions.
          </p>
        </div>

        {/* View Switcher */}
        <div className="flex bg-slate-100 p-0.5 rounded-md border border-slate-200 text-xs">
          <button
            onClick={() => setActiveTab("benchmark")}
            className={`px-3 py-1 rounded font-medium transition-all ${
              activeTab === "benchmark" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600"
            }`}
          >
            Metrics Benchmark
          </button>
          <button
            onClick={() => setActiveTab("figures")}
            className={`px-3 py-1 rounded font-medium transition-all ${
              activeTab === "figures" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600"
            }`}
          >
            Diagnostic Plots
          </button>
          <button
            onClick={() => setActiveTab("dataset")}
            className={`px-3 py-1 rounded font-medium transition-all ${
              activeTab === "dataset" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600"
            }`}
          >
            Dataset & Features
          </button>
        </div>
      </div>

      {activeTab === "benchmark" && (
        <div className="space-y-6">
          <ModelComparisonTable metricsData={metricsData} />

          {/* Hyperparameter Configuration Card */}
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
              Hyperparameter Specification & Training Provenance
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded border border-slate-200">
                <b className="text-slate-900 font-sans">Logistic Regression:</b>
                <div className="font-mono text-slate-600 mt-1 text-[11px]">
                  C=1.0, penalty='l2', solver='lbfgs', max_iter=1000, random_state=42
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded border border-slate-200">
                <b className="text-slate-900 font-sans">Decision Tree:</b>
                <div className="font-mono text-slate-600 mt-1 text-[11px]">
                  criterion='gini', max_depth=5, min_samples_leaf=4, random_state=42
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded border border-slate-200">
                <b className="text-slate-900 font-sans">Random Forest:</b>
                <div className="font-mono text-slate-600 mt-1 text-[11px]">
                  n_estimators=150, max_depth=7, min_samples_leaf=2, random_state=42
                </div>
              </div>
              <div className="p-3 bg-emerald-50 rounded border border-emerald-200">
                <b className="text-emerald-950 font-sans">XGBoost (Champion):</b>
                <div className="font-mono text-emerald-800 mt-1 text-[11px]">
                  n_estimators=100, learning_rate=0.08, max_depth=4, eval_metric='logloss'
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === "figures" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* ROC Curve */}
            <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
              <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                <span className="text-xs font-bold text-slate-800">ROC Curves Comparison</span>
                <span className="text-[11px] font-mono text-slate-400">reports/figures/roc_curves.png</span>
              </div>
              <div className="flex items-center justify-center p-2 bg-slate-50 rounded border border-slate-200">
                <img
                  src="/static/figures/roc_curves.png"
                  alt="ROC Curves Comparison"
                  className="max-h-[340px] object-contain rounded"
                  onError={(e: any) => {
                    e.target.style.display = "none";
                  }}
                />
              </div>
            </div>

            {/* Feature Importance */}
            <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
              <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                <span className="text-xs font-bold text-slate-800">Gini Feature Importance</span>
                <span className="text-[11px] font-mono text-slate-400">reports/figures/feature_importance.png</span>
              </div>
              <div className="flex items-center justify-center p-2 bg-slate-50 rounded border border-slate-200">
                <img
                  src="/static/figures/feature_importance.png"
                  alt="Feature Importance"
                  className="max-h-[340px] object-contain rounded"
                  onError={(e: any) => {
                    e.target.style.display = "none";
                  }}
                />
              </div>
            </div>

            {/* Confusion Matrices */}
            <div className="col-span-1 lg:col-span-2 bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
              <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
                <span className="text-xs font-bold text-slate-800">Comparative Confusion Matrices</span>
                <span className="text-[11px] font-mono text-slate-400">reports/figures/confusion_matrices.png</span>
              </div>
              <div className="flex items-center justify-center p-2 bg-slate-50 rounded border border-slate-200">
                <img
                  src="/static/figures/confusion_matrices.png"
                  alt="Confusion Matrices"
                  className="max-h-[380px] object-contain rounded"
                  onError={(e: any) => {
                    e.target.style.display = "none";
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === "dataset" && (
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-2">
            <Database className="w-4 h-4 text-emerald-700" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Dataset Profile & Engineered Schema
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-500 font-sans">Primary Source:</span>
              <div className="font-bold text-slate-900 mt-0.5">UCI Algerian Forest Fires</div>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-500 font-sans">Total Validated Observations:</span>
              <div className="font-bold text-slate-900 mt-0.5">243 Records across 2 Regions</div>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-500 font-sans">Engineered Feature Dimension:</span>
              <div className="font-bold text-slate-900 mt-0.5">16 Total Input Dimensions</div>
            </div>
          </div>

          <div className="space-y-2 pt-2">
            <h4 className="text-xs font-bold text-slate-700">Documented Feature Set:</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {[
                { name: "Temperature", desc: "Ambient temperature in °C" },
                { name: "RH", desc: "Relative humidity percentage" },
                { name: "Ws", desc: "Surface wind speed in km/h" },
                { name: "Rain", desc: "Daily accumulated rainfall in mm" },
                { name: "FFMC", desc: "Fine Fuel Moisture Code (litter dryness)" },
                { name: "DMC", desc: "Duff Moisture Code (organic layer moisture)" },
                { name: "DC", desc: "Drought Code (deep compact organic soil)" },
                { name: "ISI", desc: "Initial Spread Index (rate of fire spread)" },
                { name: "BUI", desc: "Buildup Index (available combustion fuel)" },
                { name: "FWI", desc: "Fire Weather Index (overall fire intensity)" },
                { name: "temp_rh_ratio", desc: "Derived: Temperature / Relative Humidity" },
                { name: "dryness_index", desc: "Derived: Atmospheric evapotranspiration drying rate" },
                { name: "wind_temp_interaction", desc: "Derived: Convective heat transfer interaction" },
                { name: "rain_deficit", desc: "Derived: Inverse rainfall indicator" },
                { name: "ffmc_isi_ratio", desc: "Derived: Spread potential normalized by moisture" },
              ].map((f) => (
                <div key={f.name} className="p-2 bg-slate-50 border border-slate-200 rounded flex justify-between">
                  <span className="font-mono font-bold text-slate-900">{f.name}</span>
                  <span className="text-slate-500 text-[11px]">{f.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
