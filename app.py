
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from health_check_parser import parse_health_check

st.set_page_config(layout="wide", page_title="Procurement Health Check")

st.title("📊 Procurement Health Check Tool")

# Download Button for KPI Calculation Guide (PDF)
with open("KPI_Calculation_Guide.pdf", "rb") as f:
    st.download_button(
        label="📘 Download KPI Calculation Guide (PDF)",
        data=f,
        file_name="KPI_Calculation_Guide.pdf",
        mime="application/pdf"
    )

# Upload files
st.header("Upload Completed Templates")
kpi_file = st.file_uploader("Upload KPI Performance Template (.xlsx)", type="xlsx")
hc_file = st.file_uploader("Upload Health Check Questionnaire (.xlsx)", type="xlsx")

# Processing
if kpi_file and hc_file:
    try:
        kpi_df = pd.read_excel(kpi_file)
        scores_df, comments_df = parse_health_check(hc_file)

        st.subheader("✅ KPI Performance Data")
        st.dataframe(kpi_df)

        st.subheader("✅ Health Check Scores by Category")
        st.dataframe(scores_df)

        st.subheader("💬 Health Check Comments Summary")
        st.dataframe(comments_df)

        # Example bar chart
        st.subheader("📈 Health Check Category Scores")
        fig, ax = plt.subplots()
        ax.bar(scores_df["Category"], scores_df["Avg Score"], color="#1f77b4")
        ax.set_ylabel("Avg Score (1–5)")
        ax.set_ylim(0, 5)
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing files: {e}")
else:
    st.info("Please upload both files to proceed.")
