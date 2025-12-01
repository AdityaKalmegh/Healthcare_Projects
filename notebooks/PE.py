import pandas as pd
import re

def transform_pe_sessions(df_PE):
    """
    Transform wide-format PE (Prolonged Exposure) session data
    into long-format rows with Date, PCL-5, and BDI-2 Scores.
    """

    long_rows = []

    # ---- Identify all unique PE session numbers ----
    session_numbers = sorted({
        int(re.findall(r'PE\s*(\d+)', col)[0])
        for col in df_PE.columns
        if re.search(r'PE\s*\d+', col)
    })

    for _, row in df_PE.iterrows():

        for session_num in session_numbers:

            # ---- PE Date ----
            date_pattern = re.compile(
                rf"PE\s*{session_num}\s*Date",
                re.IGNORECASE
            )
            date_col = next((c for c in df_PE.columns if date_pattern.search(c)), None)
            if date_col is None:
                raise ValueError(f"Date column for PE {session_num} not found.")

            # ---- PE PCL-5 Score ----
            pcl_pattern = re.compile(
                rf"PE\s*{session_num}\s*PCL-5\s*Score",
                re.IGNORECASE
            )
            pcl_col = next((c for c in df_PE.columns if pcl_pattern.search(c)), None)
            if pcl_col is None:
                raise ValueError(f"PCL-5 Score column for PE {session_num} not found.")

            # ---- PE BDI-2 Score ----
            bdi_pattern = re.compile(
                rf"PE\s*{session_num}\s*BDI-2\s*Score",
                re.IGNORECASE
            )
            bdi_col = next((c for c in df_PE.columns if bdi_pattern.search(c)), None)
            if bdi_col is None:
                raise ValueError(f"BDI-2 Score column for PE {session_num} not found.")

            # ---- Build long-format row ----
            long_rows.append({
                "ID": row["ID"],
                "PatientID": row["PatientID"],
                "PE_Session": session_num,
                "PE_Date": pd.to_datetime(row[date_col]) if pd.notna(row[date_col]) else None,
                "PCL5_Score": row[pcl_col],
                "BDI2_Score": row[bdi_col],
            })

    return pd.DataFrame(long_rows)
