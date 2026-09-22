from pathlib import Path

import dagster as dg

from martech.database import get_connection


GOOGLE_ADS_PATH = Path("data/raw/google_ads.csv")


@dg.asset(
    group_name="ingestion",
    metadata={
        "layer": "raw",
        "source": "google_ads",
    },
)
def google_ads_raw() -> dg.MaterializeResult:
    """Load fake Google Ads campaign data into DuckDB."""

    con = get_connection()
    try:
        con.execute(
            """
            CREATE OR REPLACE TABLE raw_google_ads AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(GOOGLE_ADS_PATH)],
        )

        row_count = con.execute(
            "SELECT COUNT(*) FROM raw_google_ads"
        ).fetchone()[0]
    finally:
        con.close()

    return dg.MaterializeResult(
        metadata={
            "row_count": row_count,
            "table": "raw_google_ads",
        }
    )
