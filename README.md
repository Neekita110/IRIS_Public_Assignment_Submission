## Project Structure

```
IRIS_Public_Assignment/
│
├── Data/
│   └── capbudg.xls
├── main.py
├── README.md
└── IRIS_Postman_Collection.json
```

## main.py

## README.md

# IRIS Public Assignment – FastAPI Excel Processor

## Overview

This project implements a FastAPI application that reads and processes an Excel file (`Data/capbudg.xls`) and exposes endpoints for:

- Listing all tables (sheet names)
- Listing row names of a table
- Summing all numeric values in a specified row

## How to Run

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pandas openpyxl xlrd
   ```

2. **Start the API server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 9090
   ```

3. **API Documentation:**  
   Visit `http://localhost:9090/docs` for interactive Swagger UI.

## Endpoints

| Endpoint            | Method | Description                                                |
|---------------------|--------|------------------------------------------------------------|
| /list_tables        | GET    | Lists all tables (sheet names) in the Excel file           |
| /get_table_details  | GET    | Lists row names for a given table                          |
| /row_sum            | GET    | Returns the sum of numeric values in a specified row       |

### Example Usage

- **List Tables:**  
  `GET http://localhost:9090/list_tables`

- **Get Table Details:**  
  `GET http://localhost:9090/get_table_details?table_name=Initial%20Investment`

- **Row Sum:**  
  `GET http://localhost:9090/row_sum?table_name=Initial%20Investment&row_name=Tax%20Credit%20(if%20any%20)=`

## Notes

- Only numeric values are summed; units like `%` are ignored.
- Errors are returned for missing tables/rows or malformed requests.

## Potential Improvements

- Support for `.xlsx`, `.csv`, and Google Sheets.
- File upload endpoint for dynamic Excel processing.
- Advanced data operations (filter, aggregate, export).
- Simple web UI for non-technical users.
- Authentication for production use.
- Caching for large files.

## Missed Edge Cases

- Empty Excel files: returns an error.
- Tables with no numeric data: returns `0`.
- Merged cells or irregular structures: may yield unpredictable results.
- Special characters: handled, but malformed files may cause issues.

## Postman Collection

A sample Postman collection (`IRIS_Postman_Collection.json`) is included with all endpoints and example requests.

## Submission Checklist

- [x] FastAPI application code
- [x] README.md with instructions and insights
- [x] Postman collection for endpoint testing
- [x] Public repository structure
