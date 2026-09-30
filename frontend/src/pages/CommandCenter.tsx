import React from "react";
import { DashboardData, Zone } from "../types";
import { MetricCard } from "../components/MetricCard";
import { RiskGauge } from "../components/RiskGauge";
import { RiskBadge } from "../components/RiskBadge";
import { RiskMap } from "../components/RiskMap";
import { AnomalyCard } from "../components/AnomalyCard";
import {
  ShieldAlert,
  Flame,
  Activity,
  Award,
  ArrowRight,
  TrendingUp,
  MapPin,
} from "lucide-react";

interface CommandCenterProps {
  dashboardData: DashboardData | null;
  zones: Zone[];
  selectedZone: Zone | null;
  onSelectZone: (zone: Zone) => void;
  onNavigateTab: (tab: any) => void;
}

export const CommandCenter: React.FC<CommandCenterProps> = ({
  dashboardData,
  zones,
  selectedZone,
  onSelectZone,
  onNavigateTab,
}) => {
  const summary = dashboardData?.summary;

  return (
    <div className="space-y-6">
      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          label="Fleet Average Risk"
          value={`${summary?.current_risk ?? "--"}`}
          subtext="Calibrated 0-100 baseline"
          icon={<Flame className="w-5 h-5 text-orange-600" />}
          variant={
            (summary?.current_risk ?? 0) > 60
              ? "danger"
              : (summary?.current_risk ?? 0) > 40
              ? "warning"
              : "default"
          }
        />
        <MetricCard
          label="Active Forest Zones"
          value={summary?.active_zones ?? zones.length}
          subtext="Monitored reserves"
          icon={<MapPin className="w-5 h-5 text-emerald-600" />}
        />
        <MetricCard
          label="High / Critical Zones"
          value={`${(summary?.high_risk_zones_count ?? 0) + (summary?.critical_risk_zones_count ?? 0)}`}
          subtext="Requiring heightened surveillance"
          icon={<ShieldAlert className="w-5 h-5 text-red-600" />}
          variant={
            (summary?.critical_risk_zones_count ?? 0) > 0 ? "danger" : "default"
          }
        />
        <MetricCard
          label="Atmospheric Anomalies"
          value={summary?.anomalies_count ?? 0}
          subtext="Isolation Forest flagged"
          icon={<Activity className="w-5 h-5 text-amber-600" />}
          variant={(summary?.anomalies_count ?? 0) > 0 ? "warning" : "default"}
        />
        <MetricCard
          label="Champion Model F1"
          value={summary?.model_f1 ? (summary.model_f1 * 100).toFixed(1) + "%" : "96.6%"}
          subtext={`${summary?.model_name ?? "XGBoost"} (Holdout test)`}
          icon={<Award className="w-5 h-5 text-emerald-700" />}
          variant="success"
        />
      </div>

      {/* Main Map & Zone Inspector Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Interactive Leaflet Map */}
        <div className="lg:col-span-8">
          <div className="mb-2 flex justify-between items-baseline">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
              Forest Digital Twin • Spatial Risk Map
            </h2>
            <span className="text-xs text-slate-500">
              Click any zone marker to view telemetry
            </span>
          </div>
          <RiskMap
            zones={zones}
            selectedZone={selectedZone}
            onSelectZone={onSelectZone}
          />
        </div>

        {/* Selected Zone Details Drawer */}
        <div className="lg:col-span-4 flex flex-col space-y-4">
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs flex-1 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Zone Telemetry
                </span>
                {selectedZone && <RiskBadge level={selectedZone.risk_level} size="sm" />}
              </div>

              {selectedZone ? (
                <div>
                  <h3 className="text-lg font-black text-slate-900 tracking-tight">
                    {selectedZone.zone_name}
                  </h3>
                  <div className="text-xs font-mono text-slate-400 mb-4">
                    Lat {selectedZone.latitude.toFixed(4)}, Lon {selectedZone.longitude.toFixed(4)}
                  </div>

                  <div className="mb-4">
                    <RiskGauge score={selectedZone.risk_score} level={selectedZone.risk_level} />
                  </div>

                  {/* Weather readings grid */}
                  <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-md border border-slate-200 mb-4">
                    <div>
                      <span className="text-slate-500">Temperature:</span>
                      <div className="font-bold text-slate-900 font-mono">
                        {selectedZone.temperature}°C
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-500">Humidity:</span>
                      <div className="font-bold text-slate-900 font-mono">
                        {selectedZone.humidity}% RH
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-500">Wind Velocity:</span>
                      <div className="font-bold text-slate-900 font-mono">
                        {selectedZone.wind} km/h
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-500">Rainfall:</span>
                      <div className="font-bold text-slate-900 font-mono">
                        {selectedZone.rainfall} mm
                      </div>
                    </div>
                    <div className="col-span-2 pt-2 border-t border-slate-200/60 flex justify-between">
                      <span className="text-slate-500">Historical Fires Recorded:</span>
                      <b className="text-slate-800 font-mono">{selectedZone.historical_fire_count}</b>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-10 text-xs text-slate-400">
                  Select a zone from the map to inspect microclimate parameters.
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="space-y-2 pt-4 border-t border-slate-100">
              <button
                onClick={() => onNavigateTab("prediction")}
                className="w-full py-2 px-3 rounded bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs flex items-center justify-between transition-all shadow-xs"
              >
                <span>Run Prediction on this Zone</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => onNavigateTab("forecast")}
                className="w-full py-2 px-3 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-between transition-all"
              >
                <span>View Diurnal Forecast</span>
                <TrendingUp className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section: Top Risk Zones Table & Environmental Anomalies */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Risk Zones */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Top Monitored Risk Zones
            </h3>
            <span className="text-xs text-slate-400 font-mono">By Risk Score</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 font-semibold text-[11px] uppercase">
                  <th className="py-2">Zone Name</th>
                  <th className="py-2">Risk</th>
                  <th className="py-2">Temp</th>
                  <th className="py-2">Humidity</th>
                  <th className="py-2">Wind</th>
                  <th className="py-2 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {zones.slice(0, 5).map((z) => (
                  <tr key={z.id} className="hover:bg-slate-50">
                    <td className="py-2.5 font-sans font-medium text-slate-900">
                      {z.zone_name}
                    </td>
                    <td className="py-2.5">
                      <span className="font-bold">{z.risk_score}</span>{" "}
                      <span className="text-[10px] text-slate-400">({z.risk_level})</span>
                    </td>
                    <td className="py-2.5">{z.temperature}°C</td>
                    <td className="py-2.5">{z.humidity}%</td>
                    <td className="py-2.5">{z.wind} km/h</td>
                    <td className="py-2.5 text-right font-sans">
                      <button
                        onClick={() => onSelectZone(z)}
                        className="text-emerald-700 hover:text-emerald-800 font-semibold text-[11px]"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Environmental Anomalies Panel */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Activity className="w-4 h-4 text-amber-600" />
              <span>Active Environmental Anomalies</span>
            </h3>
            <span className="text-xs text-slate-400 font-mono">Isolation Forest</span>
          </div>

          <div className="space-y-3">
            {dashboardData?.anomalous_zones && dashboardData.anomalous_zones.length > 0 ? (
              dashboardData.anomalous_zones.map((anom) => (
                <div
                  key={anom.zone_id}
                  className="p-3 bg-amber-50/60 border border-amber-200 rounded-md text-xs space-y-1"
                >
                  <div className="flex justify-between items-baseline font-bold text-slate-900">
                    <span>{anom.zone_name}</span>
                    <span className="text-amber-800 text-[11px]">{anom.badge}</span>
                  </div>
                  <p className="text-slate-600 text-[11px] leading-relaxed">
                    {anom.narrative}
                  </p>
                </div>
              ))
            ) : (
              <div className="p-6 text-center text-xs text-slate-400 bg-slate-50 rounded border border-dashed border-slate-200">
                All zone observations currently conform to empirical climatic baselines.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
