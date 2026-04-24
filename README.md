# Car Rental Data Pipeline

A modular Python data engineering project that ingests raw rental data, transforms it into useful summary tables, validates the outputs, and prepares final reporting artifacts for analysis.

## Overview

This project demonstrates a simple ETL-style workflow for car rental data. It focuses on clean pipeline structure, data validation, reusable transformations, and automated testing.

## Pipeline Stages

### 01_ingest.py
Loads raw source files and places them into a staging-ready format.

### transform.py
Cleans the data, standardizes columns, validates required fields, adds derived metrics, and builds summary tables.

### 03_validate.py
Checks output schemas, null values, and expected data types to confirm the processed data is ready for use.

### 04_report.py
Generates final reporting outputs and summary artifacts for review.

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

The pipeline expects these parquet files in `data/staging/`:

- `cars.parquet`
- `costs.parquet`
- `revenue.parquet`
- `branches.parquet`

## Outputs

The pipeline writes the following processed files to `data/processed/`:

- `car_summary.csv`
- `car_summary.parquet`
- `branch_summary.csv`
- `branch_summary.parquet`

## How to Run

Run the pipeline stages as needed:

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
- Unit tests for column standardization, validation, and aggregation.
- End-to-end tests for pipeline output creation.
- Fixture-based sample data for repeatable test cases.

## Key Business Questions

The outputs help answer questions such as:
- Which car makes and models produce the strongest profit?
- Which branches have the highest fleet activity?
- Where should the business focus future vehicle purchases or replacements?

## Future Improvements

Possible next steps:
- Use all raw input tables in joins and enrichment logic.
- Add stronger schema checks for source and output data.
- Expand reporting with charts or dashboard-ready tables.
- Add data quality thresholds for production-style validation.

## Author

Built as a data engineering portfolio project focused on modular pipeline design, testing, and reproducible analytics outputs.