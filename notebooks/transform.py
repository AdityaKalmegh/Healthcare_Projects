import pandas as pd
import re

def transform_therapy_data(df, patient_id_col="PatientID"):
    """
    Universal transformation for converting wide therapy session data 
    into long format.

    Expected wide format column examples:
        'PE 1 Date', 'PE 1 PCL-5 Score', 'PE 1 BDI-2 Score'
        'IGT 2 Date', 'IGT 2 Score'
        'EMDR 1 SUD Pre-Tx', etc.

    Returns a long-format dataframe with columns:
        PatientID, Therapy, Session, Metric, Value, Date
    """

    id_cols = [patient_id_col]
    value_rows = []

    for _, row in df.iterrows():
        patient_id = row[patient_id_col]

        for col in df.columns:
            if col == patient_id_col:
                continue

            # Regex to extract therapy, session, and metric
            match = re.match(r'([A-Za-z]+)\s+(\d+)\s+(.*)', col)
            if not match:
                continue

            therapy = match.group(1)                 # e.g., PE, EMDR, IGT
            session = int(match.group(2))            # e.g., 1, 2, 3
            metric = match.group(3).strip()          # e.g., Date, PCL-5 Score, Score

            value = row[col]

            # Skip empty cells
            if pd.isna(value):
                continue

            # Handle date separately
            if "date" in metric.lower():
                value_date = pd.to_datetime(value, errors="ignore")
                metric_name = "Date"
                metric_value = value_date
            else:
                metric_name = metric
                metric_value = value
                # retrieve session date for this same session, if present
                date_col = f"{therapy} {session} Date"
                date_value = row.get(date_col, None)
                value_date = pd.to_datetime(date_value, errors="ignore") if date_value else None
            
            value_rows.append({
                "PatientID": patient_id,
                "Therapy": therapy,
                "Session": session,
                "Metric": metric_name,
                "Value": metric_value,
                "Date": value_date
            })

    long_df = pd.DataFrame(value_rows)

    # Sort for readability
    long_df = long_df.sort_values(by=["PatientID", "Therapy", "Session", "Metric"])

    return long_df
