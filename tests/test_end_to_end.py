from pathlib import Path
import pandas as pd

from pipelines.transform import main


def test_pipeline_writes_outputs(tmp_path):
    staging = tmp_path / "data" / "staging"
    processed = tmp_path / "data" / "processed"
    staging.mkdir(parents=True, exist_ok=True)

    cars = pd.DataFrame(
        {
            "car_make": ["Toyota", "Ford"],
            "car_model": ["Corolla", "Focus"],
            "Revenue": [1000, 1100],
            "Total Cost": [700, 650],
            "Profit": [300, 450],
            "car_id": [1, 2],
            "Branch Location": ["Boston, Massachusetts", "Dallas, Texas"],
            "car_rented_length_percent": [0.5, 0.8],
            "rental_days": [10, 9],
        }
    )

    for name in ["cars", "costs", "revenue", "branches"]:
        cars.to_parquet(staging / f"{name}.parquet", index=False)

    main(staging_dir=staging, processed_dir=processed)

    assert (processed / "car_summary.csv").exists()
    assert (processed / "branch_summary.csv").exists()
    assert (processed / "car_summary.parquet").exists()
    assert (processed / "branch_summary.parquet").exists()