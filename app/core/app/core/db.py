import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# For SQLite set check_same_thread to False to allow usage from multiple threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    """
    Create database tables defined in SQLModel models.
    Call this at app startup (or before first use).
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """
    Return a new Session instance. Use it as a context manager:
        with get_session() as session:
            ...
    """
    return Session(engine)
