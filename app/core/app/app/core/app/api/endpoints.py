from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from datetime import datetime
import os
import logging

from sqlmodel import select

from app.core.extractor import scrape_url
from app.core.db import get_session
from app.core.models import ScrapeJob, ScrapedData
from app.core import exporters

router = APIRouter()
logger = logging.getLogger("api")


@router.post("/jobs", response_model=ScrapeJob)
def create_job(job: ScrapeJob):
    """
    Create and persist a new scrape job configuration.
    """
    session = get_session()
    with session as s:
        s.add(job)
        s.commit()
        s.refresh(job)
    return job


@router.get("/jobs", response_model=List[ScrapeJob])
def list_jobs():
    """
    Return all configured scrape jobs.
    """
    session = get_session()
    with session as s:
        jobs = s.exec(select(ScrapeJob)).all()
    return jobs


def _run_and_store(job_id: int):
    """
    Internal worker: run scrape for job_id and store results.
    """
    session = get_session()
    with session as s:
        job = s.get(ScrapeJob, job_id)
        if not job:
            logger.warning("Job %s not found in _run_and_store", job_id)
            return
        try:
            results = scrape_url(job.url, job.selector)
            record = ScrapedData(job_id=job.id, data={"items": results})
            s.add(record)
            job.last_run = datetime.utcnow()
            job.last_status = "success"
            s.add(job)
            s.commit()
        except Exception as e:
            job.last_run = datetime.utcnow()
            job.last_status = f"failed: {str(e)}"
            s.add(job)
            s.commit()
            logger.exception("Failed to run job %s", job_id)


@router.post("/scrape/{job_id}")
def run_job_scrape(job_id: int, background: bool = True, background_tasks: BackgroundTasks = None):
    """
    Trigger scraping for a job. If background and background_tasks provided,
    the heavy work is scheduled as a BackgroundTask.
    """
    session = get_session()
    with session as s:
        job = s.get(ScrapeJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

    if background and background_tasks is not None:
        background_tasks.add_task(_run_and_store, job_id)
        return {"status": "started"}
    else:
        _run_and_store(job_id)
        return {"status": "completed"}


@router.get("/data/{job_id}")
def get_latest_data(job_id: int):
    """
    Return the most recent ScrapedData row for the given job.
    """
    session = get_session()
    with session as s:
        results = s.exec(
            select(ScrapedData).where(ScrapedData.job_id == job_id).order_by(ScrapedData.captured_at.desc())
        ).all()
        if not results:
            raise HTTPException(status_code=404, detail="No data found for job")
        return results[0]


@router.get("/export/{job_id}")
def export_job_data(job_id: int, format: str = "csv"):
    """
    Export the latest scraped data for job_id to CSV, JSON, or Excel.
    Returns the path of the created export file.
    """
    session = get_session()
    with session as s:
        record = s.exec(
            select(ScrapedData).where(ScrapedData.job_id == job_id).order_by(ScrapedData.captured_at.desc())
        ).first()
        if not record:
            raise HTTPException(status_code=404, detail="No data to export")
        items = record.data.get("items", [])

    os.makedirs("exports", exist_ok=True)
    ts = record.captured_at.strftime("%Y%m%d%H%M%S")

    if format == "csv":
        path = f"exports/job_{job_id}_{ts}.csv"
        exporters.export_to_csv(items, path)
    elif format == "json":
        path = f"exports/job_{job_id}_{ts}.json"
        exporters.export_to_json(items, path)
    elif format == "excel":
        path = f"exports/job_{job_id}_{ts}.xlsx"
        exporters.export_to_excel(items, path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

    return {"path": path}
