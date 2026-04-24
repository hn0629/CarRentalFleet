from pathlib import Path
import pandas as pd

CAR_SUMMARY = Path("data/processed/car_summary.csv")
BRANCH_SUMMARY = Path("data/processed/branch_summary.csv")

def test_processed_files_exist():
    assert CAR_SUMMARY.exists()
    assert BRANCH_SUMMARY.exists()

def test_car_summary_schema_and_quality():
    df = pd.read_csv(CAR_SUMMARY)
    expected = {"car_make", "car_model", "car_count", "avg_revenue", "avg_cost", "avg_profit", "avg_profit_margin"}
    assert expected.issubset(df.columns)
    assert df.notna().all().all()
    assert pd.api.types.is_numeric_dtype(df["avg_revenue"])
    assert pd.api.types.is_numeric_dtype(df["avg_profit"])
    assert df[["car_make", "car_model"]].duplicated().sum() == 0

def test_branch_summary_schema_and_quality():
    df = pd.read_csv(BRANCH_SUMMARY)
    expected = {"branch_location", "fleet_size", "avg_revenue", "avg_cost", "avg_profit"}
    assert expected.issubset(df.columns)
    assert df.notna().all().all()
    assert pd.api.types.is_numeric_dtype(df["fleet_size"])
    assert pd.api.types.is_numeric_dtype(df["avg_profit"])
    assert df["branch_location"].duplicated().sum() == 0