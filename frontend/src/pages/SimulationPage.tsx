import React from "react";
import { SimulationResult } from "../types";
import { SimulationGrid } from "../components/SimulationGrid";
import { PlayCircle, ShieldCheck } from "lucide-react";

interface SimulationPageProps {
  simulationData: SimulationResult | null;
  isLoading: boolean;
  onRunSimulation: (params: {
    start_zone: string;
    wind_speed: number;
    wind_direction: string;
    dryness: number;
    duration_hours: number;
  }) => void;
}

export const SimulationPage: React.FC<SimulationPageProps> = ({
  simulationData,
  isLoading,
  onRunSimulation,
}) => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-3">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <PlayCircle className="w-5 h-5 text-emerald-700" />
          Educational Wildfire Spread Simulation
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Interactive cellular automaton simulating directional flame progression governed by wind vectors, fuel dryness, and neighborhood adjacency.
        </p>
      </div>

      <SimulationGrid
        simulationData={simulationData}
        isLoading={isLoading}
        onRunSimulation={onRunSimulation}
      />
    </div>
  );
};
