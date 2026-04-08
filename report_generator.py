import sqlite3
import click
import os
import datetime
import typing
from typing import List, Dict, Optional, Tuple

DB_PATH = os.getenv("DEV_PRODUCTIVITY_DB", "dev_productivity.db")


def _get_connection() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A valid database connection object.

    Raises:
        sqlite3.Error: If the connection cannot be established.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def _ensure_db_schema() -> None:
    """
    Ensures the required 'sessions' table exists in the database.

    Creates the table with columns for task tracking, category, duration,
    and timestamps if it does not already exist.

    Raises:
        sqlite3.Error: If the table creation fails.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                category TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to create schema: {e}")
    finally:
        conn.close()


def _get_weekly_start_end_dates() -> Tuple[str, str]:
    """
    Calculates the start and end timestamps for the previous week.

    Returns:
        Tuple[str, str]: ISO format strings for the start and end dates.
    """
    now = datetime.datetime.now()
    last_week_monday = now - datetime.timedelta(days=now.weekday() + 7)
    next_week_monday = last_week_monday + datetime