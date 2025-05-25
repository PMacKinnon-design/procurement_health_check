
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from health_check_parser import parse_health_check

st.set_page_config(layout="wide", page_title="Procurement Health Check")

st.image("KPI_Calculation_Guide.pdf", width=120)
st.title("📋 Procurement Health Check")

st.markdown("This app evaluates your procurement department's health across 8 key categories based on KPIs and qualitative input.")

# Downloadable Templates
with st.expander("📥 Download Templates"):
    col1, col2 = st.columns(2)
    with col1:
        with open("KPI_Performance_Template_FULL.xlsx", "rb") as f:
            st.download_button("📊 Download KPI Template", f, file_name="KPI_Performance_Template_FULL.xlsx")
        with open("KPI_Calculation_Guide.pdf", "rb") as f:
            st.download_button("📘 Download KPI Calculation Guide", f, file_name="KPI_Calculation_Guide.pdf")
    with col2:
        with open("Health_Check_Questionnaire_Template_v2.xlsx", "rb") as f:
            st.download_button("📝 Download Health Check Questionnaire", f, file_name="Health_Check_Questionnaire_Template_v2.xlsx")

# File uploads
st.subheader("📤 Upload Completed Templates")
kpi_file = st.file_uploader("Upload Completed KPI Template", type=["xlsx"])
hc_file = st.file_uploader("Upload Completed Health Check Questionnaire", type=["xlsx"])

if kpi_file and hc_file:
    try:
        kpi_df = pd.read_excel(kpi_file)
        kpi_df["Score"] = pd.qcut(kpi_df["Your Value"] / kpi_df["Benchmark"], q=3, labels=[1, 3, 5])
        st.subheader("📊 KPI Performance Summary")
        st.dataframe(kpi_df)

        # KPI Bar Charts by Category
        st.subheader("📈 KPI Comparison by Category")
        for category in kpi_df["Category"].unique():
            subset = kpi_df[kpi_df["Category"] == category]
            fig, ax = plt.subplots(figsize=(8, 4))
            bar1 = ax.barh(subset["KPI"], subset["Your Value"], color="#1f77b4", label="Your Value")
            bar2 = ax.barh(subset["KPI"], subset["Benchmark"], color="#ff7f0e", alpha=0.6, label="Benchmark")
            ax.set_title(f"{category}")
            ax.legend()
            st.pyplot(fig)

        # Health Check Questionnaire
        st.subheader("🩺 Health Check Questionnaire Scores")
        scores_df, comments_df = parse_health_check(hc_file)
        st.dataframe(scores_df)

        # Health Chart
        st.subheader("📊 Health Check Scores by Category")
        fig2, ax2 = plt.subplots()
        ax2.bar(scores_df["Category"], scores_df["Avg Score"], color="#4CAF50")
        ax2.set_ylim(1, 5)
        ax2.set_ylabel("Avg Score (1–5)")
        ax2.set_xticklabels(scores_df["Category"], rotation=45, ha="right")
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"⚠️ Error processing files: {e}")
else:
    st.info("Please upload both the KPI template and the Health Check questionnaire to begin.")
