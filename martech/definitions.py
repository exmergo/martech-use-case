import dagster as dg


all_assets = dg.load_assets_from_modules(
    [
        __import__(
            "martech.assets.google_ads",
            fromlist=["*"],
        ),
        __import__(
            "martech.assets.meta_ads",
            fromlist=["*"],
        ),
        __import__(
            "martech.assets.hubspot",
            fromlist=["*"],
        ),
    ]
)


defs = dg.Definitions(
    assets=all_assets,
)