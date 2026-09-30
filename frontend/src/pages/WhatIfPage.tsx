import React from "react";
import { PredictionInput, WhatIfResult } from "../types";
import { WhatIfPanel } from "../components/WhatIfPanel";
import { Sliders, Lightbulb } from "lucide-react";

interface WhatIfPageProps {
  onRunWhatIf: (baseline: PredictionInput, modifications: PredictionInput) => Promise<WhatIfResult>;
}

export const WhatIfPage: React.FC<WhatIfPageProps> = ({ onRunWhatIf }) => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-3">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <Sliders className="w-5 h-5 text-emerald-700" />
          Counterfactual What-If Simulator
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Interactively modify ambient weather and moisture inputs to evaluate associated statistical changes in model fire risk scores.
        </p>
      </div>

      <WhatIfPanel onRunWhatIf={onRunWhatIf} />

      {/* Analytical Guidelines Note */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
        <div className="flex items-start gap-2.5">
          <Lightbulb className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
          <div className="text-xs text-slate-600 leading-relaxed">
            <b className="text-slate-900">Understanding Counterfactual Analysis in Machine Learning:</b>
            <p className="mt-1">
              Counterfactual what-if analysis enables environmental scientists and decision-makers to inspect model sensitivity across varying input perturbations. The reported risk point delta reflects the learned associations within the historical observation distribution. Remember that correlation does not guarantee direct operational causality; model outcomes should be corroborated with real-time on-the-ground forest patrol surveillance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
