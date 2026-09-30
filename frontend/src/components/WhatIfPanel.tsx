import React, { useState } from "react";
import { ArrowRight, Sliders, Sparkles, AlertCircle } from "lucide-react";
import { PredictionInput, WhatIfResult } from "../types";
import { RiskBadge } from "./RiskBadge";

interface WhatIfPanelProps {
  initialValues?: PredictionInput;
  onRunWhatIf: (baseline: PredictionInput, modifications: PredictionInput) => Promise<WhatIfResult>;
}

export const WhatIfPanel: React.FC<WhatIfPanelProps> = ({
  initialValues,
  onRunWhatIf,
}) => {
  const [baseline, setBaseline] = useState<PredictionInput>(
    initialValues || {
      Temperature: 38.0,
      RH: 25.0,
      Ws: 22.0,
      Rain: 0.0,
      Region: 0,
    }
  );

  const [modifications, setModifications] = useState<PredictionInput>({
    Temperature: 30.0,
    RH: 55.0,
    Ws: 12.0,
    Rain: 2.5,
    Region: 0,
  });

  const [result, setResult] = useState<WhatIfResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleCompute = async () => {
    setLoading(true);
    try {
      const res = await onRunWhatIf(baseline, modifications);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
        <div>
          <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-700" />
            <span>What-If Scenario Laboratory</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Test counterfactual microclimate interventions and observe model-associated risk deltas.
          </p>
        </div>

        <button
          onClick={handleCompute}
          disabled={loading}
          className="px-4 py-2 rounded-md bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-xs transition-all flex items-center gap-1.5"
        >
          <Sparkles className="w-3.5 h-3.5" />
          {loading ? "Recalculating..." : "Evaluate Scenario"}
        </button>
      </div>

      {/* Scenario Presets */}
      <div className="mb-4 bg-slate-50 border border-slate-200/80 rounded-lg p-3">
        <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <span>Targeted Intervention Scenarios:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => {
              setBaseline({ Temperature: 36.5, RH: 34.0, Ws: 18.0, Rain: 0.0, Region: 2 });
              setModifications({ Temperature: 28.0, RH: 75.0, Ws: 12.0, Rain: 8.5, Region: 2 });
            }}
            className="text-xs px-2.5 py-1 rounded bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 border border-slate-200 hover:border-emerald-300 font-medium transition-colors"
          >
            🇮🇳 Pre-Monsoon Showers (Bandipur / Western Ghats)
          </button>
          <button
            type="button"
            onClick={() => {
              setBaseline({ Temperature: 34.0, RH: 42.0, Ws: 14.0, Rain: 0.0, Region: 2 });
              setModifications({ Temperature: 42.0, RH: 20.0, Ws: 24.0, Rain: 0.0, Region: 2 });
            }}
            className="text-xs px-2.5 py-1 rounded bg-white hover:bg-rose-50 text-slate-700 hover:text-rose-800 border border-slate-200 hover:border-rose-300 font-medium transition-colors"
          >
            🇮🇳 Severe Heatwave Surge (Simlipal / Central India)
          </button>
          <button
            type="button"
            onClick={() => {
              setBaseline({ Temperature: 37.0, RH: 30.0, Ws: 20.0, Rain: 0.0, Region: 2 });
              setModifications({ Temperature: 24.0, RH: 85.0, Ws: 10.0, Rain: 14.0, Region: 2 });
            }}
            className="text-xs px-2.5 py-1 rounded bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-800 border border-slate-200 hover:border-blue-300 font-medium transition-colors"
          >
            🇮🇳 Monsoon Cloudburst Quenching
          </button>
          <button
            type="button"
            onClick={() => {
              setBaseline({ Temperature: 38.0, RH: 25.0, Ws: 22.0, Rain: 0.0, Region: 0 });
              setModifications({ Temperature: 30.0, RH: 55.0, Ws: 12.0, Rain: 2.5, Region: 0 });
            }}
            className="text-xs px-2.5 py-1 rounded bg-white hover:bg-slate-100 text-slate-600 border border-slate-200 font-medium transition-colors"
          >
            🇩🇿 Mediterranean Coastal Cooling
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Baseline Inputs */}
        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              1. Observed Baseline Conditions
            </span>
            <span className="text-[11px] font-mono text-slate-500">Current</span>
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Temperature:</span>
              <b className="font-mono">{baseline.Temperature}°C</b>
            </div>
            <input
              type="range"
              min="20"
              max="45"
              step="1"
              value={baseline.Temperature}
              onChange={(e) =>
                setBaseline({ ...baseline, Temperature: parseFloat(e.target.value) })
              }
              className="w-full accent-slate-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Relative Humidity:</span>
              <b className="font-mono">{baseline.RH}%</b>
            </div>
            <input
              type="range"
              min="10"
              max="90"
              step="1"
              value={baseline.RH}
              onChange={(e) =>
                setBaseline({ ...baseline, RH: parseFloat(e.target.value) })
              }
              className="w-full accent-slate-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Wind Speed:</span>
              <b className="font-mono">{baseline.Ws} km/h</b>
            </div>
            <input
              type="range"
              min="5"
              max="40"
              step="1"
              value={baseline.Ws}
              onChange={(e) =>
                setBaseline({ ...baseline, Ws: parseFloat(e.target.value) })
              }
              className="w-full accent-slate-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Rainfall:</span>
              <b className="font-mono">{baseline.Rain} mm</b>
            </div>
            <input
              type="range"
              min="0"
              max="15"
              step="0.5"
              value={baseline.Rain}
              onChange={(e) =>
                setBaseline({ ...baseline, Rain: parseFloat(e.target.value) })
              }
              className="w-full accent-slate-700"
            />
          </div>
        </div>

        {/* Counterfactual Modification Inputs */}
        <div className="bg-emerald-50/40 p-4 rounded-lg border border-emerald-200 space-y-3">
          <div className="flex items-center justify-between border-b border-emerald-200 pb-2">
            <span className="text-xs font-bold text-emerald-900 uppercase tracking-wider">
              2. Counterfactual Intervention
            </span>
            <span className="text-[11px] font-mono text-emerald-700">Simulated</span>
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Temperature:</span>
              <b className="font-mono text-emerald-950">{modifications.Temperature}°C</b>
            </div>
            <input
              type="range"
              min="20"
              max="45"
              step="1"
              value={modifications.Temperature}
              onChange={(e) =>
                setModifications({ ...modifications, Temperature: parseFloat(e.target.value) })
              }
              className="w-full accent-emerald-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Relative Humidity:</span>
              <b className="font-mono text-emerald-950">{modifications.RH}%</b>
            </div>
            <input
              type="range"
              min="10"
              max="90"
              step="1"
              value={modifications.RH}
              onChange={(e) =>
                setModifications({ ...modifications, RH: parseFloat(e.target.value) })
              }
              className="w-full accent-emerald-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Wind Speed:</span>
              <b className="font-mono text-emerald-950">{modifications.Ws} km/h</b>
            </div>
            <input
              type="range"
              min="5"
              max="40"
              step="1"
              value={modifications.Ws}
              onChange={(e) =>
                setModifications({ ...modifications, Ws: parseFloat(e.target.value) })
              }
              className="w-full accent-emerald-700"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Rainfall:</span>
              <b className="font-mono text-emerald-950">{modifications.Rain} mm</b>
            </div>
            <input
              type="range"
              min="0"
              max="15"
              step="0.5"
              value={modifications.Rain}
              onChange={(e) =>
                setModifications({ ...modifications, Rain: parseFloat(e.target.value) })
              }
              className="w-full accent-emerald-700"
            />
          </div>
        </div>
      </div>

      {/* Comparative Results */}
      {result && (
        <div className="mt-6 pt-5 border-t border-slate-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-center">
              <div className="text-xs text-slate-500 font-semibold uppercase">Baseline Risk</div>
              <div className="text-2xl font-black text-slate-900 font-mono mt-1">
                {result.baseline_risk}
              </div>
              <div className="mt-1">
                <RiskBadge level={result.baseline_level} size="sm" />
              </div>
            </div>

            <div className="bg-emerald-50/50 border border-emerald-200 rounded-lg p-3 text-center">
              <div className="text-xs text-emerald-800 font-semibold uppercase">Simulated Risk</div>
              <div className="text-2xl font-black text-emerald-950 font-mono mt-1">
                {result.modified_risk}
              </div>
              <div className="mt-1">
                <RiskBadge level={result.modified_level} size="sm" />
              </div>
            </div>

            <div
              className={`rounded-lg p-3 text-center border ${
                result.risk_delta < 0
                  ? "bg-emerald-100/60 border-emerald-300 text-emerald-900"
                  : result.risk_delta > 0
                  ? "bg-red-100/60 border-red-300 text-red-900"
                  : "bg-slate-100 border-slate-300 text-slate-800"
              }`}
            >
              <div className="text-xs font-semibold uppercase">Associated Delta</div>
              <div className="text-2xl font-black font-mono mt-1">
                {result.risk_delta > 0 ? `+${result.risk_delta}` : result.risk_delta} pts
              </div>
              <div className="text-[11px] font-bold mt-1 tracking-wide">
                {result.delta_direction}
              </div>
            </div>
          </div>

          {/* Primary drivers of change list */}
          {result.primary_drivers_of_change.length > 0 && (
            <div className="bg-slate-50 rounded-lg p-3.5 border border-slate-200 mb-3">
              <div className="text-xs font-bold text-slate-700 mb-2">
                Primary Associated Drivers of Risk Delta:
              </div>
              <ul className="text-xs text-slate-600 space-y-1">
                {result.primary_drivers_of_change.map((driver) => (
                  <li key={driver.feature} className="flex items-start gap-1.5">
                    <span className="text-emerald-700 font-bold">•</span>
                    <span>
                      <b>{driver.feature}</b> ({driver.baseline_value} → {driver.modified_value}): {driver.reason}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Causal Disclaimer Section 24 */}
          <div className="text-[11px] text-slate-500 italic bg-slate-50 p-2.5 rounded border border-slate-200/60 flex items-start gap-1.5">
            <AlertCircle className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
            <span>{result.disclaimer}</span>
          </div>
        </div>
      )}
    </div>
  );
};
