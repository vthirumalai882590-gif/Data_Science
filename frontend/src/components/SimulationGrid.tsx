import React, { useState, useEffect } from "react";
import { Play, Pause, RotateCcw, Compass, AlertOctagon, Info } from "lucide-react";
import { SimulationResult, SimulationStep } from "../types";

interface SimulationGridProps {
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

export const SimulationGrid: React.FC<SimulationGridProps> = ({
  simulationData,
  isLoading,
  onRunSimulation,
}) => {
  const [currentStepIdx, setCurrentStepIdx] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [windSpeed, setWindSpeed] = useState<number>(22.0);
  const [windDirection, setWindDirection] = useState<string>("NE");
  const [dryness, setDryness] = useState<number>(75.0);
  const [duration, setDuration] = useState<number>(24);

  const steps = simulationData?.steps || [];
  const currentStep: SimulationStep | undefined = steps[currentStepIdx];
  const gridDimension = simulationData?.grid_dimension || 9;

  // Auto-play animation loop
  useEffect(() => {
    let interval: any = null;
    if (isPlaying && steps.length > 0) {
      interval = setInterval(() => {
        setCurrentStepIdx((prev) => {
          if (prev >= steps.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, 1400);
    }
    return () => clearInterval(interval);
  }, [isPlaying, steps.length]);

  const handleRun = () => {
    setIsPlaying(false);
    setCurrentStepIdx(0);
    onRunSimulation({
      start_zone: "zone-bej-01",
      wind_speed: windSpeed,
      wind_direction: windDirection,
      dryness: dryness,
      duration_hours: duration,
    });
  };

  const getCellColor = (state: string) => {
    switch (state) {
      case "SAFE":
        return "bg-emerald-100/70 border-emerald-200 text-emerald-800";
      case "AT_RISK":
        return "bg-amber-200/90 border-amber-300 text-amber-900 animate-pulse";
      case "SIMULATED_FIRE":
        return "bg-red-600 border-red-700 text-white font-black shadow-md scale-95";
      case "AFFECTED":
        return "bg-slate-700 border-slate-800 text-slate-300";
      default:
        return "bg-slate-100 border-slate-200 text-slate-500";
    }
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
        <div>
          <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Educational Fire Spread Simulator</span>
            <span className="text-xs font-normal text-slate-500 font-mono">
              2D Cellular Automaton
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Models wind advection vectors and fuel moisture resistance across discrete time horizons.
          </p>
        </div>

        {/* Playback Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentStepIdx(0)}
            disabled={!simulationData || steps.length === 0}
            className="p-1.5 rounded border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-40"
            title="Reset to T+0"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            disabled={!simulationData || steps.length === 0}
            className="px-3 py-1.5 rounded bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 flex items-center gap-1.5 disabled:opacity-40"
          >
            {isPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5" /> Pause
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" /> Play Progression
              </>
            )}
          </button>
        </div>
      </div>

      {/* Prominent Educational Disclaimer Section 2 & 25 */}
      <div className="bg-amber-50/80 border-l-4 border-amber-500 p-3 rounded-r-md text-xs text-amber-900 mb-5 flex items-start gap-2">
        <AlertOctagon className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Educational Simulation Notice:</span> This is a simplified educational cellular simulation and should not be used for real-world emergency response or evacuation planning.
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Parameter Sliders */}
        <div className="lg:col-span-4 space-y-4 bg-slate-50 p-4 rounded-lg border border-slate-200">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Simulation Micro-Climate Parameters
          </h4>

          {/* Wind Speed */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="font-medium text-slate-700">Wind Velocity:</span>
              <span className="font-mono font-bold text-slate-900">{windSpeed} km/h</span>
            </div>
            <input
              type="range"
              min="0"
              max="60"
              step="1"
              value={windSpeed}
              onChange={(e) => setWindSpeed(parseFloat(e.target.value))}
              className="w-full accent-slate-800"
            />
          </div>

          {/* Wind Heading */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="font-medium text-slate-700 flex items-center gap-1">
                <Compass className="w-3.5 h-3.5 text-slate-500" /> Wind Direction:
              </span>
              <span className="font-mono font-bold text-slate-900">{windDirection}</span>
            </div>
            <div className="grid grid-cols-4 gap-1">
              {["N", "NE", "E", "SE", "S", "SW", "W", "NW"].map((dir) => (
                <button
                  key={dir}
                  type="button"
                  onClick={() => setWindDirection(dir)}
                  className={`py-1 text-xs font-mono font-bold rounded border transition-all ${
                    windDirection === dir
                      ? "bg-slate-900 text-white border-slate-900"
                      : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                  }`}
                >
                  {dir}
                </button>
              ))}
            </div>
          </div>

          {/* Dryness Index */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="font-medium text-slate-700">Vegetation Dryness:</span>
              <span className="font-mono font-bold text-slate-900">{dryness}%</span>
            </div>
            <input
              type="range"
              min="10"
              max="95"
              step="1"
              value={dryness}
              onChange={(e) => setDryness(parseFloat(e.target.value))}
              className="w-full accent-slate-800"
            />
          </div>

          {/* Duration */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="font-medium text-slate-700">Duration Horizon:</span>
              <span className="font-mono font-bold text-slate-900">{duration} Hours</span>
            </div>
            <div className="flex gap-2">
              {[12, 24, 48].map((hrs) => (
                <button
                  key={hrs}
                  type="button"
                  onClick={() => setDuration(hrs)}
                  className={`flex-1 py-1 text-xs font-semibold rounded border transition-all ${
                    duration === hrs
                      ? "bg-slate-900 text-white border-slate-900"
                      : "bg-white text-slate-700 border-slate-200 hover:bg-slate-100"
                  }`}
                >
                  {hrs}h
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleRun}
            disabled={isLoading}
            className="w-full py-2.5 rounded bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs uppercase tracking-wider transition-all shadow-xs flex items-center justify-center gap-1.5"
          >
            {isLoading ? "Simulating Cellular Dynamics..." : "Execute Simulation"}
          </button>
        </div>

        {/* Right Column: Cellular Grid Visualizer */}
        <div className="lg:col-span-8 flex flex-col items-center">
          {/* Timeline Step Selector */}
          <div className="flex items-center gap-2 mb-4 w-full justify-center">
            {steps.map((st, idx) => (
              <button
                key={st.time_label}
                onClick={() => {
                  setIsPlaying(false);
                  setCurrentStepIdx(idx);
                }}
                className={`px-3 py-1.5 text-xs font-bold rounded-md border transition-all ${
                  currentStepIdx === idx
                    ? "bg-slate-900 text-white border-slate-900 shadow-xs"
                    : "bg-white text-slate-600 border-slate-200 hover:bg-slate-100"
                }`}
              >
                {st.time_label}
              </button>
            ))}
          </div>

          {/* Grid Container */}
          <div
            className="grid gap-1.5 p-3 bg-slate-900 rounded-xl shadow-lg border border-slate-800"
            style={{
              gridTemplateColumns: `repeat(${gridDimension}, minmax(0, 1fr))`,
            }}
          >
            {currentStep?.cells.map((cell, cIdx) => (
              <div
                key={`${cell.row}-${cell.col}-${cIdx}`}
                className={`w-9 h-9 md:w-11 md:h-11 rounded-sm border flex items-center justify-center text-[10px] font-mono select-none transition-all duration-300 ${getCellColor(
                  cell.state
                )}`}
                title={`Cell [${cell.row}, ${cell.col}]: ${cell.state}`}
              >
                {cell.state === "SIMULATED_FIRE"
                  ? "🔥"
                  : cell.state === "AFFECTED"
                  ? "▪"
                  : cell.state === "AT_RISK"
                  ? "!"
                  : ""}
              </div>
            ))}
          </div>

          {/* State Legend & Counts */}
          <div className="mt-4 flex flex-wrap justify-center gap-4 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-xs bg-emerald-100 border border-emerald-300 inline-block" />
              <span className="text-slate-600">Safe Canopy</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-xs bg-amber-200 border border-amber-400 inline-block" />
              <span className="text-slate-700 font-medium">
                At Risk: <b>{currentStep?.at_risk_count ?? 0}</b>
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-xs bg-red-600 inline-block" />
              <span className="text-red-700 font-bold">
                Active Fire: <b>{currentStep?.active_fire_count ?? 0}</b>
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-xs bg-slate-700 inline-block" />
              <span className="text-slate-600">
                Burned Area: <b>{currentStep?.affected_count ?? 0}</b>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
