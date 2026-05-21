from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

import pandas as pd


SUPPORTED_CSV_EXTENSIONS = {".csv"}
SUPPORTED_EXCEL_EXTENSIONS = {".xlsx", ".xls"}
SUPPORTED_EXTENSIONS = SUPPORTED_CSV_EXTENSIONS | SUPPORTED_EXCEL_EXTENSIONS


def get_file_extension(filename: str) -> str:
    """Return normalized file extension."""
    return Path(filename).suffix.lower()


def get_file_type(filename: str) -> str:
    """Return supported file type based on extension."""
    extension = get_file_extension(filename)

    if extension in SUPPORTED_CSV_EXTENSIONS:
        return "csv"

    if extension in SUPPORTED_EXCEL_EXTENSIONS:
        return "excel"

    raise ValueError(
        f"Unsupported file extension: {extension}. "
        f"Supported extensions are: {', '.join(sorted(SUPPORTED_EXTENSIONS))}."
    )


def load_dataset(
    content: bytes,
    filename: str,
    sheet_name: str | int | None = None,
    skiprows: int = 0,
    separator: str = ",",
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """Load a dataset from CSV or Excel content."""
    file_type = get_file_type(filename)

    if file_type == "csv":
        return pd.read_csv(
            StringIO(content.decode(encoding)),
            sep=separator,
            skiprows=skiprows,
        )

    return pd.read_excel(
        BytesIO(content),
        sheet_name=sheet_name or 0,
        skiprows=skiprows,
    )


def to_json_safe(value: Any) -> Any:
    """Convert pandas/numpy values to JSON-safe values."""
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def preview_dataset(
    df: pd.DataFrame,
    filename: str,
    separator: str,
    encoding: str,
    skiprows: int,
    sheet_name: str | None = None,
) -> dict[str, Any]:
    """Generate a user-friendly dataset preview report."""
    row_count = int(df.shape[0])
    column_count = int(df.shape[1])
    total_cells = row_count * column_count
    missing_cells = int(df.isna().sum().sum())
    duplicated_rows = int(df.duplicated().sum())

    missing_rate = (
        round((missing_cells / total_cells) * 100, 2)
        if total_cells > 0
        else 0
    )

    columns_summary = []
    warnings = []
    suggestions = []
    recommended_actions = []

    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        column_missing_rate = (
            round((missing_count / row_count) * 100, 2)
            if row_count > 0
            else 0
        )
        unique_count = int(df[column].nunique(dropna=True))

        columns_summary.append(
            {
                "column": str(column),
                "type": str(df[column].dtype),
                "missing_values": missing_count,
                "missing_rate_percent": column_missing_rate,
                "unique_values": unique_count,
            }
        )

        if column_missing_rate > 30:
            warnings.append(
                f"Column '{column}' has a high missing value rate "
                f"({column_missing_rate}%)."
            )

        if unique_count == 1 and row_count > 0:
            warnings.append(
                f"Column '{column}' contains only one distinct value."
            )

    empty_columns = [str(column) for column in df.columns if df[column].isna().all()]

    if empty_columns:
        warnings.append(
            f"Fully empty columns detected: {', '.join(empty_columns)}."
        )

    if duplicated_rows > 0:
        warnings.append(f"{duplicated_rows} duplicate rows detected.")

    if column_count == 1 and filename.lower().endswith(".csv"):
        warnings.append(
            "Only one column was detected in this CSV file. "
            "The separator may be incorrect."
        )
        suggestions.append(
            "Try another separator, for example ';' instead of ','."
        )
        recommended_actions.append(
            {
                "label": "Change CSV separator",
                "parameter": "separator",
                "current_value": separator,
                "recommended_value": ";",
                "reason": (
                    "Only one column was detected. "
                    "The file probably uses a different separator."
                ),
            }
        )

    if any(str(column).startswith("Unnamed") for column in df.columns):
        warnings.append(
            "Some columns appear to have no explicit name."
        )
        suggestions.append(
            "Check whether the file contains extra header rows. "
            "Try skiprows=1 or skiprows=2 if needed."
        )
        recommended_actions.append(
            {
                "label": "Skip extra header rows",
                "parameter": "skiprows",
                "current_value": skiprows,
                "recommended_value": skiprows + 1,
                "reason": (
                    "Some columns appear to be unnamed or automatically generated."
                ),
            }
        )

    if row_count == 0:
        warnings.append("The file does not contain any usable data rows.")
        suggestions.append(
            "Check the selected Excel sheet, CSV separator or skiprows parameter."
        )

    quality_score = 100

    if missing_rate >= 5:
        quality_score -= 15
    if missing_rate >= 20:
        quality_score -= 20
    if duplicated_rows > 0:
        quality_score -= 10
    if column_count == 1 and filename.lower().endswith(".csv"):
        quality_score -= 30
    if empty_columns:
        quality_score -= 20

    quality_score = max(0, quality_score)

    if not warnings:
        global_status = "ok"
        global_message = "The dataset appears to be loaded correctly."
    else:
        global_status = "warning"
        global_message = (
            "The dataset was loaded, but some points require attention."
        )

    preview_table = [
        {
            str(column): to_json_safe(value)
            for column, value in row.items()
        }
        for row in df.head(10).to_dict(orient="records")
    ]

    user_report = [
        {
            "question": "Was the dataset loaded successfully?",
            "answer": global_message,
            "status": global_status,
            "suggestion": (
                None
                if global_status == "ok"
                else "Review the warnings and recommended actions below."
            ),
        },
        {
            "question": "How much data was detected?",
            "answer": f"{row_count} rows and {column_count} columns.",
            "status": "ok" if row_count > 0 and column_count > 0 else "error",
            "suggestion": None,
        },
        {
            "question": "What is the dataset quality score?",
            "answer": f"{quality_score}/100",
            "status": "ok" if quality_score >= 80 else "warning",
            "suggestion": (
                None
                if quality_score >= 80
                else "Fix priority warnings before running a full analysis."
            ),
        },
        {
            "question": "Are missing values a concern?",
            "answer": f"{missing_cells} missing cells ({missing_rate}%).",
            "status": "ok" if missing_rate < 5 else "warning",
            "suggestion": (
                None
                if missing_rate < 5
                else "Review columns containing the highest percentage of missing values."
            ),
        },
        {
            "question": "Are duplicate rows present?",
            "answer": f"{duplicated_rows} duplicate rows detected.",
            "status": "ok" if duplicated_rows == 0 else "warning",
            "suggestion": (
                None
                if duplicated_rows == 0
                else "Check whether these duplicates should be removed before analysis."
            ),
        },
    ]

    return {
        "status": global_status,
        "quality_score": quality_score,
        "user_report": user_report,
        "recommended_actions": recommended_actions,
        "suggestions": suggestions,
        "warnings": warnings,
        "read_parameters": {
            "filename": filename,
            "separator": separator,
            "encoding": encoding,
            "skiprows": skiprows,
            "sheet_name": sheet_name,
        },
        "dataset_info": {
            "rows": row_count,
            "columns": column_count,
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "missing_cells_rate_percent": missing_rate,
            "duplicated_rows": duplicated_rows,
        },
        "columns_summary": columns_summary,
        "preview_table": preview_table,
    }


def get_available_excel_sheets(content: bytes) -> list[str]:
    excel_file = pd.ExcelFile(BytesIO(content))
    return [str(sheet_name) for sheet_name in excel_file.sheet_names]