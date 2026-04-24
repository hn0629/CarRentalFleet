# Car Rental Data Pipeline

A Python data pipeline that cleans rental fleet data, builds summary tables, and helps identify the most profitable car models and branch locations for purchase decisions.

## Overview

This project processes raw car rental data into curated summary outputs for analysis and reporting. It includes data validation, derived metrics, aggregation logic, and automated tests.

## What it does

- Loads raw parquet files from `data/staging/`.
- Standardizes column names.
- Validates required fields and numeric columns.
- Creates derived metrics such as profit margin and cost ratio.
- Builds summary tables by car model and branch location.
- Saves processed outputs as CSV and Parquet files.

## Project Structure

```text
Car Rental Project/
├── pipelines/
│   └── transform.py
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   └── test_end_to_end.py
├── data/
│   ├── staging/
│   └── processed/
└── README.md
```

## Data Inputs

Place these files in `data/staging/` before running the pipeline:

- `cars.parquet`
- `costs.parquet`
- `revenue.parquet`
- `branches.parquet`

## Outputs

The pipeline writes these files to `data/processed/`:

- `car_summary.csv`
- `car_summary.parquet`
- `branch_summary.csv`
- `branch_summary.parquet`

## Run the Pipeline

```powershell
python pipelines/transform.py
```

## Run Tests

```powershell
python -m pytest -q
```

## Testing Strategy

The project uses:
- Unit tests for cleaning, validation, and aggregation functions.
- Fixture-based sample data for repeatable test cases.
- An end-to-end test that verifies the pipeline writes output files correctly.

## Key Insights

The outputs help answer questions like:
- Which car makes and models generate the strongest profit?
- Which branches have the highest fleet activity?
- Where should the business focus future purchases or replacements?

## Future Improvements

Possible next steps:
- Join and use the additional input tables more fully.
- Add more schema checks for incoming data.
- Add tests that verify output contents, not just file creation.
- Build a dashboard from the processed summaries.

## Author

Built as a data engineering and analytics portfolio project focused on clean transformation logic, testing, and reproducible outputs.