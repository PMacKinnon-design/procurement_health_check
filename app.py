
import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Procurement Health Check")

st.title("📊 Procurement Health Check")

st.markdown("### 📥 Upload KPI Performance File")
kpi_file = st.file_uploader("Upload your completed KPI Performance Excel file:", type=["xlsx"])

if kpi_file:
    try:
        xls = pd.ExcelFile(kpi_file)
        st.markdown("✅ File uploaded successfully.")
        st.markdown("🧪 DEBUG: Available sheet names in uploaded file:")
        st.write(xls.sheet_names)

        if "KPI Performance" in xls.sheet_names:
            df = xls.parse("KPI Performance")
            st.markdown("✅ Successfully loaded 'KPI Performance' sheet.")
            st.dataframe(df.head())
        else:
            st.error("❌ Error: Worksheet named 'KPI Performance' not found.")
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
