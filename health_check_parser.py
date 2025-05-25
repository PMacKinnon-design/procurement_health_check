
import pandas as pd

def parse_health_check(file):
    xls = pd.ExcelFile(file)
    scores = []
    comments = []

    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        if "Score (1–5)" in df.columns and "Comment" in df.columns:
            avg_score = df["Score (1–5)"].mean()
            joined_comments = "; ".join([str(c) for c in df["Comment"].dropna()])
            scores.append({"Category": sheet, "Avg Score": round(avg_score, 2)})
            comments.append({"Category": sheet, "Comments": joined_comments})

    scores_df = pd.DataFrame(scores)
    comments_df = pd.DataFrame(comments)
    return scores_df, comments_df
