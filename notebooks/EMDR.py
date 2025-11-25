import pandas as pd
import re

def transform_emdr_sessions(df_EMDR):
    """
    Transform wide-format EMDR session data into long-format rows.
    Supports inconsistent spacing, Excel artifacts, and multiple EMDR sessions.
    """

    long_rows = []

    # ---- Identify all EMDR session numbers dynamically ----
    session_numbers = sorted({
        int(re.findall(r'EMDR\s*(\d+)', col)[0])
        for col in df_EMDR.columns
        if re.search(r'EMDR\s*\d+', col)
    })

    for _, row in df_EMDR.iterrows():

        for session_num in session_numbers:

            # ---- Date column ----
            date_pattern = re.compile(
                rf"EMDR\s*{session_num}\s*Date",
                re.IGNORECASE
            )
            date_col = next((c for c in df_EMDR.columns if date_pattern.search(c)), None)
            if date_col is None:
                raise ValueError(f"Date column for EMDR {session_num} not found.")

            # ---- PCL-5 Score column ----
            pcl_pattern = re.compile(
                rf"EMDR\s*{session_num}\s*PCL-5\s*Score",
                re.IGNORECASE
            )
            pcl_col = next((c for c in df_EMDR.columns if pcl_pattern.search(c)), None)
            if pcl_col is None:
                raise ValueError(f"PCL-5 Score column for EMDR {session_num} not found.")

            # ---- SUD Pre-Tx ----
            sud_pre_pattern = re.compile(
                rf"EMDR\s*{session_num}\s*SUD\s*Pre-Tx",
                re.IGNORECASE
            )
            sud_pre_col = next((c for c in df_EMDR.columns if sud_pre_pattern.search(c)), None)

            # ---- SUD Post-Tx ----
            sud_post_pattern = re.compile(
                rf"EMDR\s*{session_num}\s*SUD\s*Post-Tx",
                re.IGNORECASE
            )
            sud_post_col = next((c for c in df_EMDR.columns if sud_post_pattern.search(c)), None)

            # ---- Build long-format row ----
            long_rows.append({
                "ID": row["ID"],
                "PatientID": row["PatientID"],
                "EMDR_Session": session_num,
                "EMDR_Date": pd.to_datetime(row[date_col]) if pd.notna(row[date_col]) else None,
                "PCL5_Score": row[pcl_col],
                "SUD_PreTx": row[sud_pre_col] if sud_pre_col else None,
                "SUD_PostTx": row[sud_post_col] if sud_post_col else None,
            })

    return pd.DataFrame(long_rows)
