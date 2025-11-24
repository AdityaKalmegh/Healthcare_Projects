import pandas as pd
import re

def transform_procedures(df):
    long_rows = []

    for _, row in df.iterrows():

        # Find all unique procedure numbers based on both Date and Score patterns
        proc_nums = sorted({
            int(re.findall(r'Procedure\s+(\d+)', col)[0])
            for col in df.columns
            if re.search(r'Procedure\s+\d+', col)
        })

        for n in proc_nums:

            # Match date column (consistent)
            date_col = f"Procedure {n} Date"

            # Match score column (may contain spaces or colon variations)
            score_pattern = re.compile(
                rf"Procedure {n}\s*:?\s*PCL-5 Score",
                flags=re.IGNORECASE
            )

            # Identify the score column dynamically (handles both formats)
            score_col = next((c for c in df.columns if score_pattern.fullmatch(c)), None)

            if score_col is None:
                raise ValueError(f"Score column for Procedure {n} not found.")

            long_rows.append({
                "patientID": row["patientID"],
                "Therapist": row["Therapist"],
                "ProcedureNumber": n,
                "ProcedureDate": pd.to_datetime(row[date_col]),
                "PCL5_Score": row[score_col],
            })
df_long = transform_procedures(df)
print(df_long)

    return pd.DataFrame(long_rows)
