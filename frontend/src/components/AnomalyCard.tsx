import React from "react";
import { AlertTriangle, Activity, CheckCircle2 } from "lucide-react";
import { AnomalyInfo } from "../types";

export const AnomalyCard: React.FC<{ anomaly: AnomalyInfo }> = ({ anomaly }) => {
  const isNormal = anomaly.status === "NORMAL";

  return (
    <div
      className={`rounded-lg border p-4 shadow-xs transition-all ${
        isNormal
          ? "bg-white border-slate-200"
          : anomaly.status === "HIGHLY UNUSUAL"
          ? "bg-red-50/40 border-red-300"
          : "bg-amber-50/40 border-amber-300"
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
          <Activity className="w-4 h-4 text-slate-500" />
          Environmental Anomaly Monitor
        </span>
        <span
          className={`text-xs font-bold px-2 py-0.5 rounded-full border ${
            isNormal
              ? "bg-emerald-50 text-emerald-800 border-emerald-200"
              : anomaly.status === "HIGHLY UNUSUAL"
              ? "bg-red-100 text-red-800 border-red-300 font-extrabold"
              : "bg-amber-100 text-amber-800 border-amber-300"
          }`}
        >
          {anomaly.badge}
        </span>
      </div>

      <p className="text-xs text-slate-700 leading-relaxed mb-3">
        {anomaly.narrative}
      </p>

      {/* Deviating Features Breakdown */}
      {anomaly.deviations.length > 0 ? (
        <div className="space-y-1.5 pt-2 border-t border-slate-200/60">
          <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
            Atmospheric Deviations vs Historical Baseline:
          </div>
          {anomaly.deviations.map((dev) => (
            <div
              key={dev.feature}
              className="text-xs bg-white/80 border border-slate-200 rounded px-2.5 py-1.5 flex justify-between items-center"
            >
              <span className="font-medium text-slate-800">
                {dev.feature}: <b className="font-mono">{dev.current_value}</b>
              </span>
              <span className="text-slate-500 text-[11px]">
                Normal: <span className="font-mono">{dev.historical_normal}</span>{" "}
                <span
                  className={
                    dev.direction === "higher"
                      ? "text-red-600 font-bold"
                      : "text-blue-600 font-bold"
                  }
                >
                  ({dev.direction} by {Math.abs(dev.z_score)}σ)
                </span>
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-[11px] text-emerald-700 flex items-center gap-1 pt-1">
          <CheckCircle2 className="w-3.5 h-3.5" />
          All observed meteorological variables conform within empirical variance bands.
        </div>
      )}
    </div>
  );
};
