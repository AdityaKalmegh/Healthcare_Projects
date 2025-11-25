import pandas as pd
import re

def transform_wet_procedures(df_WET):
    """
    Transform wide-format WET session data into long-format rows.
    Handles variable naming patterns such as:
    'WET 1: Date', 'WET 1 : PCL-5 Score', 'WET 1 SUD Pre-Tx', etc.
    """

    long_rows = []

    # Identify all unique WET session numbers dynamically
    session_numbers = sorted({
        int(re.findall(r'WET\s+(\d+)', col)[0])
        for col in df_WET.columns
        if re.search(r'WET\s+\d+', col)
    })

    for _, row in df_WET.iterrows():

        for session_num in session_numbers:

            # --- Date Column (consistent pattern) ---
            date_col = f"WET {session_num}: Date"

          # PCL-5 Score (extremely flexible matching)
pcl5_pattern = re.compile(
    rf"WET\s*{session_num}\s*:?\.?\s*PCL-5\s*Score",
    flags=re.IGNORECASE
)

pcl5_col = next((c for c in df_WET.columns if pcl5_pattern.search(c)), None)

if pcl5_col is None:
    print("DEBUG: Columns found:", list(df_WET.columns))
    raise ValueError(f"PCL-5 Score column missing for WET {session_num}")

            # --- SUD Pre-Tx ---
            pre_sud_pattern = re.compile(
                rf"WET {session_num}\s*SUD Pre-Tx",
                flags=re.IGNORECASE
            )
            pre_sud_col = next((c for c in df_WET.columns if pre_sud_pattern.fullmatch(c)), None)

            # --- SUD Post-Tx ---
            post_sud_pattern = re.compile(
                rf"WET {session_num}\s*SUD Post-Tx",
                flags=re.IGNORECASE
            )
            post_sud_col = next((c for c in df_WET.columns if post_sud_pattern.fullmatch(c)), None)

            # Build one row per session
            long_rows.append({
                "ID": row["ID"],
                "PatientID": row["PatientID"],
                "WET_Session": session_num,
                "WET_Date": pd.to_datetime(row[date_col]) if pd.notna(row[date_col]) else None,
                "PCL5_Score": row[pcl5_col],
                "SUD_PreTx": row[pre_sud_col] if pre_sud_col else None,
                "SUD_PostTx": row[post_sud_col] if post_sud_col else None,
            })

    return pd.DataFrame(long_rows)
