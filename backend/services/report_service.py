"""
FIREGUARD X - Report Generation Service
Generates professional environmental risk audit reports with styling,
data quality tables, SHAP feature rankings, and disclaimers.
"""

import datetime

def generate_html_report(data: dict) -> str:
    zone_name = data.get("zone_name", "Monitored Forest Zone")
    region = data.get("region", "Bejaia / Sidi Bel-abbes")
    risk_score = data.get("risk_score", 0.0)
    risk_level = data.get("risk_level", "LOW")
    probability = data.get("probability", 0.0)
    inputs = data.get("inputs", {})
    drivers = data.get("drivers", [])
    anomaly_status = data.get("anomaly_status", "NORMAL")
    notes = data.get("notes", "Routine algorithmic forest surveillance.")
    generated_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Determine risk badge color
    badge_color = "#16a34a"
    if risk_level == "MODERATE": badge_color = "#ca8a04"
    elif risk_level == "ELEVATED": badge_color = "#ea580c"
    elif risk_level == "HIGH": badge_color = "#dc2626"
    elif risk_level == "CRITICAL": badge_color = "#7c2d12"

    drivers_rows = ""
    for d in drivers[:6]:
        direction_color = "#dc2626" if d.get("is_positive", True) else "#16a34a"
        drivers_rows += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;"><b>{d.get('label', d.get('feature'))}</b></td>
            <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{d.get('display_value', 'N/A')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; color: {direction_color}; font-weight: bold;">
                {d.get('contribution', 0.0):+.4f} ({d.get('direction', 'Impact')})
            </td>
        </tr>
        """

    inputs_chips = "".join([
        f"<span style='display:inline-block; margin: 4px; padding: 4px 8px; background: #f3f4f6; border-radius: 4px; font-size: 13px; font-family: monospace;'><b>{k}</b>: {v}</span>"
        for k, v in inputs.items()
    ])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>FIREGUARD X - Risk Intelligence Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1f2937; line-height: 1.5; padding: 32px; background: #fafafa; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e5e7eb; }}
            .header {{ border-bottom: 3px solid #1b4332; padding-bottom: 16px; margin-bottom: 24px; }}
            .title {{ font-size: 26px; font-weight: 800; color: #1b4332; margin: 0; }}
            .subtitle {{ font-size: 14px; color: #4b5563; margin-top: 4px; }}
            .card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 18px; margin-bottom: 20px; }}
            .risk-banner {{ display: flex; align-items: center; justify-content: space-between; padding: 16px; border-radius: 6px; background: {badge_color}15; border-left: 6px solid {badge_color}; margin-bottom: 24px; }}
            .risk-title {{ font-size: 20px; font-weight: bold; color: {badge_color}; }}
            .risk-score {{ font-size: 32px; font-weight: 900; color: {badge_color}; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 14px; }}
            th {{ text-align: left; padding: 8px; background: #f3f4f6; border-bottom: 2px solid #d1d5db; font-weight: 600; }}
            .disclaimer {{ margin-top: 32px; padding: 16px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; font-size: 12px; color: #991b1b; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="title">FIREGUARD X</h1>
                <div class="subtitle">Environmental Risk Intelligence & Predictive Forest Protection Platform</div>
                <div style="font-size: 12px; color: #6b7280; margin-top: 8px;">Generated: {generated_at} | Region: {region}</div>
            </div>

            <div class="risk-banner">
                <div>
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #4b5563;">Assessed Zone</div>
                    <div style="font-size: 22px; font-weight: bold; color: #111827;">{zone_name}</div>
                    <div class="risk-title" style="margin-top: 4px;">{risk_level} RISK LEVEL</div>
                </div>
                <div style="text-align: right;">
                    <div class="risk-score">{risk_score}<span style="font-size: 16px; font-weight: normal; color: #6b7280;">/100</span></div>
                    <div style="font-size: 13px; color: #4b5563;">Calibrated Model Probability: <b>{probability:.1%}</b></div>
                </div>
            </div>

            <div class="card">
                <h3 style="margin-top: 0; font-size: 16px; color: #111827; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">1. Environmental Parameters Inspected</h3>
                <div style="margin-top: 10px;">{inputs_chips}</div>
                <div style="margin-top: 12px; font-size: 13px; color: #4b5563;">
                    <b>Environmental Anomaly Status:</b> <span style="font-weight: 600;">{anomaly_status}</span>
                </div>
            </div>

            <div class="card">
                <h3 style="margin-top: 0; font-size: 16px; color: #111827; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">2. Explainable AI Feature Contributions (SHAP)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Observed Value</th>
                            <th>Direction & Shapley Contribution</th>
                        </tr>
                    </thead>
                    <tbody>
                        {drivers_rows}
                    </tbody>
                </table>
            </div>

            <div class="card">
                <h3 style="margin-top: 0; font-size: 16px; color: #111827;">3. Operational Monitoring Notes</h3>
                <p style="font-size: 14px; color: #374151; margin-bottom: 0;">{notes}</p>
            </div>

            <div class="disclaimer">
                <b>Responsible AI & Academic Research Notice:</b><br/>
                This report is compiled by FIREGUARD X based on historical environmental modeling and machine learning algorithms (XGBoost/Random Forest). Wildfire predictions are probabilistic estimations of environmental vulnerability and must not be used as the sole basis for real-world life-safety emergency operations.
            </div>
        </div>
    </body>
    </html>
    """
    return html
