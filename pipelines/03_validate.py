from pathlib import Path
import pandas as pd

PROCESSED = Path("data/processed")

car_summary = pd.read_csv(PROCESSED / "car_summary.csv")
branch_summary = pd.read_csv(PROCESSED / "branch_summary.csv")

assert not car_summary.empty
assert not branch_summary.empty
assert car_summary["avg_profit"].notna().all()
assert branch_summary["avg_revenue"].notna().all()

print("Validation passed")
print("car_summary rows:", len(car_summary))
print("branch_summary rows:", len(branch_summary))