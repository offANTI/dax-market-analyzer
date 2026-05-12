import argparse
import logging
import time

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
    start_time = time.time()

    logger.info("Starting DAX sample portfolio pipeline.")
    logger.info("Tracking %s tickers.", len(DAX_SAMPLE_TICKERS))

    if full_update:
        raw_data = fetch_data(DAX_SAMPLE_TICKERS)

        logger.info(
            "Extracted %s rows for %s tickers.",
            len(raw_data),
            raw_data["Ticker"].nunique(),
        )

        save_to_db(raw_data, "raw_prices")

        analytics = process_data(raw_data)

        logger.info("Generated %s analytics records.", len(analytics))

        save_to_db(analytics, "processed_analytics")

    create_visuals()

    execution_time = round(time.time() - start_time, 2)

    logger.info("Pipeline finished successfully in %s seconds.", execution_time)


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
