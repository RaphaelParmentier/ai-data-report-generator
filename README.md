# AI Data Report Generator

AI-powered data profiling and report generation pipeline for structured datasets.

This project aims to automate the first layer of data analysis: loading a dataset, assessing its quality, generating descriptive insights, and producing a readable report that can be used by analysts, consultants, or business teams.

## Why this project?

Most data projects start with repetitive exploratory work:

- checking missing values
- identifying duplicated rows
- detecting suspicious columns
- summarizing numerical and categorical variables
- generating first-level business insights
- preparing a readable report for non-technical stakeholders

This repository explores how to turn that process into a reusable, explainable, and production-oriented workflow.

## Core objectives

- Build a clean Python data analysis pipeline
- Detect common data quality issues automatically
- Generate structured dataset profiles
- Produce human-readable analytical reports
- Prepare the project for future AI-assisted report generation

## Current status

MVP in progress.

The first version focuses on deterministic data profiling before adding LLM-based report generation.

## Planned features

- CSV loading and validation
- Missing value analysis
- Duplicate detection
- Numerical variable summaries
- Categorical variable summaries
- Automated report generation in Markdown
- Optional AI-generated executive summary
- Export to PDF
- Lightweight web interface

## Project structure

```txt
ai-data-report-generator/
├── data/
│   └── sample_customers.csv
├── notebooks/
│   └── exploration.ipynb
├── outputs/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_quality.py
│   ├── profiling.py
│   └── report_generator.py
├── .gitignore
├── README.md
└── requirements.txt