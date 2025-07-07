from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(
    title="Excel Processor API",
    description="API to process and query tables from an Excel file",
    version="1.0.0"
)

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_PATH = "Data/capbudg.xls"

def get_excel():
    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        return xls
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load Excel file.")

@app.get("/list_tables")
def list_tables():
    """
    List all table (sheet) names in the Excel file.
    """
    xls = get_excel()
    return {"tables": xls.sheet_names}

@app.get("/get_table_details")
def get_table_details(table_name: str = Query(..., description="Name of the table (sheet)")):
    """
    Return the row names (first column values) for the selected table.
    """
    xls = get_excel()
    if table_name not in xls.sheet_names:
        raise HTTPException(status_code=404, detail="Table not found.")
    df = xls.parse(table_name)
    if df.empty or df.shape[1] == 0:
        return {"table_name": table_name, "row_names": []}
    row_names = df.iloc[:, 0].dropna().astype(str).tolist()
    return {"table_name": table_name, "row_names": row_names}

@app.get("/row_sum")
def row_sum(
    table_name: str = Query(..., description="Name of the table (sheet)"),
    row_name: str = Query(..., description="Name of the row (first column value)")
):
    """
    Calculate and return the sum of all numerical data points in the specified row.
    Only numbers are summed; non-numeric values are ignored.
    """
    xls = get_excel()
    if table_name not in xls.sheet_names:
        raise HTTPException(status_code=404, detail="Table not found.")
    df = xls.parse(table_name)
    if df.empty or df.shape[1] < 2:
        raise HTTPException(status_code=404, detail="Table has insufficient columns.")
    # Find the row by matching the first column
    match = df[df.iloc[:, 0].astype(str) == row_name]
    if match.empty:
        raise HTTPException(status_code=404, detail="Row not found.")
    # Sum numeric values in the row (excluding the first column)
    row_data = match.iloc[0, 1:]
    numeric_values = pd.to_numeric(row_data, errors='coerce')
    total = float(numeric_values.sum())
    return {
        "table_name": table_name,
        "row_name": row_name,
        "sum": total
    }
