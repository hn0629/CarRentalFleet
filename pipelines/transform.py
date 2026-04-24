from pathlib import Path
import pandas as pd

DEFAULT_STAGING = Path("data/staging")
DEFAULT_PROCESSED = Path("data/processed")


def load_inputs(staging_dir=DEFAULT_STAGING):
    staging_dir = Path(staging_dir)
    cars = pd.read_parquet(staging_dir / "cars.parquet")
    costs = pd.read_parquet(staging_dir / "costs.parquet")
    revenue = pd.read_parquet(staging_dir / "revenue.parquet")
    branches = pd.read_parquet(staging_dir / "branches.parquet")
    return cars, costs, revenue, branches


def standardize_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def validate_input(df):
    required_cols = ["car_make", "car_model", "Revenue", "Total Cost", "Profit", "car_id"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    for col in ["Revenue", "Total Cost", "Profit", "car_id"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"{col} must be numeric")
        if df[col].isna().any():
            raise ValueError(f"Null values found in {col}")

    return df


def add_derived_columns(df):
    df = df.copy()
    df["profit_margin"] = df["Profit"] / df["Revenue"]
    df["cost_ratio"] = df["Total Cost"] / df["Revenue"]

    util_col = next(
        (c for c in ["car_rented_length_percent", "Car rented length percent", "Car rented length percent "] if c in df.columns),
        None,
    )
    if util_col:
        df["utilization_proxy"] = pd.to_numeric(df[util_col], errors="coerce")
    else:
        df["utilization_proxy"] = pd.NA

    rental_days_col = next((c for c in ["rental_days", "Rental Days"] if c in df.columns), None)
    if rental_days_col:
        df[rental_days_col] = pd.to_numeric(df[rental_days_col], errors="coerce")

    return df


def build_car_summary(df):
    agg = {
        "car_count": pd.NamedAgg(column="car_id", aggfunc="count"),
        "avg_revenue": pd.NamedAgg(column="Revenue", aggfunc="mean"),
        "avg_cost": pd.NamedAgg(column="Total Cost", aggfunc="mean"),
        "avg_profit": pd.NamedAgg(column="Profit", aggfunc="mean"),
        "avg_profit_margin": pd.NamedAgg(column="profit_margin", aggfunc="mean"),
        "avg_utilization": pd.NamedAgg(column="utilization_proxy", aggfunc="mean"),
    }

    rental_days_col = next((c for c in ["rental_days", "Rental Days"] if c in df.columns), None)
    if rental_days_col:
        agg["avg_rental_days"] = pd.NamedAgg(column=rental_days_col, aggfunc="mean")

    return (
        df.groupby(["car_make", "car_model"])
        .agg(**agg)
        .reset_index()
        .sort_values(["avg_profit", "avg_revenue"], ascending=False)
    )


def build_branch_summary(df):
    branch_col = "Branch Location" if "Branch Location" in df.columns else "branch_location"
    if branch_col not in df.columns:
        raise ValueError("Missing branch location column")

    return (
        df.groupby(branch_col, as_index=False)
        .agg(
            fleet_size=("car_id", "count"),
            avg_revenue=("Revenue", "mean"),
            avg_profit=("Profit", "mean"),
            avg_cost=("Total Cost", "mean"),
        )
        .rename(columns={branch_col: "branch_location"})
        .sort_values(["avg_profit", "avg_revenue"], ascending=False)
    )


def save_outputs(car_summary, branch_summary, processed_dir=DEFAULT_PROCESSED):
    processed_dir = Path(processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    car_summary.to_parquet(processed_dir / "car_summary.parquet", index=False)
    branch_summary.to_parquet(processed_dir / "branch_summary.parquet", index=False)
    car_summary.to_csv(processed_dir / "car_summary.csv", index=False)
    branch_summary.to_csv(processed_dir / "branch_summary.csv", index=False)


def main(staging_dir=DEFAULT_STAGING, processed_dir=DEFAULT_PROCESSED):
    cars, costs, revenue, branches = load_inputs(staging_dir)
    cars = standardize_columns(cars)
    cars = validate_input(cars)
    cars = add_derived_columns(cars)
    car_summary = build_car_summary(cars)
    branch_summary = build_branch_summary(cars)
    save_outputs(car_summary, branch_summary, processed_dir)
    print("Transform complete")
    print("car_summary", car_summary.shape)
    print("branch_summary", branch_summary.shape)


if __name__ == "__main__":
    main()