import argparse
import random
from pathlib import Path

import pandas as pd


SCENARIOS = (
    "synthetic",
    "hubspot_second_association",
)

START_DATE = "2026-07-01"
END_DATE = "2026-08-31"
DATES = pd.date_range(START_DATE, END_DATE, freq="D")

GOOGLE_CAMPAIGNS = [
    {
        "campaign_id": "GOOG-001",
        "campaign_name": "Brand Search",
    },
    {
        "campaign_id": "GOOG-002",
        "campaign_name": "Demo Intent",
    },
    {
        "campaign_id": "GOOG-003",
        "campaign_name": "Data Platform",
    },
]

META_CAMPAIGNS = [
    {
        "campaign_id": "META-001",
        "campaign_name": "MarTech Awareness",
    },
    {
        "campaign_id": "META-002",
        "campaign_name": "Analytics Leaders",
    },
    {
        "campaign_id": "META-003",
        "campaign_name": "Revenue Attribution",
    },
]

ALL_CAMPAIGNS = GOOGLE_CAMPAIGNS + META_CAMPAIGNS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate deterministic synthetic MarTech source data."
    )
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS,
        default="synthetic",
        help="Synthetic data scenario to generate (default: synthetic).",
    )
    return parser.parse_args()


def main():
    scenario = parse_args().scenario
    random.seed(42)

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    google_ads = []

    for date in DATES:
        for campaign in GOOGLE_CAMPAIGNS:
            impressions = random.randint(1500, 7000)
            clicks = random.randint(100, min(700, impressions))
            spend = round(random.uniform(80, 450), 2)
            conversions = random.randint(3, 30)

            google_ads.append(
                {
                    "date": date.date(),
                    "campaign_id": campaign["campaign_id"],
                    "campaign_name": campaign["campaign_name"],
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend": spend,
                    "conversions": conversions,
                }
            )

    meta_ads = []

    for date in DATES:
        for campaign in META_CAMPAIGNS:
            impressions = random.randint(2000, 10000)
            clicks = random.randint(100, min(900, impressions))
            spend = round(random.uniform(100, 500), 2)
            conversions = random.randint(3, 35)

            meta_ads.append(
                {
                    "date": date.date(),
                    "campaign_id": campaign["campaign_id"],
                    "campaign_name": campaign["campaign_name"],
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend": spend,
                    "conversions": conversions,
                }
            )

    contacts = []
    deals = []
    deal_contacts = []

    contact_id = 1
    deal_id = 1

    for campaign in ALL_CAMPAIGNS:
        number_of_contacts = random.randint(45, 65)

        for _ in range(number_of_contacts):
            current_contact_id = f"CONTACT-{contact_id:04d}"
            created_at = pd.Timestamp(random.choice(DATES))

            lifecycle_stage = random.choices(
                [
                    "lead",
                    "marketing_qualified_lead",
                    "customer",
                ],
                weights=[0.55, 0.25, 0.20],
                k=1,
            )[0]

            contacts.append(
                {
                    "contact_id": current_contact_id,
                    "created_at": created_at.date(),
                    "source": (
                        "google_ads"
                        if campaign["campaign_id"].startswith("GOOG")
                        else "meta_ads"
                    ),
                    "campaign_id": campaign["campaign_id"],
                    "campaign_name": campaign["campaign_name"],
                    "lifecycle_stage": lifecycle_stage,
                }
            )

            # Customers receive a closed-won deal.
            if lifecycle_stage == "customer":
                current_deal_id = f"DEAL-{deal_id:04d}"
                closed_at = created_at + pd.Timedelta(
                    days=random.randint(3, 25)
                )

                deals.append(
                    {
                        "deal_id": current_deal_id,
                        "contact_id": current_contact_id,
                        "campaign_id": campaign["campaign_id"],
                        "deal_amount": round(
                            random.uniform(1500, 20000),
                            2,
                        ),
                        "deal_status": "closed_won",
                        "closed_at": closed_at.date(),
                    }
                )

                # Store the HubSpot deal-contact relationship explicitly so
                # downstream attribution uses the association table's grain.
                deal_contacts.append(
                    {
                        "deal_id": current_deal_id,
                        "contact_id": current_contact_id,
                    }
                )

                deal_id += 1

            contact_id += 1

    if scenario == "hubspot_second_association":
        target_deal = deals[0]
        second_contact = next(
            contact
            for contact in contacts
            if contact["contact_id"] != target_deal["contact_id"]
            and contact["campaign_id"] != target_deal["campaign_id"]
        )

        deal_contacts.append(
            {
                "deal_id": target_deal["deal_id"],
                "contact_id": second_contact["contact_id"],
            }
        )

    pd.DataFrame(google_ads).to_csv(
        raw_dir / "google_ads.csv",
        index=False,
    )
    pd.DataFrame(meta_ads).to_csv(
        raw_dir / "meta_ads.csv",
        index=False,
    )
    pd.DataFrame(contacts).to_csv(
        raw_dir / "hubspot_contacts.csv",
        index=False,
    )
    pd.DataFrame(deals).to_csv(
        raw_dir / "hubspot_deals.csv",
        index=False,
    )
    pd.DataFrame(deal_contacts).to_csv(
        raw_dir / "hubspot_deal_contacts.csv",
        index=False,
    )

    print("Synthetic MarTech data generated successfully.")
    print(f"Scenario: {scenario}")
    print(f"Google Ads rows: {len(google_ads)}")
    print(f"Meta Ads rows: {len(meta_ads)}")
    print(f"HubSpot contacts: {len(contacts)}")
    print(f"HubSpot deals: {len(deals)}")
    print(f"HubSpot deal-contact associations: {len(deal_contacts)}")
    print(f"Output directory: {raw_dir.resolve()}")


if __name__ == "__main__":
    main()
