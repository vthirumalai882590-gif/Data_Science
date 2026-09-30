import React from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon?: React.ReactNode;
  variant?: "default" | "warning" | "danger" | "success";
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  subtext,
  icon,
  variant = "default",
}) => {
  const borderStyles = {
    default: "border-slate-200 hover:border-slate-300",
    warning: "border-amber-200 bg-amber-50/30",
    danger: "border-red-200 bg-red-50/30",
    success: "border-emerald-200 bg-emerald-50/30",
  }[variant];

  return (
    <div
      className={`bg-white rounded-lg border p-4 shadow-xs transition-all flex flex-col justify-between ${borderStyles}`}
    >
      <div className="flex items-center justify-between text-slate-500 mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-600">
          {label}
        </span>
        {icon && <span className="text-slate-400">{icon}</span>}
      </div>
      <div>
        <div className="text-2xl font-bold text-slate-900 tracking-tight font-mono">
          {value}
        </div>
        {subtext && (
          <div className="text-xs text-slate-500 mt-1 flex items-center gap-1">
            {subtext}
          </div>
        )}
      </div>
    </div>
  );
};
