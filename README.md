# Car Rental Project

This project ingests a rental car Excel workbook, transforms it into clean staging and summary tables, validates the outputs, and generates basic reports.

## Project structure

- `data/raw/` — source Excel file.
- `data/staging/` — cleaned Parquet extracts.
- `data/processed/` — grouped summary tables.
- `reports/` — CSV outputs and PNG charts.
- `pipelines/` — Python scripts for each pipeline step.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the pipeline

Run each step from the project root:

```bash
python pipelines/01_ingest.py
python pipelines/02_transform.py
python pipelines/03_validate.py
python pipelines/04_report.py
```

## Outputs

After a successful run, you should have:

- `data/staging/cars.parquet`
- `data/staging/costs.parquet`
- `data/staging/revenue.parquet`
- `data/staging/branches.parquet`
- `data/processed/car_summary.csv`
- `data/processed/car_summary.parquet`
- `data/processed/branch_summary.csv`
- `data/processed/branch_summary.parquet`
- `reports/top_10_profit.csv`
- `reports/top_10_revenue.csv`
- `reports/top_10_branches.csv`
- `reports/top_10_profit.png`
- `reports/top_10_revenue.png`
- `reports/top_10_branches.png`

## Notes

- The pipeline is designed to be run from the repository root.
- If you change any file paths, update the scripts accordingly.