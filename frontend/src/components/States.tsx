import React from "react";
import { Loader2, AlertCircle, Inbox } from "lucide-react";

export const LoadingState: React.FC<{ message?: string }> = ({
  message = "Analyzing environmental conditions...",
}) => (
  <div className="flex flex-col items-center justify-center p-12 bg-white rounded-lg border border-slate-200 shadow-xs">
    <Loader2 className="w-8 h-8 text-emerald-700 animate-spin mb-3" />
    <span className="text-sm font-semibold text-slate-700">{message}</span>
    <span className="text-xs text-slate-400 mt-1">
      Computing statistical risk engines and SHAP vectors...
    </span>
  </div>
);

export const ErrorState: React.FC<{
  title?: string;
  message?: string;
  onRetry?: () => void;
}> = ({
  title = "Analysis Error",
  message = "Unable to complete calculation. Please verify environmental inputs and connectivity.",
  onRetry,
}) => (
  <div className="p-6 bg-red-50 border border-red-200 rounded-lg text-red-900 shadow-xs">
    <div className="flex items-center gap-2 mb-2 font-bold text-sm">
      <AlertCircle className="w-4 h-4 text-red-600" />
      <span>{title}</span>
    </div>
    <p className="text-xs text-red-700 leading-relaxed mb-4">{message}</p>
    {onRetry && (
      <button
        onClick={onRetry}
        className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white font-semibold text-xs rounded transition-all shadow-xs"
      >
        Retry Operation
      </button>
    )}
  </div>
);

export const EmptyState: React.FC<{
  title: string;
  description: string;
}> = ({ title, description }) => (
  <div className="flex flex-col items-center justify-center p-8 bg-slate-50 border border-dashed border-slate-300 rounded-lg text-center">
    <Inbox className="w-8 h-8 text-slate-400 mb-2" />
    <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
      {title}
    </span>
    <span className="text-xs text-slate-500 max-w-sm mt-1">{description}</span>
  </div>
);
