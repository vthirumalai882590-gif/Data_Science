import React from "react";
import { ZoneForecast } from "../types";
import { Clock, AlertTriangle, TrendingUp } from "lucide-react";
import { RiskBadge } from "./RiskBadge";

export const ForecastChart: React.FC<{ forecast: ZoneForecast | null }> = ({
  forecast,
}) => {
  if (!forecast) {
    return (
      <div className="p-6 text-center text-xs text-slate-400 bg-white rounded-lg border border-slate-200">
        Select a zone to generate meteorological risk trajectory forecast.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Clock className="w-4 h-4 text-slate-500" />
            <span>Diurnal Risk Trajectory Forecast</span>
            <span className="text-xs font-normal text-slate-500 font-mono">
              • {forecast.zone_name}
            </span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Diurnal atmospheric thermodynamics & empirical meteorological inertia projection.
          </p>
        </div>

        {forecast.is_escalating && (
          <span className="text-xs bg-red-50 text-red-800 border border-red-200 px-2.5 py-1 rounded-md font-bold flex items-center gap-1.5 animate-pulse">
            <AlertTriangle className="w-3.5 h-3.5 text-red-600" />
            Risk Escalation Alert (+{forecast.score_delta} pts)
          </span>
        )}
      </div>

      {/* Forecast Horizon Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 mb-4">
        {forecast.forecast.map((pt) => (
          <div
            key={pt.label}
            className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-center flex flex-col justify-between"
          >
            <div>
              <div className="text-[11px] font-bold text-slate-700">{pt.label}</div>
              <div className="text-[10px] text-slate-400 mb-2">{pt.period}</div>
              <div className="text-xl font-black font-mono text-slate-900">
                {pt.risk_score}
                <span className="text-[10px] font-normal text-slate-400">/100</span>
              </div>
            </div>

            <div className="mt-2 pt-2 border-t border-slate-200/60 text-[11px] text-slate-600">
              <div>🌡️ {pt.temperature}°C</div>
              <div>💧 {pt.rh}% RH</div>
              <div className="mt-1.5">
                <RiskBadge level={pt.risk_level} size="sm" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-xs text-slate-500 bg-slate-50 p-2.5 rounded border border-slate-200/60 flex items-center justify-between">
        <span><b>Trajectory Note:</b> {forecast.escalation_warning}</span>
        <span className="text-[10px] font-mono text-slate-400">
          Diurnal Cycle Simulation
        </span>
      </div>
    </div>
  );
};
