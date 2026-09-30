import React, { useState, useEffect } from "react";
import { FileText, Download, Printer, Search, Calendar, ShieldCheck, History } from "lucide-react";
import { PredictionHistoryItem } from "../types";
import { RiskBadge } from "../components/RiskBadge";

interface ReportsPageProps {
  onFetchHistory: () => Promise<PredictionHistoryItem[]>;
  onFetchReportsList: () => Promise<any[]>;
}

export const ReportsPage: React.FC<ReportsPageProps> = ({
  onFetchHistory,
  onFetchReportsList,
}) => {
  const [history, setHistory] = useState<PredictionHistoryItem[]>([]);
  const [reportsList, setReportsList] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [hist, reps] = await Promise.all([onFetchHistory(), onFetchReportsList()]);
        setHistory(hist);
        setReportsList(reps);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredHistory = history.filter((item) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      item.zone_id.toLowerCase().includes(q) ||
      item.risk_level.toLowerCase().includes(q) ||
      item.risk_score.toString().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-700" />
            Audit Reports & Operational Surveillance History
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Historical audit logs and compiled intelligence reports persisted in SQLite database.
          </p>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-2.5 top-2" />
          <input
            type="text"
            placeholder="Search by zone or risk level..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-8 pr-3 py-1.5 text-xs border border-slate-300 rounded bg-white w-64 focus:ring-2 focus:ring-emerald-600 focus:outline-hidden"
          />
        </div>
      </div>

      {/* Generated Reports List */}
      {reportsList.length > 0 && (
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3 flex items-center gap-2">
            <Printer className="w-4 h-4 text-slate-500" />
            <span>Generated Printable Intelligence Reports</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {reportsList.map((rep) => (
              <div
                key={rep.id}
                className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col justify-between"
              >
                <div>
                  <div className="text-xs font-bold text-slate-900">{rep.zone_name}</div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                    {new Date(rep.timestamp).toLocaleString()}
                  </div>
                  <div className="mt-2 flex items-center justify-between">
                    <span className="font-mono font-bold text-sm text-slate-900">
                      Score: {rep.risk_score}
                    </span>
                    <RiskBadge level={rep.risk_level} size="sm" />
                  </div>
                </div>

                <a
                  href={rep.view_url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-3 text-center text-xs font-semibold text-emerald-700 hover:text-emerald-800 bg-white border border-slate-200 rounded py-1.5 transition-all shadow-xs flex items-center justify-center gap-1.5"
                >
                  <Printer className="w-3.5 h-3.5" /> View / Print Report
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Prediction History Table */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
        <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <History className="w-4 h-4 text-slate-500" />
            <span>Prediction Audit Log (SQLite Database)</span>
          </h3>
          <span className="text-xs font-mono text-slate-400">
            Total Records: {filteredHistory.length}
          </span>
        </div>

        {filteredHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[11px]">
                  <th className="py-2.5 px-3">Timestamp (UTC)</th>
                  <th className="py-2.5 px-3">Zone / Target</th>
                  <th className="py-2.5 px-3">Risk Score</th>
                  <th className="py-2.5 px-3">Risk Level</th>
                  <th className="py-2.5 px-3">Model Probability</th>
                  <th className="py-2.5 px-3">Data Quality</th>
                  <th className="py-2.5 px-3">Weather Inputs</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50">
                    <td className="py-2.5 px-3 text-slate-500">
                      {new Date(item.timestamp).toLocaleString()}
                    </td>
                    <td className="py-2.5 px-3 font-sans font-medium text-slate-900">
                      {item.zone_id}
                    </td>
                    <td className="py-2.5 px-3 font-bold">{item.risk_score}</td>
                    <td className="py-2.5 px-3 font-sans">
                      <RiskBadge level={item.risk_level} size="sm" />
                    </td>
                    <td className="py-2.5 px-3">{(item.probability * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-emerald-700">
                      {(item.data_quality * 100).toFixed(0)}%
                    </td>
                    <td className="py-2.5 px-3 text-[11px] text-slate-500">
                      T: {item.input_data?.Temperature ?? "--"}°C | RH:{" "}
                      {item.input_data?.RH ?? "--"}% | Ws: {item.input_data?.Ws ?? "--"} km/h
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-10 text-center text-xs text-slate-400">
            No prediction logs found in the database. Run predictions to accumulate history.
          </div>
        )}
      </div>
    </div>
  );
};
