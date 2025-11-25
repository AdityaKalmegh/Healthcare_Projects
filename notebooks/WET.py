import pandas as pd
import re

def transform_wet_sessions(df):
    long_rows = []

    for _, row in df.iterrows():

        # Identify unique WET session numbers (1, 2, …)
        wet_nums = sorted({
            int(re.findall(r'WET\s+(\d+)', col)[0])
            for col in df.columns
            if re.search(r'WET\s+\d+', col)
        })

        for n in wet_nums:

            # --- Identify Columns Dynamically ---

            # Date field: always "WET n: Date"
            date_col = next(
                (c for c in df.columns if re.fullmatch(rf"WET {n}\s*:?\s*Date", c)),
                None
            )

            # PCL-5 Score field
            pcl_col = next(
                (c for c in df.columns if re.fullmatch(rf"WET {n}\s*:?\s*PCL-5 Score", c)),
                None
            )

            # SUD Pre-Tx field
            sud_pre_col = next(
                (c for c in df.columns if re.fullmatch(rf"WET {n}\s*SUD Pre-Tx", c)),
                None
            )

            # SUD Post-Tx field
            sud_post_col = next(
                (c for c in df.columns if re.fullmatch(rf"WET {n}\s*SUD Post-Tx", c)),
                None
            )

            # --- Validate expected fields ---
            if date_col is None:
                raise ValueError(f"Date column for WET {n} not found.")

            if pcl_col is None:
                raise ValueError(f"PCL-5 Score column for WET {n} not found.")

            # --- Build the long row ---
            long_rows.append({
                "ID": row["ID"],
                "PatientID": row["PatientID"],
                "SessionNumber": n,
                "SessionDate": pd.to_datetime(row[date_col]),
                "PCL5_Score": row[pcl_col],
                "SUD_PreTx": row[sud_pre_col] if sud_pre_col else None,
                "SUD_PostTx": row[sud_post_col] if sud_post_col else None,
            })

    return pd.DataFrame(long_rows)
