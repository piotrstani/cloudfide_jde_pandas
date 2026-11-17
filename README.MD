## 🚀 Running the Project and Tests

### 1. Prerequisites
Make sure you have Python (version 3.9+) and the required packages (`pandas`, `pytest`) installed.

### 2. Environment Setup (optional in venv)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pandas pytest
```

### 3. Running the Data Pipeline
The script will process the `sales.csv` file and generate a revenue summary report in `revenue_by_region.csv`:
```bash
python pipeline.py
```

### 4. Running All Tests with a Single Command
You can run all tests using:
```bash
pytest -v
```

## 🔍 Analysis of Issues in `sales.csv` and How They Are Handled

| Data Issue | Impact / CSV Line Numbers | How It Is Handled in Code |
| :--- | :--- | :--- |
| **Technical rows (mid-file header and summary)** | Row **751** (repeated header) and row **1508** (`TOTAL`) | Filtered out during the creation of a new data copy (`clean_df`) using logical masks. |
| **Exact row duplicates** | Rows including **306-307**, **825-826**, **970-971**, **1245-1246**, **1411-1412| Duplicate records were filtered out using `~raw_df.duplicated()` (keeping the first occurrence). |
| **Missing unit prices (`Unit Price` is NaN)** | Rows **612**, **1104**, **1356**, **1484** | **Left for business decision.** The rows were filtered out to avoid distorting calculations. |
| **Negative quantities (`Quantity < 0`)** | Rows **423**, **517**, **782**, **1016**, **1295**, **1452** | **Left for business decision.** The rows were filtered out to avoid distorting calculations. |
| **Number formatting (spaces in quantities, commas in prices)** | Rows with thousands separators in `Quantity` (e.g., `1 762`) and decimal commas in `Unit Price` (e.g., `59,00`) | Cleaned on the fly by removing spaces, replacing commas with dots, and casting to numeric types. |