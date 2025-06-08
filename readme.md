# 🧠 GxP Validator – AI-Powered Audit Trail Review Tool

**GxP Validator** is a secure, offline, and explainable AI tool designed to assist pharma and life sciences teams with:
- Anomaly detection in audit trail data (e.g., Jira, LIMS, MES)
- Visual inspection of anomalies
- Generation of validation-ready reports
- Full audit trail logging for compliance

---

## ✅ Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 📂 CSV Input                  | Load audit trail data from any system (Jira, MES, LIMS)                     |
| 🧠 AI Anomaly Detection       | Uses Isolation Forest to detect data deviations                            |
| 🔍 SHAP Explainability        | Transparent feature-level insight into each anomaly                        |
| 📈 Validation Report          | Accuracy comparison using labeled injected anomalies                       |
| 📝 Audit Review Report        | Generates a downloadable TXT file summarizing top findings                 |
| 🧾 Audit Trail Logging        | Logs user actions for traceability (21 CFR Part 11 / Annex 11 support)     |
| 💾 Offline Mode               | No internet needed – data stays local (no cloud upload)                    |

---

## 🧪 How to Use (No Install)

1. 📥 Unzip the folder.
2. ▶️ Double-click `run_app.bat` or run:
   ```bash
   streamlit run app.py
