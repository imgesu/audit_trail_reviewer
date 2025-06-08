# AI-Powered Audit Trail Validator – Compliant Anomaly Review Tool
# Author: imge

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
import plotly.express as px
import shap
import matplotlib.pyplot as plt
from datetime import datetime

# 🔒 Streamlit setup – local use only
st.set_page_config(page_title="Audit Trail Validator – GxP Compliant", layout="wide")
st.title("🧠 Audit Trail Validator – AI Anomaly Detection & Review Assistant")

# 📒 Utility: Write local audit log
def write_audit_log(action):
    with open("audit_log.txt", "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {action}\n")

# 📥 Step 1: File upload
uploaded_file = st.file_uploader("📂 Upload Audit Trail CSV (from Jira, LIMS, MES, etc.)", type="csv")

if uploaded_file:
    write_audit_log("File uploaded")
    st.success("✅ File loaded successfully (data is never sent externally)")
    
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("🔎 Raw Data Preview")
        st.dataframe(df.head())

        # 📊 Step 2: Select numeric features
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        st.sidebar.title("⚙️ Configuration")
        selected_features = st.sidebar.multiselect("Select numeric columns for anomaly detection", numeric_cols, default=numeric_cols)

        if not selected_features:
            st.warning("Please select at least one numeric column.")
            write_audit_log("No features selected")
        else:
            write_audit_log(f"Selected features: {selected_features}")
            X = df[selected_features]

            # 🧠 Step 3: Train ML model
            model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
            model.fit(X)
            df['anomaly_score'] = model.decision_function(X)
            df['is_anomaly'] = model.predict(X)
            write_audit_log("IsolationForest model trained")

            # 📊 Step 4: Visual Explorer
            st.subheader("📊 Visual Anomaly Explorer")
            if 'Temp_C' in df.columns and 'pH' in df.columns:
                fig = px.scatter(
                    df, x="Temp_C", y="pH",
                    color=df['is_anomaly'].map({1: "Normal", -1: "Anomaly"}),
                    symbol=df.get("InjectedAnomaly", False).map(lambda x: "Injected" if x else "Regular"),
                    title="Anomaly Detection: Temperature vs pH"
                )
                st.plotly_chart(fig, use_container_width=True)

            # 🚨 Step 5: Anomaly Review Table
            anomalies = df[df['is_anomaly'] == -1]
            st.subheader(f"🚨 Detected Anomalies: {len(anomalies)}")
            st.dataframe(anomalies)
            write_audit_log(f"{len(anomalies)} anomalies detected")

            # 📈 Step 6: Validation Report (if labeled)
            if "InjectedAnomaly" in df.columns:
                true_anomalies = df[df["InjectedAnomaly"] == True]
                true_detected = true_anomalies[true_anomalies["is_anomaly"] == -1]
                recall = len(true_detected) / len(true_anomalies) * 100 if len(true_anomalies) > 0 else 0
                st.subheader("📈 Validation Report")
                st.markdown(f"**Injected Anomalies:** {len(true_anomalies)}")
                st.markdown(f"**Correctly Detected:** {len(true_detected)}")
                st.markdown(f"**Detection Accuracy:** {recall:.2f}%")
                write_audit_log("Validation report generated")

            # 🔍 Step 7: Explainable AI (SHAP)
            st.subheader("🔍 Explainable AI – Feature Impact")
            try:
                explainer = shap.Explainer(model, X)
                shap_values = explainer(X)
                st.write("Top contributing features for anomalies (sample of 100 rows):")
                fig, ax = plt.subplots(figsize=(10, 6))
                shap.summary_plot(shap_values[:100], X.iloc[:100], plot_type="bar", show=False)
                st.pyplot(fig)
                write_audit_log("SHAP summary plot generated")
            except Exception as e:
                st.warning(f"SHAP explanation failed: {e}")
                write_audit_log(f"SHAP explanation error: {e}")

            # 💾 Step 8: Optional model saving
            if st.button("💾 Save Model (local only)"):
                os.makedirs("models", exist_ok=True)
                joblib.dump(model, "models/gxp_anomaly_model.pkl")
                st.success("Model saved locally.")
                write_audit_log("Model saved")

            # 📤 Step 9: Download annotated CSV
            if st.download_button("📤 Download Results", df.to_csv(index=False), file_name="audit_review_output.csv"):
                write_audit_log("Annotated output downloaded")

    except Exception as e:
        st.error(f"🚫 File processing failed: {e}")
        write_audit_log(f"Upload error: {e}")

else:
    st.info("Please upload a CSV file to begin your local, AI-driven audit review.")
