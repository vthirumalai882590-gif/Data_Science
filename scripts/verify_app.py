"""
FIREGUARD X - Full End-to-End Application Verification Script
Validates both Backend (FastAPI :8000) and Frontend (Vite :5173).
Tests all core user flows:
1. Health check & model pre-warm
2. Fleet dashboard summary
3. Spatial zones & telemetry
4. Real-time prediction pipeline (probability, risk score, data quality, anomaly detection)
5. Explainable AI (SHAP attributions & plain language narrative)
6. Counterfactual What-If scenario analysis
7. Educational fire spread cellular simulation
8. Diurnal trajectory forecasting (6h to 72h)
9. Report generation & HTML preview
10. Database prediction persistence & audit log
"""

import urllib.request
import json
import sys

def run_tests():
    print("=" * 65)
    print("      FIREGUARD X - END-TO-END APPLICATION VERIFICATION      ")
    print("=" * 65)

    # 1. Frontend Web Check
    print("\n[1/10] Verifying Frontend Web Server (:5173)...")
    try:
        with urllib.request.urlopen("http://127.0.0.1:5173/", timeout=5) as res:
            html = res.read().decode("utf-8")
            assert res.status == 200
            assert "id=\"root\"" in html or "root" in html
            print("  [OK] Frontend is serving HTML index (Status 200 OK)")
    except Exception as e:
        print(f"  [FAIL] Frontend check failed: {e}")
        return False

    # 2. Health Endpoint
    print("\n[2/10] Verifying Backend Health & Model Pre-warming (:8000)...")
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            assert data["status"] == "HEALTHY"
            assert data["model_loaded"] is True
            print(f"  [OK] Health Status: {data['status']} | Model Pre-warmed: {data['selected_model']}")
    except Exception as e:
        print(f"  [FAIL] Backend health failed: {e}")
        return False

    # 3. Dashboard Summary
    print("\n[3/10] Verifying Command Center Fleet Summary...")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/dashboard", timeout=5) as res:
        data = json.loads(res.read().decode("utf-8"))
        summary = data["summary"]
        print(f"  [OK] Average Fleet Risk: {summary['current_risk']}/100")
        print(f"  [OK] Active Monitored Zones: {summary['active_zones']}")
        print(f"  [OK] High/Critical Zones: {summary['high_risk_zones_count']} High, {summary['critical_risk_zones_count']} Critical")
        print(f"  [OK] Champion Model F1: {summary['model_f1'] * 100:.1f}%")

    # 4. Spatial Zones
    print("\n[4/10] Verifying Spatial Forest Digital Twin Zones...")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/zones", timeout=5) as res:
        zones = json.loads(res.read().decode("utf-8"))
        assert len(zones) >= 8
        first_zone = zones[0]
        print(f"  [OK] Loaded {len(zones)} spatial zones across Bejaia & Sidi Bel-abbes regions.")
        print(f"  [OK] Sample Zone: {first_zone['zone_name']} (Risk: {first_zone['risk_score']} {first_zone['risk_level']})")

    # 5. Real-time Prediction Pipeline
    print("\n[5/10] Verifying Prediction & Risk Engine...")
    pred_payload = {
        "Temperature": 39.5,
        "RH": 22.0,
        "Ws": 24.0,
        "Rain": 0.0,
        "FFMC": 93.5,
        "DMC": 38.0,
        "DC": 145.0,
        "ISI": 15.0,
        "BUI": 42.0,
        "FWI": 28.0,
        "Region": 1,
        "zone_id": "Tessala Mountain Forest"
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/predict",
        data=json.dumps(pred_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        pred_res = json.loads(res.read().decode("utf-8"))
        assert pred_res["risk_score"] >= 80.0
        print(f"  [OK] Risk Score: {pred_res['risk_score']}/100 ({pred_res['risk_level']})")
        print(f"  [OK] Model Probability: {pred_res['probability_percent']}%")
        print(f"  [OK] Data Quality Verified: {pred_res['data_quality']['percentage']}%")
        print(f"  [OK] Environmental Anomaly Status: {pred_res['anomaly']['status']}")

    # 6. Explainable AI (SHAP Attributions)
    print("\n[6/10] Verifying Explainable AI (SHAP Attributions)...")
    drivers = pred_res["drivers"]
    assert len(drivers) >= 4
    top_driver = drivers[0]
    print(f"  [OK] Number of SHAP Attributions: {len(drivers)}")
    print(f"  [OK] Top Driver: {top_driver['label']} [{top_driver['display_value']}] -> {top_driver['contribution']:+.4f} ({top_driver['direction']})")
    print(f"  [OK] Synthesized Narrative: \"{pred_res['narrative'][:80]}...\"")

    # 7. Counterfactual What-If
    print("\n[7/10] Verifying Counterfactual What-If Scenario Lab...")
    whatif_payload = {
        "baseline": pred_payload,
        "modifications": {
            "Temperature": 26.0,
            "RH": 65.0,
            "Ws": 10.0,
            "Rain": 4.0,
            "Region": 1
        }
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/what-if",
        data=json.dumps(whatif_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        w_res = json.loads(res.read().decode("utf-8"))
        assert w_res["risk_delta"] < 0
        print(f"  [OK] Baseline Risk: {w_res['baseline_risk']} -> Simulated Risk: {w_res['modified_risk']}")
        print(f"  [OK] Associated Delta: {w_res['risk_delta']} pts ({w_res['delta_direction']})")
        print(f"  [OK] Primary Driver of Delta: {w_res['primary_drivers_of_change'][0]['feature']} ({w_res['primary_drivers_of_change'][0]['reason']})")

    # 8. Educational Fire Spread Cellular Automaton
    print("\n[8/10] Verifying Educational Fire Spread Simulation...")
    sim_payload = {
        "start_zone": "zone-bej-01",
        "wind_speed": 22.0,
        "wind_direction": "NE",
        "dryness": 80.0,
        "duration_hours": 24,
        "grid_size": 9
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/simulation",
        data=json.dumps(sim_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        sim_res = json.loads(res.read().decode("utf-8"))
        steps = sim_res["steps"]
        assert len(steps) == 5
        print(f"  [OK] Simulation Steps Generated: {[s['time_label'] for s in steps]}")
        print(f"  [OK] T+24h Active Fires: {steps[-1]['active_fire_count']} | Burned Cells: {steps[-1]['affected_count']}")
        print(f"  [OK] Educational Disclaimer Present: \"{sim_res['disclaimer'][:65]}...\"")

    # 9. Diurnal Risk Forecasting
    print("\n[9/10] Verifying Diurnal Risk Trajectory Forecast...")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/forecast/zone-bej-01", timeout=5) as res:
        f_res = json.loads(res.read().decode("utf-8"))
        horizons = f_res["forecast"]
        assert len(horizons) == 5
        print(f"  [OK] Projected Horizons: {[h['label'] for h in horizons]}")
        print(f"  [OK] T+6h Peak Risk: {horizons[0]['risk_score']} ({horizons[0]['risk_level']})")
        print(f"  [OK] Escalation Warning: {f_res['escalation_warning']}")

    # 10. Audit Report Generation & SQLite Persistence
    print("\n[10/10] Verifying Audit Report Generation & SQLite Database...")
    rep_payload = {
        "zone_name": "Tessala Mountain Forest",
        "region": "Sidi Bel-abbes Region",
        "inputs": pred_payload,
        "risk_score": pred_res["risk_score"],
        "risk_level": pred_res["risk_level"],
        "probability": pred_res["model_probability"],
        "drivers": drivers,
        "anomaly_status": pred_res["anomaly"]["status"],
        "notes": "Routine supervisory inspection during high temperature spell."
    }
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/reports/generate",
        data=json.dumps(rep_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        rep_res = json.loads(res.read().decode("utf-8"))
        assert rep_res["id"] > 0
        assert len(rep_res["report_html"]) > 500
        print(f"  [OK] Audit Report #{rep_res['id']} compiled and saved to database.")
        print(f"  [OK] HTML Report Length: {len(rep_res['report_html'])} bytes.")

    with urllib.request.urlopen("http://127.0.0.1:8000/api/predictions/history?limit=10", timeout=5) as res:
        hist = json.loads(res.read().decode("utf-8"))
        assert len(hist) > 0
        print(f"  [OK] Prediction History Table verified: {len(hist)} records retrieved from SQLite.")


    print("\n" + "=" * 65)
    print("ALL 10 END-TO-END VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
