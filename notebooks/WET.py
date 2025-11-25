import pandas as pd
import re

def transform_wet_procedures(df_WET):
    """
    Transform wide-format WET session data into long-format rows.
    Robust to inconsistent naming (spaces, colons, Excel artifacts).
    """

    long_rows = []

    # ---- Identify all unique WET session numbers dynamically ----
    session_numbers = sorted({
        int(re.findall(r'WET\s*(\d+)', col)[0])
        for col in df_WET.columns
        if re.search(r'WET\s*\d+', col)
    })

    for _, row in df_WET.iterrows():

        for session_num in session_numbers:

            # --- Date column (predictable name) ---
            date_pattern = re.compile(rf"WET\s*{session_num}\s*:\s*Date", re.IGNORECASE)
            date_col = next((c for c in df_WET.columns if date_pattern.search(c)), None)

            if date_col is None:
                raise ValueError(f"Date column for WET {session_num} not found.")

            # --- PCL-5 Score column (VERY flexible) ---
            pcl5_pattern = re.compile(
                rf"WET\s*{session_num}\s*:?\s*PCL-5\s*Score",
                re.IGNORECASE
            )
            pcl5_col = next((c for c in df_WET.columns if pcl5_pattern.search(c)), None)

            if pcl5_col is None:
                print("\nDEBUG: Available columns:", list(df_WET.columns))
                raise ValueError(f"PCL-5 Score column for WET Session {session_num} not found.")

            # --- SUD Pre-Tx column ---
            sud_pre_pattern = re.compile(
                rf"WET\s*{session_num}\s*SUD\s*Pre-Tx",
                re.IGNORECASE
            )
            sud_pre_col = next((c for c in df_WET.columns if sud_pre_pattern.search(c)), None)

            # --- SUD Post-Tx column ---
            sud_post_pattern = re.compile(
                rf"WET\s*{session_num}\s*SUD\s*Post-Tx",
                re.IGNORECASE
            )
            sud_post_col = next((c for c in df_WET.columns if sud_post_pattern.search(c)), None)

            # ---- Build long-format row ----
            long_rows.append({
                "ID": row["ID"],
                "PatientID": row["PatientID"],
                "WET_Session": session_num,
                "WET_Date": pd.to_datetime(row[date_col]) if pd.notna(row[date_col]) else None,
                "PCL5_Score": row[pcl5_col],
                "SUD_PreTx": row[sud_pre_col] if sud_pre_col else None,
                "SUD_PostTx": row[sud_post_col] if sud_post_col else None,
            })

    return pd.DataFrame(long_rows)
