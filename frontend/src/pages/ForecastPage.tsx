import React, { useState, useEffect } from "react";
import { Zone, ZoneForecast } from "../types";
import { ForecastChart } from "../components/ForecastChart";
import { LoadingState } from "../components/States";
import { Activity, Clock, AlertTriangle, ShieldCheck } from "lucide-react";

interface ForecastPageProps {
  zones: Zone[];
  selectedZone: Zone | null;
  onSelectZone: (zone: Zone) => void;
  onFetchForecast: (zoneId: string) => Promise<ZoneForecast>;
}

export const ForecastPage: React.FC<ForecastPageProps> = ({
  zones,
  selectedZone,
  onSelectZone,
  onFetchForecast,
}) => {
  const [forecast, setForecast] = useState<ZoneForecast | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const activeZoneId = selectedZone?.id || (zones.length > 0 ? zones[0].id : "");

  const loadForecast = async (zoneId: string) => {
    if (!zoneId) return;
    setLoading(true);
    try {
      const data = await onFetchForecast(zoneId);
      setForecast(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeZoneId) {
      loadForecast(activeZoneId);
    }
  }, [activeZoneId]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-700" />
            Diurnal Environmental Risk Forecasting
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Projects forward-looking fire-risk scores at 6h, 12h, 24h, 48h, and 72h based on diurnal thermodynamic cycles and atmospheric inertia.
          </p>
        </div>

        {/* Zone Selector Dropdown */}
        <div className="flex items-center gap-2 text-xs">
          <span className="font-semibold text-slate-600">Select Zone:</span>
          <select
            value={activeZoneId}
            onChange={(e) => {
              const matched = zones.find((z) => z.id === e.target.value);
              if (matched) {
                onSelectZone(matched);
                loadForecast(matched.id);
              }
            }}
            className="p-1.5 rounded border border-slate-300 bg-white font-medium text-slate-800 text-xs focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
          >
            {zones.map((z) => (
              <option key={z.id} value={z.id}>
                {z.zone_name} ({z.risk_level})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <LoadingState message="Generating diurnal thermodynamic trajectory..." />
      ) : (
        <div className="space-y-6">
          <ForecastChart forecast={forecast} />

          {/* Academic Methodology Details Section 22 */}
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
              Forecasting Methodology & Temporal Assumptions
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Because the UCI Algerian Forest Fires dataset contains daily sequential records rather than sub-hourly automated weather stations, this forecast applies a <b>diurnal solar-radiation thermodynamic cycle model</b> combined with <b>empirical 24-hour meteorological inertia</b>. Midday temperatures peak between T+6h and T+24h while night radiative cooling elevates relative humidity at T+12h. Projected environmental vectors are subsequently processed through the trained machine learning pipeline.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
