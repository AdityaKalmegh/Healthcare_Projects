import pandas as pd
import re

# Load Excel file (first sheet or specify sheet_name="Sheet1")
df = pd.read_excel("patient_procedures.xlsx")

# Load CSV
df = pd.read_csv("patient_procedures.csv")

# Function to transform the dataset
def transform_procedures(df):
    long_rows = []

    for _, row in df.iterrows():
        # Extract all unique procedure numbers dynamically
        proc_nums = sorted({int(re.findall(r'Procedure (\d+)', col)[0])
                            for col in df.columns 
                            if re.search(r'Procedure \d+ (Date|Score)', col)})

        for n in proc_nums:
            long_rows.append({
                "patientID": row["patientID"],
                "Doctor": row["Doctor"],
                "ProcedureNumber": n,
                "ProcedureDate": pd.to_datetime(row[f"Procedure {n} Date"]),
                "ProcedureScore": row[f"Procedure {n} Score"]
            })

  print(df_long)

df_long.to_csv("patient_procedures_long.csv", index=False)
df_long.to_excel("patient_procedures_long.xlsx", index=False)

    return pd.DataFrame(long_rows)

# Apply transformation
df_long = transform_procedures(df)
