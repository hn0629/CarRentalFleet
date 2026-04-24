import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pipelines.transform import (
    standardize_columns,
    validate_input,
    add_derived_columns,
    build_car_summary,
    build_branch_summary,
)


@pytest.fixture
def sample_cars_df():
    return pd.DataFrame(
        {
            "car_make": ["Toyota", "Toyota", "Ford", "Ford"],
            "car_model": ["Corolla", "Corolla", "Focus", "Focus"],
            "Revenue": [1000, 1200, 900, 1100],
            "Total Cost": [700, 800, 600, 650],
            "Profit": [300, 400, 300, 450],
            "car_id": [1, 2, 3, 4],
            "Branch Location": [
                "Boston, Massachusetts",
                "Boston, Massachusetts",
                "Dallas, Texas",
                "Dallas, Texas",
            ],
            "car_rented_length_percent": [0.5, 0.6, 0.7, 0.8],
            "rental_days": [10, 12, 8, 9],
        }
    )


def test_standardize_columns(sample_cars_df):
    out = standardize_columns(sample_cars_df)
    assert "car_make" in out.columns
    assert "car_model" in out.columns
    assert " car_make " not in out.columns


def test_validate_input_passes(sample_cars_df):
    df = standardize_columns(sample_cars_df)
    out = validate_input(df)
    assert out["Revenue"].notna().all()
    assert out["Profit"].notna().all()
    assert pd.api.types.is_numeric_dtype(out["car_id"])


def test_validate_input_fails_on_missing_column(sample_cars_df):
    df = standardize_columns(sample_cars_df).drop(columns=["Profit"])
    with pytest.raises(ValueError, match="Missing columns"):
        validate_input(df)


def test_validate_input_rejects_nulls(sample_cars_df):
    df = standardize_columns(sample_cars_df)
    df.loc[0, "Revenue"] = None
    with pytest.raises(ValueError, match="Null values found"):
        validate_input(df)


def test_add_derived_columns(sample_cars_df):
    df = validate_input(standardize_columns(sample_cars_df))
    out = add_derived_columns(df)
    assert "profit_margin" in out.columns
    assert "cost_ratio" in out.columns
    assert "utilization_proxy" in out.columns
    assert out["profit_margin"].iloc[0] == 0.3


def test_build_car_summary(sample_cars_df):
    df = add_derived_columns(validate_input(standardize_columns(sample_cars_df)))
    out = build_car_summary(df)

    expected = pd.DataFrame(
        {
            "car_make": ["Ford", "Toyota"],
            "car_model": ["Focus", "Corolla"],
            "car_count": [2, 2],
            "avg_revenue": [1000.0, 1100.0],
            "avg_cost": [625.0, 750.0],
            "avg_profit": [375.0, 350.0],
            "avg_profit_margin": [0.3712121212121212, 0.31666666666666665],
            "avg_utilization": [0.75, 0.55],
            "avg_rental_days": [8.5, 11.0],
        }
    )

    assert_frame_equal(
        out.reset_index(drop=True)[expected.columns],
        expected,
        check_like=False,
    )


def test_build_branch_summary(sample_cars_df):
    df = add_derived_columns(validate_input(standardize_columns(sample_cars_df)))
    out = build_branch_summary(df)

    expected = pd.DataFrame(
        {
            "branch_location": ["Dallas, Texas", "Boston, Massachusetts"],
            "fleet_size": [2, 2],
            "avg_revenue": [1000.0, 1100.0],
            "avg_profit": [375.0, 350.0],
            "avg_cost": [625.0, 750.0],
        }
    )

    assert_frame_equal(
        out.reset_index(drop=True)[expected.columns],
        expected,
        check_like=False,
    )