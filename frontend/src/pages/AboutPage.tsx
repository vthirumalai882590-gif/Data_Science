import React from "react";
import { ShieldCheck, BookOpen, AlertOctagon, Cpu, Database, Award } from "lucide-react";

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="border-b border-slate-200 pb-3">
        <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-emerald-700" />
          About FIREGUARD X & Academic Methodology
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Explainable Forest Fire Risk Intelligence, Prediction & Simulation Platform.
        </p>
      </div>

      {/* Mission & Problem Statement */}
      <div className="bg-white rounded-lg border border-slate-200 p-6 shadow-xs space-y-3">
        <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-700" />
          Problem Statement & Academic Solution
        </h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          Wildfires constitute catastrophic socio-environmental disasters accelerated by global climate shifts, prolonged droughts, and severe heat advection. Traditional predictive interfaces frequently function as opaque black boxes that output a single risk probability without explaining contributing drivers, validating data quality, or evaluating potential counterfactual scenarios.
        </p>
        <p className="text-xs text-slate-600 leading-relaxed">
          <b>FIREGUARD X</b> addresses this gap through an end-to-end, interpretable Data Science methodology encompassing:
        </p>
        <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-5">
          <li>
            <b>Data Collection & Cleaning</b>: Authentic meteorological observations and Fire Weather Index components from the UCI Algerian Forest Fires dataset.
          </li>
          <li>
            <b>Feature Engineering</b>: Domain-derived metrics capturing temperature-humidity compounding stress, evapotranspiration drying index, and convective heat advection.
          </li>
          <li>
            <b>Multi-Model Comparison</b>: Systematic benchmark comparing Logistic Regression, Decision Trees, Random Forests, and XGBoost on stratified holdout test partitions.
          </li>
          <li>
            <b>Explainable AI (XAI)</b>: Local Shapley Additive exPlanations (SHAP) attributing directional risk contributions for every environmental input.
          </li>
          <li>
            <b>Environmental Anomaly Detection</b>: Unsupervised Isolation Forest identifying unprecedented compound weather regimes.
          </li>
          <li>
            <b>Educational Cellular Automaton</b>: Pedagogical 2D grid demonstrating wind vector and fuel dryness fire propagation dynamics.
          </li>
        </ul>
      </div>

      {/* Responsible AI Notice */}
      <div className="bg-amber-50/80 border-l-4 border-amber-500 p-5 rounded-r-lg text-xs text-amber-900 space-y-2">
        <div className="flex items-center gap-2 font-bold text-sm text-amber-950">
          <AlertOctagon className="w-5 h-5 text-amber-600" />
          Responsible AI & Operational Limitations
        </div>
        <p className="leading-relaxed">
          <b>1. Probabilistic Likelihood:</b> Predictions represent statistical estimations derived from historical meteorological patterns. They do not constitute guaranteed deterministic certainties.
        </p>
        <p className="leading-relaxed">
          <b>2. Ecosystem Specificity:</b> The trained models reflect Mediterranean and semi-arid North African forest ecosystems (Bejaia & Sidi Bel-abbes). Transferability to boreal or tropical rainforests necessitates domain fine-tuning.
        </p>
        <p className="leading-relaxed">
          <b>3. Educational Simulation Disclaimer:</b> The 2D cellular automaton fire-spread simulator is strictly an educational tool demonstrating directional propagation physics. It must never be deployed for tactical emergency management, live firefighting, or civilian evacuation routing.
        </p>
      </div>

      {/* Provenance and System Specs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs text-xs space-y-2">
          <div className="font-bold text-slate-900 flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-slate-500" />
            Technology Stack
          </div>
          <div className="text-slate-600 space-y-1">
            <div>• <b>Backend:</b> FastAPI, Pydantic V2, SQLAlchemy 2.0, Uvicorn</div>
            <div>• <b>ML Core:</b> scikit-learn, XGBoost, SHAP, NumPy, Pandas</div>
            <div>• <b>Frontend:</b> React 19, TypeScript, Vite, Tailwind CSS, Leaflet</div>
            <div>• <b>Database:</b> SQLite (Production-ready for PostgreSQL)</div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs text-xs space-y-2">
          <div className="font-bold text-slate-900 flex items-center gap-1.5">
            <Database className="w-4 h-4 text-slate-500" />
            Dataset Provenance
          </div>
          <div className="text-slate-600 space-y-1">
            <div>• <b>Repository:</b> UCI Machine Learning Repository</div>
            <div>• <b>Dataset:</b> Algerian Forest Fires Dataset (June–Sept 2012)</div>
            <div>• <b>Validated Rows:</b> 243 instances across 2 regions</div>
            <div>• <b>Evaluation Partition:</b> 80/20 Stratified Partition (Seed 42)</div>
          </div>
        </div>
      </div>
    </div>
  );
};
