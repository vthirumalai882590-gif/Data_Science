import React from "react";
import { FeatureDriver } from "../types";
import { HelpCircle, ArrowUpRight, ArrowDownRight } from "lucide-react";

interface FeatureContributionChartProps {
  drivers: FeatureDriver[];
  narrative?: string;
}

export const FeatureContributionChart: React.FC<FeatureContributionChartProps> = ({
  drivers,
  narrative,
}) => {
  if (!drivers || drivers.length === 0) {
    return (
      <div className="text-center py-6 text-xs text-slate-400">
        Run prediction to compute SHAP feature contributions.
      </div>
    );
  }

  // Find max contribution for relative bar width
  const maxImpact = Math.max(...drivers.map((d) => d.abs_contribution), 0.05);

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
      <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
        <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
          <span>Explainable AI Attribution (SHAP)</span>
          <span className="text-xs font-normal text-slate-500">
            • Why this prediction?
          </span>
        </h3>
        <span className="text-[11px] font-mono text-slate-400">
          Shapley Values
        </span>
      </div>

      {narrative && (
        <div className="bg-slate-50 border border-slate-200/80 rounded-md p-3 mb-4 text-xs text-slate-700 leading-relaxed font-sans">
          <b className="text-slate-900">Interpretation:</b> {narrative}
        </div>
      )}

      {/* Feature attribution rows */}
      <div className="space-y-3">
        {drivers.map((d) => {
          const widthPct = Math.min(100, Math.max(8, (d.abs_contribution / maxImpact) * 100));
          const isRiskIncrease = d.is_positive;

          return (
            <div key={d.feature} className="text-xs">
              <div className="flex justify-between items-baseline mb-1">
                <span className="font-semibold text-slate-800 flex items-center gap-1">
                  {d.label}
                  <span className="text-slate-400 font-mono font-normal">
                    [{d.display_value}]
                  </span>
                </span>
                <span
                  className={`font-mono font-bold flex items-center gap-0.5 ${
                    isRiskIncrease ? "text-red-600" : "text-emerald-700"
                  }`}
                >
                  {isRiskIncrease ? (
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  ) : (
                    <ArrowDownRight className="w-3.5 h-3.5" />
                  )}
                  {d.contribution > 0 ? `+${d.contribution.toFixed(3)}` : d.contribution.toFixed(3)}
                </span>
              </div>

              {/* Attribution Bar */}
              <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden flex">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isRiskIncrease ? "bg-red-500" : "bg-emerald-600"
                  }`}
                  style={{ width: `${widthPct}%` }}
                />
              </div>

              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>{d.description}</span>
                <span className={isRiskIncrease ? "text-red-700 font-medium" : "text-emerald-700 font-medium"}>
                  {d.direction}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
