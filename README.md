# Web Data Extractor & Exporter

A lightweight Python project for scraping web pages using CSS selectors and exporting extracted data to CSV, JSON, or Excel. Includes a CLI (Typer), a small FastAPI-based API/dashboard, and local persistence with SQLite (SQLModel). Docker and GitHub Actions CI are included for easy deployment and testing.

Key features
- Create and run scrape jobs (URL + CSS selector).
- Store scraped results in SQLite.
- Export results to CSV / JSON / XLSX.
- Run via CLI or HTTP API (FastAPI).
- Dockerfile and docker-compose for quick deployment.
- Unit tests with pytest, and CI workflow included.

Quick start (local, after full project files are added)
1. (Optional) Create & activate venv:
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the server (when app/ files exist):
   uvicorn app.main:app --reload

4. Open the dashboard / API:
   http://localhost:8000/

CLI examples
- One-off scrape and export:
  python -m app.cli run --url "https://example.com" --selector "h1" --export csv

API examples (curl)
- Create job:
  curl -X POST "http://localhost:8000/api/jobs" -H "Content-Type: application/json" -d '{"name":"example","url":"https://example.com","selector":"h1"}'

- Run job:
  curl -X POST "http://localhost:8000/api/scrape/1"

- Get latest scraped data:
  curl "http://localhost:8000/api/data/1"

- Export latest data:
  curl "http://localhost:8000/api/export/1?format=csv"

Notes
- This README is the project entry point for reviewers. To run the app you will need the app/ source files (can be added later via Upload files or by pushing from a computer).
- License: MIT. See LICENSE file (add when ready).
