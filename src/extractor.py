import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


def fetch_data(tickers: list[str], period: str = "2y") -> pd.DataFrame:
    logger.info("Starting data extraction for tickers: %s", tickers)

    data_frames = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            logger.warning("No data returned for ticker: %s", ticker)
            continue

        history = history.reset_index()
        history["Ticker"] = ticker
        data_frames.append(history)

    if not data_frames:
        raise ValueError("No market data was extracted.")

    full_data = pd.concat(data_frames, ignore_index=True)

    return full_data
