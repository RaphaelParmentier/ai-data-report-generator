# AI Data Quality Auditor

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript)
![Gemini](https://img.shields.io/badge/Gemini-AI-8E75FF?logo=google)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?logo=vercel)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render)

AI-assisted platform for auditing CSV and Excel datasets through deterministic quality checks, visual diagnostics and executive reporting workflows.

Built with a modern full-stack architecture using Next.js, FastAPI and Gemini AI.

---

## Overview

AI Data Quality Auditor is designed to help analysts, consultants and data teams quickly inspect raw datasets before analysis or reporting workflows.

The platform combines:

- deterministic data quality validation
- visual diagnostics
- AI-generated audit insights
- standalone HTML executive reports

The objective is to bridge the gap between:

- raw operational datasets
- data quality auditing
- business-readable reporting

---

## Core Features

### Dataset ingestion

- CSV support
- Excel support (`.xlsx`, `.xls`)
- Multi-sheet handling
- Configurable separators
- Configurable encoding
- Skip rows support

### Deterministic data audit

Automated checks include:

- Missing values detection
- Duplicate row detection
- Constant column detection
- Schema profiling
- Dataset scoring
- Memory usage analysis

### Visual diagnostics

Interactive frontend visualizations:

- Missing value charts
- Column type distribution
- Quality score indicators
- Issue and recommendation panels

### AI audit layer

Optional Gemini-powered interpretation layer:

- Executive summary generation
- Business impact analysis
- Priority action recommendations
- Technical audit observations

The AI layer is isolated from the deterministic engine to ensure:

- Transparency
- Reproducibility
- Controlled AI usage

### Executive reporting

Exportable standalone reports:

- JSON audit export
- Premium HTML audit report
- Embedded SVG charts
- Printable PDF-compatible layout

---

## Why this project matters

Real-world datasets are often:

- Inconsistent
- Poorly documented
- Duplicated
- Partially missing
- Operationally noisy

Most lightweight dashboard tools stop at visualization.

This project focuses on:

- Auditability
- Explainability
- Actionable diagnostics
- Executive-ready reporting

The hybrid deterministic + AI approach allows:

- Reproducible quality checks
- Human-readable interpretations
- Scalable reporting workflows

---

## AI Design Philosophy

The platform intentionally separates:

### Deterministic audit engine

Responsible for:

- Metrics
- Validation
- Reproducible diagnostics

### AI interpretation layer

Responsible for:

- Contextualization
- Prioritization
- Business-oriented insights

The AI model never computes metrics itself.

This architecture reduces:

- Hallucination risks
- Hidden logic
- Non-reproducible scoring

---

## Tech Stack

### Frontend

- Next.js 16
- TypeScript
- TailwindCSS
- Recharts
- Lucide React

### Backend

- FastAPI
- Pandas
- OpenPyXL
- Uvicorn

### AI

- Gemini 2.5 Flash Lite
- Structured JSON prompting
- Controlled response parsing

### Deployment

- Vercel (frontend)
- Render (backend)

---

## Architecture

```txt
frontend/
├── app/
├── components/
├── lib/
│   └── report/
│       ├── htmlReport.ts
│       ├── svgCharts.ts
│       ├── reportUtils.ts
│       └── reportTypes.ts

backend/
├── src/
│   ├── api.py
│   ├── ai_insights.py
│   ├── data_loader.py
│   └── data_quality.py
```

---

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Environment Variables

Backend `.env`

```env
GEMINI_API_KEY=your_api_key
```

---

## Production Deployment

### Frontend

Deploy on Vercel.

### Backend

Deploy on Render.

Required backend environment variable:

```env
GEMINI_API_KEY
```

---

## Current Capabilities

- Full-stack deployed application
- AI-assisted audit insights
- Interactive diagnostics
- Modular reporting engine
- SVG-based export visuals
- HTML executive reports

---

## Future Improvements

Potential next iterations:

- Authentication layer
- Report history
- PDF generation
- Dataset lineage tracking
- Anomaly detection
- Semantic schema inference
- Automated cleaning pipelines
- Collaborative audit workflows

---

## Author

Raphaël Parmentier

AI Consultant · Data Scientist · Bioinformatics & Biostatistics background

---

## License

MIT License