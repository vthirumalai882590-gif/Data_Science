import React from "react";

interface RiskGaugeProps {
  score: number;
  level: string;
  size?: "sm" | "md" | "lg";
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({ score, level }) => {
  const clamped = Math.max(0, Math.min(100, score));

  // Determine bar color
  let barColor = "bg-emerald-500";
  if (clamped > 20 && clamped <= 40) barColor = "bg-yellow-500";
  else if (clamped > 40 && clamped <= 60) barColor = "bg-orange-500";
  else if (clamped > 60 && clamped <= 80) barColor = "bg-red-600";
  else if (clamped > 80) barColor = "bg-red-900";

  return (
    <div className="w-full">
      <div className="flex justify-between items-baseline mb-1.5">
        <span className="text-xs font-semibold text-slate-600 uppercase tracking-wider">
          Calculated Risk Index
        </span>
        <span className="text-2xl font-black text-slate-900 tracking-tight">
          {clamped}
          <span className="text-sm font-medium text-slate-500">/100</span>
        </span>
      </div>

      {/* Progress Track */}
      <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200 shadow-inner">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${barColor}`}
          style={{ width: `${clamped}%` }}
        />
      </div>

      {/* Scale Marker Ticks */}
      <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
        <span>0 LOW</span>
        <span>20 MOD</span>
        <span>40 ELEV</span>
        <span>60 HIGH</span>
        <span>80 CRIT</span>
        <span>100</span>
      </div>
    </div>
  );
};
