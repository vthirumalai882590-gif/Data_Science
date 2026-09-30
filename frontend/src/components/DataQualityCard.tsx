import React from "react";
import { CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";
import { DataQualityInfo } from "../types";

export const DataQualityCard: React.FC<{ quality: DataQualityInfo }> = ({ quality }) => {
  const isHealthy = quality.score >= 0.9;

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          Data Quality Engine
        </span>
        <span
          className={`text-xs font-bold px-2 py-0.5 rounded-full ${
            isHealthy
              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
              : "bg-amber-50 text-amber-700 border border-amber-200"
          }`}
        >
          {quality.percentage}% Verified
        </span>
      </div>

      {/* Progress track */}
      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden mb-2">
        <div
          className={`h-full rounded-full transition-all duration-500 ${
            isHealthy ? "bg-emerald-500" : "bg-amber-500"
          }`}
          style={{ width: `${quality.percentage}%` }}
        />
      </div>

      <div className="text-xs text-slate-600 space-y-1">
        <p className="flex items-center gap-1">
          {quality.is_acceptable ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 inline shrink-0" />
          ) : (
            <AlertTriangle className="w-3.5 h-3.5 text-amber-500 inline shrink-0" />
          )}
          {quality.notes}
        </p>

        {quality.missing_fields.length > 0 && (
          <p className="text-red-600 text-[11px]">
            Missing required inputs: {quality.missing_fields.join(", ")}
          </p>
        )}
      </div>
    </div>
  );
};
