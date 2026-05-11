from pathlib import Path

import pandas as pd

from src.data_quality import run_data_quality_checks
from src.logger import setup_logger
from src.report_generator import (
    generate_markdown_report,
    save_markdown_report,
)

logger = setup_logger()

DATA_PATH = Path(__file__).parent / "data" / "sample_customers.csv"

logger.info("Loading dataset")

df = pd.read_csv(DATA_PATH)

logger.info("Running data quality checks")

quality_report = run_data_quality_checks(df)

logger.info("Generating markdown report")

markdown_report = generate_markdown_report(quality_report)

output_path = save_markdown_report(
    markdown_report,
    "outputs/report.md",
)

logger.info(f"Report generated successfully: {output_path}")