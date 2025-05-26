
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide", page_title="Procurement Health Check")
st.title("📊 Procurement Health Check")

# Load KPI test file
kpi_file = st.file_uploader("Upload KPI Performance File (CSV)", type=["csv"])

if kpi_file:
    try:
        kpi_df = pd.read_csv(kpi_file)
        st.success("✅ KPI Performance data loaded.")
        st.dataframe(kpi_df)

        if "Category" in kpi_df.columns:
            for category in kpi_df["Category"].unique():
                st.subheader(f"KPI Comparison - {category}")
                cat_df = kpi_df[kpi_df["Category"] == category]
                fig, ax = plt.subplots()
                bar_width = 0.35
                index = range(len(cat_df))
                ax.bar(index, cat_df["Your Value"], bar_width, label="Your Value")
                ax.bar([i + bar_width for i in index], cat_df["Benchmark"], bar_width, label="Benchmark")
                ax.set_xticks([i + bar_width / 2 for i in index])
                ax.set_xticklabels(cat_df["Metric"], rotation=45, ha="right", fontsize=8)
                ax.legend()
                st.pyplot(fig)
        else:
            st.warning("Missing 'Category' column in uploaded KPI file.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
