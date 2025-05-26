import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Procurement Health Check")

st.title("📊 Procurement Health Check Tool")
st.markdown("Upload your completed KPI and Health Check Questionnaire templates below:")

# Upload KPI File
kpi_file = st.file_uploader("📄 Upload KPI Performance Template", type=["xlsx"])
benchmark_file = "benchmark_data_full.csv"  # Must be present in same directory

if kpi_file:
    try:
        # Read KPI data
        xls = pd.ExcelFile(kpi_file)
        st.success("✅ KPI file uploaded successfully.")
        st.write("🧪 DEBUG: Available sheet names in uploaded file:")
        st.write(xls.sheet_names)

        if "KPI Performance" in xls.sheet_names:
            kpi_df = pd.read_excel(xls, sheet_name="KPI Performance")
            st.write("📄 KPI Performance Sheet Loaded:")
            st.dataframe(kpi_df)

            # Load benchmark data
            benchmark_df = pd.read_csv(benchmark_file)
            merged_df = pd.merge(kpi_df, benchmark_df, on="KPI Name", how="left")
            merged_df["Difference"] = merged_df["Your Value"] - merged_df["Benchmark Value"]

            st.subheader("📊 KPI Comparison Table")
            st.dataframe(merged_df)

            # Charts by Category
            categories = merged_df["Category"].unique()
            for category in categories:
                subset = merged_df[merged_df["Category"] == category]
                fig, ax = plt.subplots()
                ax.barh(subset["KPI Name"], subset["Your Value"], label="Your Value", color="blue")
                ax.barh(subset["KPI Name"], subset["Benchmark Value"], alpha=0.5, label="Benchmark", color="orange")
                ax.set_title(f"KPI Comparison - {category}")
                ax.legend()
                st.pyplot(fig)

        else:
            st.error("❌ Sheet 'KPI Performance' not found in the uploaded file.")

    except Exception as e:
        st.error(f"❌ Error processing files: {e}")