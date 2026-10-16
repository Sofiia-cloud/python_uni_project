"""Connection helpers for the standalone Roomly SQLite database."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'data' / 'roomly.sqlite'


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Open the project database and return rows as named mappings."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    try:
        yield connection
    finally:
        connection.close()
