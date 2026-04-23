from pathlib import Path
import pandas as pd
import plotly.express as px

PROCESSED = Path("data/processed")
REPORTS = Path("reports")
REPORTS.mkdir(parents=True, exist_ok=True)

car_summary = pd.read_csv(PROCESSED / "car_summary.csv")
branch_summary = pd.read_csv(PROCESSED / "branch_summary.csv")

top_profit = (
    car_summary.sort_values("avg_profit", ascending=False)
    .head(10)
    .loc[:, ["car_make", "car_model", "avg_profit"]]
)

top_revenue = (
    car_summary.sort_values("avg_revenue", ascending=False)
    .head(10)
    .loc[:, ["car_make", "car_model", "avg_revenue"]]
)

top_branches = (
    branch_summary.sort_values("avg_profit", ascending=False)
    .head(10)
    .loc[:, ["branch_location", "avg_profit"]]
)

top_profit.to_csv(REPORTS / "top_10_profit.csv", index=False)
top_revenue.to_csv(REPORTS / "top_10_revenue.csv", index=False)
top_branches.to_csv(REPORTS / "top_10_branches.csv", index=False)

fig1 = px.bar(
    top_profit,
    x="avg_profit",
    y=top_profit["car_make"] + " - " + top_profit["car_model"],
    orientation="h",
    title="Top 10 Cars by Average Profit",
    labels={"avg_profit": "Average Profit", "y": "Car"},
)
fig1.update_layout(yaxis={"categoryorder": "total ascending"})
fig1.write_image(REPORTS / "top_10_profit.png")

fig2 = px.bar(
    top_revenue,
    x="avg_revenue",
    y=top_revenue["car_make"] + " - " + top_revenue["car_model"],
    orientation="h",
    title="Top 10 Cars by Average Revenue",
    labels={"avg_revenue": "Average Revenue", "y": "Car"},
)
fig2.update_layout(yaxis={"categoryorder": "total ascending"})
fig2.write_image(REPORTS / "top_10_revenue.png")

fig3 = px.bar(
    top_branches,
    x="avg_profit",
    y="branch_location",
    orientation="h",
    title="Top 10 Branches by Average Profit",
    labels={"avg_profit": "Average Profit", "branch_location": "Branch"},
)
fig3.update_layout(yaxis={"categoryorder": "total ascending"})
fig3.write_image(REPORTS / "top_10_branches.png")

print("Report complete")