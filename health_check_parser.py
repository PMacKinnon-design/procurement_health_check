
import pandas as pd

def parse_health_check(file):
    xls = pd.ExcelFile(file, engine="openpyxl")

    # Parse KPI tab
    kpi_df = pd.read_excel(xls, sheet_name="KPI Performance", engine="openpyxl")

    # Parse questionnaire
    categories = xls.sheet_names[1:]
    records = []
    for cat in categories:
        df = pd.read_excel(xls, sheet_name=cat, engine="openpyxl")
        for idx, row in df.iterrows():
            records.append({
                "Category": cat,
                "Question": row.get("Question", ""),
                "Score": row.get("Score (1–5)", ""),
                "Comment": row.get("Comment", "")
            })
    questionnaire_df = pd.DataFrame(records)
    return kpi_df, questionnaire_df
