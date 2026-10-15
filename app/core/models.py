from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import JSON

class ScrapeJob(SQLModel, table=True):
    """
    Represents a configured scraping job.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    selector: str  # CSS selector used to extract items
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_run: Optional[datetime] = None
    last_status: Optional[str] = None  # e.g. "success" or "failed: <error>"

class ScrapedData(SQLModel, table=True):
    """
    Stores the result of a job run as JSON.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(index=True)
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    data: dict = Field(sa_column=JSON)  # JSON blob with extracted items
