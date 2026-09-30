import React from "react";
import { Flame, Shield, Map, Activity, Sliders, PlayCircle, BarChart3, FileText, Info } from "lucide-react";

export type TabType =
  | "command_center"
  | "risk_map"
  | "prediction"
  | "forecast"
  | "what_if"
  | "simulation"
  | "model_lab"
  | "reports"
  | "about";

interface NavbarProps {
  currentTab: TabType;
  onSelectTab: (tab: TabType) => void;
  systemStatus?: string;
  dataMode?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  onSelectTab,
  systemStatus = "OPERATIONAL",
  dataMode = "Historical / Demo",
}) => {
  const navItems: { id: TabType; label: string; icon: React.ReactNode }[] = [
    { id: "command_center", label: "Command Center", icon: <Shield className="w-4 h-4" /> },
    { id: "risk_map", label: "Risk Map", icon: <Map className="w-4 h-4" /> },
    { id: "prediction", label: "Prediction", icon: <Flame className="w-4 h-4" /> },
    { id: "forecast", label: "Forecast", icon: <Activity className="w-4 h-4" /> },
    { id: "what_if", label: "What-If Lab", icon: <Sliders className="w-4 h-4" /> },
    { id: "simulation", label: "Simulation", icon: <PlayCircle className="w-4 h-4" /> },
    { id: "model_lab", label: "Model Lab", icon: <BarChart3 className="w-4 h-4" /> },
    { id: "reports", label: "Reports", icon: <FileText className="w-4 h-4" /> },
    { id: "about", label: "About", icon: <Info className="w-4 h-4" /> },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#1b4332] text-white shadow-md border-b border-[#2d6a4f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Tagline */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => onSelectTab("command_center")}>
            <div className="w-9 h-9 rounded-lg bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center text-emerald-400">
              <Flame className="w-6 h-6 fill-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-black text-lg tracking-wider text-white">FIREGUARD X</span>
                <span className="text-[10px] font-mono uppercase bg-emerald-900/80 border border-emerald-500/30 text-emerald-300 px-1.5 py-0.5 rounded">
                  v1.0
                </span>
              </div>
              <div className="text-[11px] text-emerald-200/70 font-medium tracking-tight">
                Predict. Explain. Simulate. Monitor.
              </div>
            </div>
          </div>

          {/* Right Status Badges */}
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-950/60 border border-emerald-700/50 text-[11px] font-mono text-emerald-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              SYSTEM {systemStatus}
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded bg-slate-900/60 border border-slate-700 text-[10px] font-mono text-slate-300">
              DATA: {dataMode}
            </span>
          </div>
        </div>

        {/* Navigation Tabs Bar */}
        <nav className="flex space-x-1 overflow-x-auto py-1 scrollbar-none border-t border-[#2d6a4f]/50">
          {navItems.map((item) => {
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-md whitespace-nowrap transition-all ${
                  isActive
                    ? "bg-emerald-800 text-white shadow-xs border border-emerald-600/60"
                    : "text-emerald-100/80 hover:bg-[#2d6a4f]/60 hover:text-white"
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
