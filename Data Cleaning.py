import pandas as pd
import numpy as np

df = pd.read_csv("cms_hospital_data.csv", dtype= {"facility_id" : "string"})

# # print(df.isna().sum())
# print(df.info())
# # print(df.shape)
# Unique_Hopsital_name = df["facility_name"].nunique()
# print(f"Unique Hospital Names: {Unique_Hopsital_name}")
# groupby = df.groupby("facility_name").size().nlargest(10)
# # print(df[df["facility_name"] == "MEMORIAL HOSPITAL"].duplicated().sum())

# memorial = df[df["facility_name"] == "MEMORIAL HOSPITAL"]
# print(memorial.duplicated(
#     subset=["facility_id", "measure_id", "start_date", "end_date"]
# ).sum())

# print(memorial.groupby("start_date").size())

# print(memorial.groupby("_condition").size())

# print(memorial[memorial["_condition"] == "Electronic Clinical Quality Measure"]["measure_name"].value_counts())

# print(memorial[memorial["_condition"] == "Electronic Clinical Quality Measure"]["measure_name"].value_counts().value_counts())

# print(memorial[memorial["_condition"] == "Electronic Clinical Quality Measure"].groupby(
#     ["measure_name", "start_date"]
# ).size())

# ecqm = memorial[memorial["_condition"] == "Electronic Clinical Quality Measure"]

# print(ecqm.nunique())

# print(memorial.groupby("facility_id")["facility_name"].first())

# print(memorial.groupby("facility_id").size().sort_values(ascending=False))

# print(memorial[memorial["facility_id"] == "451358"]["measure_name"].tolist())

# print(df[df["facility_id"] == "140185"]["measure_name"].tolist())

#print(df[df["_condition"] == "Emergency Department"]["measure_name"].value_counts())

ed_time = df[
    df["measure_name"].str.startswith(
        "Average (median) time all patients spent in the emergency department"
    )
]
ed_time["score_numeric"] = pd.to_numeric(ed_time["score"], errors="coerce")


# print(ed_time[ed_time["score_numeric"].isna()]["score"].value_counts(dropna=False))

# print(ed_time["score_numeric"].describe())
ed_kpi = ed_time.groupby("facility_id")["score_numeric"].median() # Hospital Median ED Time KPI
# print(ed_kpi.sort_values(ascending=True))

# print(ed_kpi.count())

# print(ed_kpi.describe())

q1 = ed_kpi.quantile(0.25)
q3 = ed_kpi.quantile(0.75)

iqr = q3 - q1

# print(q1)
# print(q3)
# print(iqr)

upper_threshold = q3 + 1.5 * iqr

# print(upper_threshold) #298.125

high_ed = ed_kpi[ed_kpi > upper_threshold]

# print(high_ed.sort_values(ascending=False))

high_ed_df = high_ed.reset_index()
# print(high_ed_df.head())

merge = df.merge(high_ed_df, on="facility_id", how="left", suffixes=("", "_high_ed"))

# print(merge[["facility_id", "facility_name", "score_numeric_high_ed"]].sort_values(by="score_numeric", ascending=False).tail(20))


flagged = merge[merge["score_numeric"].notna()][
    ["facility_id", "facility_name", "state", "score_numeric"]
].drop_duplicates("facility_id")

# print(flagged.sort_values("score_numeric", ascending=False).head(10)) # Hospitals with highest ED Times

# print(flagged["state"].value_counts()) # States with highest ED TImes

state_total = ed_time.groupby("state")["score_numeric"].count()

# print(state_total)

state_flagged = flagged["state"].value_counts()

# print(state_flagged)

state_summary = pd.DataFrame({
    "total_hospitals": state_total,
    "flagged_hospitals": state_flagged
})
state_summary["flagged_hospitals"] = state_summary["flagged_hospitals"].fillna(0)
state_summary_30 = state_summary[
    state_summary["total_hospitals"] >= 30
]
state_summary["flagged_pct"] = (
    state_summary["flagged_hospitals"] /
    state_summary["total_hospitals"] * 100
)

state_summary_30 = state_summary[state_summary["total_hospitals"] >= 30]
state_summary_30["flagged_pct"] = state_summary_30["flagged_pct"].round(2)

# print(state_summary_30.sort_values("flagged_pct", ascending=False))

# print(flagged.sort_values("score_numeric", ascending=False).to_string(index=False)) #Faciltiy with highest ED Times

# print(flagged["score_numeric"].describe())

#66 hospitals were identified as statistical anomaly candidates because their reported median ED time exceeded 298.125 minutes. 
# These hospitals had a median ED time of 322 minutes, compared with 154 minutes across all 4,052 hospitals with valid measurements.

percentage_increase = (flagged["score_numeric"].median() - ed_time["score_numeric"].median()) / ed_time["score_numeric"].median() * 100

# print(f"Percentage increase in median ED time for flagged hospitals: {percentage_increase:.2f}%")

# The median reported ED time among the 66 anomaly candidates was 109.09% higher than the overall hospital median (322 vs. 154 minutes).

ed_time["Anomaly_Flag"] = np.where(ed_time["score_numeric"] > upper_threshold, "Anomaly", "Normal")

ed_time["excess_minutes"] = np.where(
    ed_time["score_numeric"] > upper_threshold,
    ed_time["score_numeric"] - upper_threshold,
    0
)

# print(
#     ed_time[ed_time["Anomaly_Flag"] == "Anomaly"]
#     .sort_values("excess_minutes", ascending=False)
#     [["facility_id", "facility_name", "score_numeric", "excess_minutes"]]
#     .head(15)
# )

# print(
#     ed_time.loc[ed_time["Anomaly_Flag"] == "Anomaly", "excess_minutes"]
#     .describe()
# )

conditions = [
    (ed_time["excess_minutes"] > 0) & (ed_time["excess_minutes"] <= 15),
    (ed_time["excess_minutes"] > 15) & (ed_time["excess_minutes"] <= 30),
    (ed_time["excess_minutes"] > 30) & (ed_time["excess_minutes"] <= 60),
    (ed_time["excess_minutes"] > 60)
]

choices = ["Low", "Moderate", "High", "Severe"]

ed_time["severity_category"] = np.select(conditions, choices, default="Normal")

# print(ed_time["severity_category"].value_counts())

# print(ed_time[["excess_minutes", "severity_category"]]
#       .sort_values("excess_minutes", ascending=False)
#       .head(10))

# print(conditions[0].sum())
# print(conditions[1].sum())
# print(conditions[2].sum())
# print(conditions[3].sum())

print(ed_time.columns)

Anamoly_Report = ed_time[["facility_id","facility_name", "state", "score_numeric", "excess_minutes", "severity_category"]]

Anamoly_Report = Anamoly_Report[
    Anamoly_Report["severity_category"] != "Normal"
]

Anamoly_Report = Anamoly_Report.sort_values(
    by="excess_minutes",
    ascending=False
).reset_index(drop=True)

# print(Anamoly_Report.head(10))

priority_map = {
    "Severe": "Critical",
    "High": "High",
    "Moderate": "Medium",
    "Low": "Low"
}

Anamoly_Report["priority_level"] = (
    Anamoly_Report["severity_category"]
    .map(priority_map)
)

# print(Anamoly_Report.head(10))

# print(Anamoly_Report["priority_level"].value_counts())

action_map = {
    "Critical": "Immediate investigation of ED bottlenecks",
    "High": "Review staffing and workflow constraints",
    "Medium": "Monitor and investigate recurring delays",
    "Low": "Continue monitoring"
}

Anamoly_Report["recommended_action"] = (

    Anamoly_Report["priority_level"].map(action_map)
)

print(Anamoly_Report.head(10))

Anamoly_Report[
    ["severity_category", "priority_level", "recommended_action"]
].drop_duplicates()

action_map = {
    "Critical": "Prioritize for immediate operational review",
    "High": "Conduct detailed operational review",
    "Medium": "Monitor performance and investigate recurring delays",
    "Low": "Continue routine performance monitoring"
}

Anamoly_Report["recommended_action"] = (
    Anamoly_Report["priority_level"].map(action_map)
)

Anamoly_Report = Anamoly_Report[
    [
        "facility_id",
        "facility_name",
        "state",
        "score_numeric",
        "excess_minutes",
        "severity_category",
        "priority_level",
        "recommended_action"
    ]
]
print(Anamoly_Report.head(10))

Anamoly_Report.to_csv(
    "hospital_ed_anomaly_report.csv",
    index=False
)

