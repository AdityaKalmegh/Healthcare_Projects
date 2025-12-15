start_end_by_metric = (
    long_df
    .dropna(subset=["Date"])
    .groupby(["PatientID", "Therapy", "Metric"], as_index=False)
    .agg(
        StartDate=("Date", "min"),
        EndDate=("Date", "max")
    )
)
