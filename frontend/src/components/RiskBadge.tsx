import React from "react";

interface RiskBadgeProps {
  level: string;
  size?: "sm" | "md" | "lg";
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, size = "md" }) => {
  const normLevel = (level || "LOW").toUpperCase();

  let bg = "bg-emerald-50 text-emerald-800 border-emerald-300";
  let dot = "bg-emerald-600";
  let icon = "🟢";

  if (normLevel === "MODERATE") {
    bg = "bg-amber-50 text-amber-800 border-amber-300";
    dot = "bg-amber-600";
    icon = "🟡";
  } else if (normLevel === "ELEVATED") {
    bg = "bg-orange-50 text-orange-800 border-orange-300";
    dot = "bg-orange-600";
    icon = "🟠";
  } else if (normLevel === "HIGH") {
    bg = "bg-red-50 text-red-800 border-red-300";
    dot = "bg-red-600";
    icon = "🔴";
  } else if (normLevel === "CRITICAL") {
    bg = "bg-red-100 text-red-950 border-red-500 font-bold";
    dot = "bg-red-900";
    icon = "🟣";
  }

  const sizeClasses = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-2.5 py-1 text-xs font-semibold",
    lg: "px-3.5 py-1.5 text-sm font-bold tracking-wide",
  }[size];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md border ${bg} ${sizeClasses} transition-all`}
    >
      <span className="text-[10px]">{icon}</span>
      <span>{normLevel} RISK</span>
    </span>
  );
};
