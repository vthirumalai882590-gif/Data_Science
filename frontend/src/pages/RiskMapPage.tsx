import React from "react";
import { Zone } from "../types";
import { RiskMap } from "../components/RiskMap";
import { RiskBadge } from "../components/RiskBadge";
import { RiskGauge } from "../components/RiskGauge";
import { Map, ArrowRight, ShieldCheck, Thermometer, Droplets, Wind, CloudRain, Flame } from "lucide-react";

interface RiskMapPageProps {
  zones: Zone[];
  selectedZone: Zone | null;
  onSelectZone: (zone: Zone) => void;
  onNavigateTab: (tab: any) => void;
}

export const RiskMapPage: React.FC<RiskMapPageProps> = ({
  zones,
  selectedZone,
  onSelectZone,
  onNavigateTab,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Map className="w-5 h-5 text-emerald-700" />
            Interactive Spatial Risk Map & Forest Digital Twin
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Geographic vulnerability visualization across monitored Algerian forest reserves with empirical meteorological readings.
          </p>
        </div>

        <div className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded font-mono border border-slate-200">
          Total Monitored Zones: {zones.length}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Map */}
        <div className="lg:col-span-8">
          <RiskMap
            zones={zones}
            selectedZone={selectedZone}
            onSelectZone={onSelectZone}
          />
        </div>

        {/* Selected Zone Deep Dive */}
        <div className="lg:col-span-4 bg-white rounded-lg border border-slate-200 p-5 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
              <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">
                Zone Intelligence Profile
              </span>
              {selectedZone && <RiskBadge level={selectedZone.risk_level} size="sm" />}
            </div>

            {selectedZone ? (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-black text-slate-900 tracking-tight">
                    {selectedZone.zone_name}
                  </h3>
                  <div className="text-xs text-slate-400 font-mono mt-0.5">
                    Region: {selectedZone.region_id === 0 ? "Bejaia (Coastal/Mountain)" : "Sidi Bel-abbes (Steppe/Ridge)"}
                  </div>
                  <div className="text-[11px] text-slate-400 font-mono">
                    Lat: {selectedZone.latitude.toFixed(4)}, Lon: {selectedZone.longitude.toFixed(4)}
                  </div>
                </div>

                <div>
                  <RiskGauge score={selectedZone.risk_score} level={selectedZone.risk_level} />
                </div>

                {/* Weather details */}
                <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-lg border border-slate-200">
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <Thermometer className="w-3.5 h-3.5 text-red-500" />
                    <span>Temp: <b>{selectedZone.temperature}°C</b></span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <Droplets className="w-3.5 h-3.5 text-blue-500" />
                    <span>Humidity: <b>{selectedZone.humidity}%</b></span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <Wind className="w-3.5 h-3.5 text-slate-500" />
                    <span>Wind: <b>{selectedZone.wind} km/h</b></span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <CloudRain className="w-3.5 h-3.5 text-teal-500" />
                    <span>Rainfall: <b>{selectedZone.rainfall} mm</b></span>
                  </div>
                  <div className="col-span-2 pt-2 border-t border-slate-200/60 flex items-center justify-between text-slate-800">
                    <span className="flex items-center gap-1">
                      <Flame className="w-3.5 h-3.5 text-orange-600" />
                      Historical Ground Fires:
                    </span>
                    <b className="font-mono">{selectedZone.historical_fire_count} recorded</b>
                  </div>
                </div>

                {/* FWI Parameters */}
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                  <div className="font-semibold text-slate-700 mb-1.5 text-[11px] uppercase tracking-wider">
                    Canadian FWI Index Components:
                  </div>
                  <div className="grid grid-cols-3 gap-2 font-mono text-[11px] text-slate-600">
                    <div>FFMC: <b>{selectedZone.ffmc}</b></div>
                    <div>DMC: <b>{selectedZone.dmc}</b></div>
                    <div>DC: <b>{selectedZone.dc}</b></div>
                    <div>ISI: <b>{selectedZone.isi}</b></div>
                    <div>BUI: <b>{selectedZone.bui}</b></div>
                    <div>FWI: <b>{selectedZone.fwi}</b></div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-xs text-slate-400">
                Click any zone marker on the map to inspect microclimate parameters and Canadian FWI metrics.
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-100 space-y-2 mt-4">
            <button
              onClick={() => onNavigateTab("prediction")}
              disabled={!selectedZone}
              className="w-full py-2 px-3 rounded bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs flex items-center justify-between transition-all shadow-xs disabled:opacity-40"
            >
              <span>Transfer Zone to Prediction Engine</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigateTab("forecast")}
              disabled={!selectedZone}
              className="w-full py-2 px-3 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-between transition-all disabled:opacity-40"
            >
              <span>View Diurnal Forecast for Zone</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
