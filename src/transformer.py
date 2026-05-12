import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"Date", "Ticker", "Close"}
TRADING_DAYS_PER_YEAR = 252
MIN_OBSERVATIONS_PER_TICKER = 30


def validate_input_data(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df["Close"].isna().any():
        raise ValueError("Column 'Close' contains missing values.")

    if (df["Close"] <= 0).any():
        raise ValueError("Column 'Close' contains zero or negative prices.")


def calculate_max_drawdown(prices: pd.Series) -> float:
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    return float(drawdown.min())


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Calculating financial metrics.")

    validate_input_data(df)

    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="raise")
    data = data.sort_values(["Ticker", "Date"])

    ticker_counts = data.groupby("Ticker")["Close"].count()
    invalid_tickers = ticker_counts[ticker_counts < MIN_OBSERVATIONS_PER_TICKER]

    if not invalid_tickers.empty:
        raise ValueError(
            f"Not enough observations for tickers: {invalid_tickers.to_dict()}"
        )

    data["daily_return"] = data.groupby("Ticker")["Close"].pct_change()

    metrics = (
        data.groupby("Ticker")
        .agg(
            start_price=("Close", "first"),
            end_price=("Close", "last"),
            avg_daily_return=("daily_return", "mean"),
            daily_volatility=("daily_return", "std"),
            observations=("Close", "count"),
        )
        .reset_index()
    )

    metrics["total_return"] = metrics["end_price"] / metrics["start_price"] - 1

    metrics["annualized_volatility"] = (
        metrics["daily_volatility"] * np.sqrt(TRADING_DAYS_PER_YEAR)
    )

    max_drawdowns = (
        data.groupby("Ticker")["Close"]
        .apply(calculate_max_drawdown)
        .reset_index(name="max_drawdown")
    )

    metrics = metrics.merge(max_drawdowns, on="Ticker", how="left")

    return metrics[
        [
            "Ticker",
            "total_return",
            "annualized_volatility",
            "max_drawdown",
            "observations",
        ]
    ]
