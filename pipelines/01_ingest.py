from pathlib import Path
import pandas as pd

RAW = Path("data/raw/Rental_car_fleet.xlsx")
STAGING = Path("data/staging")
STAGING.mkdir(parents=True, exist_ok=True)

xl = pd.read_excel(RAW, sheet_name=None)

cars = xl["1_car_id_mapping"][[
    "car_id", "car_model", "car_make", "car_model_year",
    "Car Cost Monthly", "Car Insurance", "Revenue", "Total Cost",
    "Profit", "Branch Id", "Branch Location", "Car rented length percent ",
    "Driver Gender", "Accident Number", "Airport Location", "Rental Days"
]].copy()

cars = cars.rename(columns={
    "Car Cost Monthly": "car_cost_monthly",
    "Car Insurance": "car_insurance",
    "Branch Id": "branch_id",
    "Branch Location": "branch_location",
    "Car rented length percent ": "car_rented_length_percent",
    "Driver Gender": "driver_gender",
    "Accident Number": "accident_number",
    "Airport Location": "airport_location",
    "Rental Days": "rental_days",
})

text_cols = ["car_model", "car_make", "branch_location", "driver_gender", "airport_location"]
for col in text_cols:
    cars[col] = cars[col].astype(str)

cars["car_id"] = pd.to_numeric(cars["car_id"], errors="coerce")
cars["car_model_year"] = pd.to_numeric(cars["car_model_year"], errors="coerce")

xl["2_car_costs"].to_parquet(STAGING / "costs.parquet", index=False)
xl["3_car_revenue"].to_parquet(STAGING / "revenue.parquet", index=False)
xl["4_branch_location"].to_parquet(STAGING / "branches.parquet", index=False)
cars.to_parquet(STAGING / "cars.parquet", index=False)

print("Ingest complete")
print("cars", cars.shape)