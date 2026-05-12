import argparse
import logging
import sys

from src.database import save_to_db
from src.extractor import fetch_data
from src.transformer import process_data
from src.visualizer import create_visuals

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

DAX_SAMPLE_TICKERS = ["SAP.DE", "SIE.DE", "ALV.DE", "BMW.DE", "DTE.DE", "AIR.DE"]


def run_pipeline(full_update: bool = True) -> None:
    logger.info("Starting DAX sample portfolio pipeline.")

    if full_update:
        raw_data = fetch_data(DAX_SAMPLE_TICKERS)
        save_to_db(raw_data, "raw_prices")

        analytics = process_data(raw_data)
        save_to_db(analytics, "processed_analytics")

    create_visuals()

    logger.info("Pipeline finished successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DAX Sample Portfolio Analyzer CLI"
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help="Run full ETL process.",
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Create report from existing database data.",
    )

    args = parser.parse_args()

    if args.update == args.report:
        parser.error("Choose exactly one option: --update or --report")

    run_pipeline(full_update=args.update)


if __name__ == "__main__":
    main()
