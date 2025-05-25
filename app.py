
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
from health_check_parser import parse_health_check

st.set_page_config(layout="wide", page_title="Procurement Health Check")

st.title("🏥 Procurement Health Check")

# Download KPI Calculation Guide
try:
    with open("KPI_Calculation_Guide.pdf", "rb") as f:
        pdf_bytes = f.read()
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="KPI_Calculation_Guide.pdf">📥 Download KPI Calculation Guide</a>'
    st.markdown(href, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ KPI Calculation Guide PDF not found.")

# File uploads
st.header("📤 Upload Your Completed Templates")
hc_file = st.file_uploader("Upload Completed Health Check Questionnaire Template", type=["xlsx"])
kpi_file = st.file_uploader("Upload Completed KPI Performance Template", type=["xlsx"])

if hc_file and kpi_file:
    try:
        kpi_df, questionnaire_df = parse_health_check(hc_file)
        uploaded_kpi_df = pd.read_excel(kpi_file, engine="openpyxl")

        st.subheader("📊 KPI Performance Summary")
        st.dataframe(uploaded_kpi_df)

        st.subheader("📝 Health Check Scores")
        st.dataframe(questionnaire_df)

    except Exception as e:
        st.error(f"❌ Error processing files: {e}")
else:
    st.info("⬆️ Please upload both files to proceed.")
