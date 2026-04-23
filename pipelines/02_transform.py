from pathlib import Path
import pandas as pd

STAGING = Path("data/staging")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

cars = pd.read_parquet(STAGING / "cars.parquet")
cars.columns = cars.columns.str.strip()

costs = pd.read_parquet(STAGING / "costs.parquet")
revenue = pd.read_parquet(STAGING / "revenue.parquet")
branches = pd.read_parquet(STAGING / "branches.parquet")

for col in ["Revenue", "Total Cost", "Profit", "car_id"]:
    cars[col] = pd.to_numeric(cars[col], errors="coerce")

cars["profit_margin"] = cars["Profit"] / cars["Revenue"]
cars["cost_ratio"] = cars["Total Cost"] / cars["Revenue"]

util_col = None
for candidate in ["car_rented_length_percent", "Car rented length percent"]:
    if candidate in cars.columns:
        util_col = candidate
        break

rental_days_col = None
for candidate in ["rental_days", "Rental Days"]:
    if candidate in cars.columns:
        rental_days_col = candidate
        break

cars["utilization_proxy"] = pd.to_numeric(cars[util_col], errors="coerce") if util_col else pd.NA

agg_dict = {
    "car_count": ("car_id", "count"),
    "avg_revenue": ("Revenue", "mean"),
    "avg_cost": ("Total Cost", "mean"),
    "avg_profit": ("Profit", "mean"),
    "avg_profit_margin": ("profit_margin", "mean"),
    "avg_utilization": ("utilization_proxy", "mean"),
}

if rental_days_col:
    cars[rental_days_col] = pd.to_numeric(cars[rental_days_col], errors="coerce")
    agg_dict["avg_rental_days"] = (rental_days_col, "mean")

car_summary = (
    cars.groupby(["car_make", "car_model"], as_index=False)
    .agg(**agg_dict)
    .sort_values(["avg_profit", "avg_revenue"], ascending=False)
)

branch_col = "Branch Location" if "Branch Location" in cars.columns else "branch_location"
branch_summary = (
    cars.groupby(branch_col, as_index=False)
    .agg(
        fleet_size=("car_id", "count"),
        avg_revenue=("Revenue", "mean"),
        avg_profit=("Profit", "mean"),
        avg_cost=("Total Cost", "mean"),
    )
    .rename(columns={branch_col: "branch_location"})
)

car_summary.to_parquet(PROCESSED / "car_summary.parquet", index=False)
branch_summary.to_parquet(PROCESSED / "branch_summary.parquet", index=False)
car_summary.to_csv(PROCESSED / "car_summary.csv", index=False)
branch_summary.to_csv(PROCESSED / "branch_summary.csv", index=False)

print("Transform complete")
print("car_summary", car_summary.shape)
print("branch_summary", branch_summary.shape)