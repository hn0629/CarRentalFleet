# Car Rental Data Pipeline

A modular Python data engineering project that ingests raw rental data, transforms it into summary tables, validates the outputs, and generates reporting artifacts for analysis and presentation.

## Overview

This project demonstrates a simple ETL-style workflow for car rental data. It focuses on clean pipeline structure, reusable transformations, output validation, and reporting outputs that can support business decisions.

## Pipeline Stages

### 01_ingest.py
Reads the raw Excel workbook from `data/raw/` and writes normalized parquet files into `data/staging/`.

### transform.py
Cleans and standardizes the staged data, validates required fields, adds derived metrics, and builds summary tables for cars and branches.

### 03_validate.py
Checks the processed outputs in `data/processed/` for required values and basic data quality rules.

### 04_report.py
Creates final reporting tables and Plotly charts in `reports/` for the top cars and branches by profit and revenue.

## Project Structure

```text
Car Rental Project/
├── pipelines/
│   ├── __init__.py
│   ├── 01_ingest.py
│   ├── transform.py
│   ├── 03_validate.py
│   └── 04_report.py
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   ├── test_validate.py
│   └── test_end_to_end.py
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
├── reports/
├── schema/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .dockerignore
```

## Data Inputs

The ingest stage expects the raw Excel workbook in `data/raw/` and reads these sheets:

- `1_car_id_mapping`
- `2_car_costs`
- `3_car_revenue`
- `4_branch_location`

## Outputs

The pipeline writes the following artifacts:

### Staging
- `data/staging/cars.parquet`
- `data/staging/costs.parquet`
- `data/staging/revenue.parquet`
- `data/staging/branches.parquet`

### Processed
- `data/processed/car_summary.csv`
- `data/processed/car_summary.parquet`
- `data/processed/branch_summary.csv`
- `data/processed/branch_summary.parquet`

### Reports
- `reports/top_10_profit.csv`
- `reports/top_10_revenue.csv`
- `reports/top_10_branches.csv`
- `reports/top_10_profit.png`
- `reports/top_10_revenue.png`
- `reports/top_10_branches.png`

## How to Run

Run each stage in order:

```powershell
python pipelines/01_ingest.py
python pipelines/transform.py
python pipelines/03_validate.py
python pipelines/04_report.py
```

## How to Test

Run the automated tests with:

```powershell
python -m pytest -q
```

## Testing Strategy

This project includes:
- Unit tests for cleaning, validation, and aggregation logic.
- End-to-end tests for pipeline output creation.
- Fixture-based sample data for repeatable test cases.

## Key Business Questions

The outputs help answer questions such as:
- Which car makes and models produce the strongest profit?
- Which cars generate the strongest revenue?
- Which branches should be prioritized for future vehicle purchases?

## Future Improvements

Possible next steps:
- Add joins so all staged tables are used directly in transformation.
- Expand validation with stricter schema and range checks.
- Add a dashboard or notebook summary for the reporting outputs.
- Parameterize file paths for easier deployment.

## Author

Built as a data engineering portfolio project focused on modular pipeline design, testing, validation, and reporting outputs.