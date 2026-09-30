import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Zone } from "../types";
import { Globe, MapPin } from "lucide-react";

interface RiskMapProps {
  zones: Zone[];
  selectedZone: Zone | null;
  onSelectZone: (zone: Zone) => void;
}

export const RiskMap: React.FC<RiskMapProps> = ({
  zones,
  selectedZone,
  onSelectZone,
}) => {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersRef = useRef<{ [key: string]: L.CircleMarker }>({});
  const [filterLevel, setFilterLevel] = useState<string>("ALL");
  const [countryFilter, setCountryFilter] = useState<string>("India");

  const filteredZones = zones.filter((z) => {
    const matchesCountry =
      countryFilter === "ALL" || (z.country || "India") === countryFilter;
    const matchesLevel = filterLevel === "ALL" || z.risk_level === filterLevel;
    return matchesCountry && matchesLevel;
  });

  const getRiskColor = (level: string) => {
    switch (level) {
      case "LOW":
        return "#16a34a";
      case "MODERATE":
        return "#ca8a04";
      case "ELEVATED":
        return "#ea580c";
      case "HIGH":
        return "#dc2626";
      case "CRITICAL":
        return "#7c2d12";
      default:
        return "#475569";
    }
  };

  // Center coordinates by country
  const handleCountryChange = (country: string) => {
    setCountryFilter(country);
    if (!mapInstanceRef.current) return;
    if (country === "India") {
      mapInstanceRef.current.flyTo([20.5937, 78.9629], 5, { duration: 1.2 });
    } else if (country === "Algeria") {
      mapInstanceRef.current.flyTo([35.8, 2.2], 7, { duration: 1.2 });
    } else {
      mapInstanceRef.current.flyTo([24.0, 45.0], 4, { duration: 1.2 });
    }
  };

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Default initial view: India centered
      const initialCenter: [number, number] = [20.5937, 78.9629];
      const map = L.map(mapContainerRef.current, {
        center: initialCenter,
        zoom: 5,
        zoomControl: true,
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;

    // Clear existing markers
    Object.values(markersRef.current).forEach((m) => m.remove());
    markersRef.current = {};

    // Add zone markers
    filteredZones.forEach((z) => {
      const color = getRiskColor(z.risk_level);
      const isSelected = selectedZone?.id === z.id;

      const marker = L.circleMarker([z.latitude, z.longitude], {
        radius: isSelected ? 14 : 9,
        fillColor: color,
        color: isSelected ? "#0f172a" : "#ffffff",
        weight: isSelected ? 3 : 1.5,
        opacity: 1,
        fillOpacity: 0.88,
      }).addTo(map);

      marker.bindPopup(`
        <div style="font-family: sans-serif; font-size: 13px; line-height: 1.4; min-width: 190px;">
          <div style="font-weight: bold; font-size: 14px; margin-bottom: 2px; color: #0f172a;">${z.zone_name}</div>
          <div style="font-size: 11px; color: #64748b; margin-bottom: 5px;">📍 ${z.country || "India"}</div>
          <div style="margin-bottom: 6px;">Risk Index: <b style="color: ${color};">${z.risk_score}/100</b> (${z.risk_level})</div>
          <div style="color: #475569; font-size: 11px;">
            🌡️ Temp: <b>${z.temperature}°C</b><br/>
            💧 Humidity: <b>${z.humidity}% RH</b><br/>
            💨 Wind: <b>${z.wind} km/h</b><br/>
            🌧️ Rainfall: <b>${z.rainfall} mm</b><br/>
            🔥 Historical Fire Incidents: <b>${z.historical_fire_count}</b>
          </div>
        </div>
      `);

      marker.on("click", () => {
        onSelectZone(z);
      });

      markersRef.current[z.id] = marker;
    });

    // If a zone is selected, pan smoothly to it
    if (selectedZone) {
      map.flyTo([selectedZone.latitude, selectedZone.longitude], Math.max(map.getZoom(), 7), {
        duration: 1.0,
      });
    }
  }, [filteredZones, selectedZone]);

  return (
    <div className="bg-white rounded-lg border border-slate-200 overflow-hidden shadow-xs flex flex-col h-[530px]">
      {/* Top Filter and Region Bar */}
      <div className="bg-slate-50 border-b border-slate-200 px-4 py-2.5 flex flex-wrap items-center justify-between gap-2 text-xs">
        {/* Country / Region Selector */}
        <div className="flex items-center gap-1.5">
          <Globe className="w-3.5 h-3.5 text-slate-500" />
          <span className="font-semibold text-slate-700">Region:</span>
          <button
            onClick={() => handleCountryChange("India")}
            className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
              countryFilter === "India"
                ? "bg-emerald-800 text-white shadow-xs"
                : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-100"
            }`}
          >
            🇮🇳 India (Bandipur, Simlipal, Corbett...)
          </button>
          <button
            onClick={() => handleCountryChange("Algeria")}
            className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
              countryFilter === "Algeria"
                ? "bg-emerald-800 text-white shadow-xs"
                : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-100"
            }`}
          >
            🇩🇿 Algeria (Bejaia, Sidi Bel-abbes)
          </button>
          <button
            onClick={() => handleCountryChange("ALL")}
            className={`px-2 py-1 rounded text-xs font-medium transition-all ${
              countryFilter === "ALL"
                ? "bg-slate-800 text-white"
                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-100"
            }`}
          >
            All
          </button>
        </div>

        {/* Risk Level Filter & Legend */}
        <div className="flex items-center gap-2">
          <span className="font-semibold text-slate-600">Risk:</span>
          {["ALL", "CRITICAL", "HIGH", "ELEVATED", "MODERATE", "LOW"].map((lvl) => (
            <button
              key={lvl}
              onClick={() => setFilterLevel(lvl)}
              className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-medium transition-all ${
                filterLevel === lvl
                  ? "bg-slate-900 text-white"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-100"
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>
      </div>

      {/* Map View */}
      <div className="relative flex-1 w-full">
        <div ref={mapContainerRef} className="w-full h-full" />
        <div className="absolute bottom-2 left-2 z-[400] bg-white/95 backdrop-blur-xs text-[10px] text-slate-600 px-2.5 py-1 rounded border border-slate-200 shadow-xs flex items-center gap-1.5">
          <MapPin className="w-3 h-3 text-red-500" />
          <span>
            Showing <b>{filteredZones.length}</b> forest zones in{" "}
            <b>{countryFilter === "ALL" ? "All Regions" : countryFilter}</b>
          </span>
        </div>
      </div>
    </div>
  );
};
