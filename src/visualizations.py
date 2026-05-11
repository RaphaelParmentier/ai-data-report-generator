from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_missing_values_chart(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Save a bar chart showing missing values by column."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    missing_values = df.isna().sum()
    missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

    if missing_values.empty:
        return output_path

    plt.figure(figsize=(8, 5))
    missing_values.plot(kind="bar")
    plt.title("Missing values by column")
    plt.xlabel("Column")
    plt.ylabel("Missing values")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path