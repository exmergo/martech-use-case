from pathlib import Path

import duckdb


DB_PATH = Path("data/martech.duckdb")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))