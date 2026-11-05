# Task 1 – Data Cleaning and Preprocessing

## Internship task objective
Clean a raw dataset containing missing values, duplicate records, inconsistent text/date formats, and inconsistent column names. Export a cleaned dataset and a short summary of the changes.

## Dataset
This project is designed for Kaggle's **Customer Personality Analysis** dataset.

Kaggle link: https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis

Download `marketing_campaign.csv` and place it here:

`dataset/marketing_campaign.csv`

The original Kaggle file is tab-separated, so the Python script reads it with `sep="\t"`.

## Tools
- Python
- Pandas
- VS Code

## Setup (Windows)
1. Install Python and VS Code.
2. Open this project folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

6. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Download the Kaggle dataset and put `marketing_campaign.csv` inside `dataset`.

## Run the project

```powershell
python data_cleaning.py
```

The script prints a before/after quality check and creates:

- `output/cleaned_dataset.csv`
- `output/cleaning_summary.txt`

## Cleaning steps performed
1. Inspect dataset shape, columns, data types, missing values, and duplicates.
2. Remove exact duplicate rows, retaining the first occurrence.
3. Trim unnecessary spaces from text values.
4. Standardize text capitalization.
5. Convert known numeric fields to numeric types.
6. Convert `Dt_Customer` to datetime when that column exists.
7. Fill numeric missing values with the median, excluding the identifier `ID`.
8. Fill categorical missing values with the mode.
9. Rename columns to lowercase with underscores.
10. Export the cleaned dataset and summary.

## Important notes
- Check the generated summary and output before submitting.
- Median/mode imputation is a basic strategy, not a universal rule. Explain why it is appropriate for each field.
- Invalid dates are converted to missing values. Review those rows if any are reported.
- Do not upload the Kaggle raw dataset to a public repository unless its licence permits redistribution. If unsure, upload the code and provide the Kaggle download link instead.

## Repository contents
- `data_cleaning.py` – complete cleaning script
- `dataset/` – place the downloaded dataset here
- `output/` – generated cleaned file and summary
- `requirements.txt` – Python dependency
- `README.md` – project documentation
