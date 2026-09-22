from pathlib import Path

import dagster as dg

from martech.database import get_connection


CONTACTS_PATH = Path("data/raw/hubspot_contacts.csv")
DEALS_PATH = Path("data/raw/hubspot_deals.csv")
DEAL_CONTACTS_PATH = Path("data/raw/hubspot_deal_contacts.csv")


@dg.multi_asset(
    outs={
        "hubspot_contacts_raw": dg.AssetOut(
            group_name="ingestion",
            metadata={
                "layer": "raw",
                "source": "hubspot",
            },
        ),
        "hubspot_deals_raw": dg.AssetOut(
            group_name="ingestion",
            metadata={
                "layer": "raw",
                "source": "hubspot",
            },
        ),
        "hubspot_deal_contacts_raw": dg.AssetOut(
            group_name="ingestion",
            metadata={
                "layer": "raw",
                "source": "hubspot",
            },
        ),
    }
)
def hubspot_raw():
    """Load fake HubSpot CRM contacts, deals, and deal-contact associations into DuckDB."""

    con = get_connection()
    try:
        con.execute(
            """
            CREATE OR REPLACE TABLE raw_hubspot_contacts AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(CONTACTS_PATH)],
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE raw_hubspot_deals AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(DEALS_PATH)],
        )

        con.execute(
            """
            CREATE OR REPLACE TABLE raw_hubspot_deal_contacts AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(DEAL_CONTACTS_PATH)],
        )

        contacts_count = con.execute(
            "SELECT COUNT(*) FROM raw_hubspot_contacts"
        ).fetchone()[0]

        deals_count = con.execute(
            "SELECT COUNT(*) FROM raw_hubspot_deals"
        ).fetchone()[0]

        deal_contacts_count = con.execute(
            "SELECT COUNT(*) FROM raw_hubspot_deal_contacts"
        ).fetchone()[0]
    finally:
        con.close()

    yield dg.Output(
        None,
        output_name="hubspot_contacts_raw",
        metadata={
            "row_count": contacts_count,
            "table": "raw_hubspot_contacts",
        },
    )

    yield dg.Output(
        None,
        output_name="hubspot_deals_raw",
        metadata={
            "row_count": deals_count,
            "table": "raw_hubspot_deals",
        },
    )

    yield dg.Output(
        None,
        output_name="hubspot_deal_contacts_raw",
        metadata={
            "row_count": deal_contacts_count,
            "table": "raw_hubspot_deal_contacts",
        },
    )
