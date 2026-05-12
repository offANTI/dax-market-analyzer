import logging
import os
import sqlite3

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def create_visuals(db_path: str = "dax_market_data.db") -> None:
    logger.info("Creating visual analytics reports.")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    os.makedirs("reports", exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        metrics = pd.read_sql("SELECT * FROM processed_analytics", conn)

    if metrics.empty:
        raise ValueError("No analytics data found in processed_analytics table.")

    create_total_return_chart(metrics)
    create_volatility_chart(metrics)
    create_drawdown_chart(metrics)

    logger.info("Visual reports saved to reports/ directory.")


def create_total_return_chart(metrics: pd.DataFrame) -> None:
    data = metrics.sort_values("total_return", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(data["Ticker"], data["total_return"])
    plt.title("Total Return Comparison")
    plt.xlabel("Ticker")
    plt.ylabel("Total Return")

    for index, value in enumerate(data["total_return"]):
        plt.text(index, value, f"{value:.1%}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("reports/total_return.png", dpi=300)
    plt.close()


def create_volatility_chart(metrics: pd.DataFrame) -> None:
    data = metrics.sort_values("annualized_volatility", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(data["Ticker"], data["annualized_volatility"])
    plt.title("Annualized Volatility Analysis")
    plt.xlabel("Ticker")
    plt.ylabel("Annualized Volatility")

    for index, value in enumerate(data["annualized_volatility"]):
        plt.text(index, value, f"{value:.1%}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("reports/volatility.png", dpi=300)
    plt.close()


def create_drawdown_chart(metrics: pd.DataFrame) -> None:
    data = metrics.sort_values("max_drawdown")

    plt.figure(figsize=(10, 6))
    plt.bar(data["Ticker"], data["max_drawdown"])
    plt.title("Maximum Drawdown Analysis")
    plt.xlabel("Ticker")
    plt.ylabel("Max Drawdown")

    for index, value in enumerate(data["max_drawdown"]):
        plt.text(index, value, f"{value:.1%}", ha="center", va="top")

    plt.tight_layout()
    plt.savefig("reports/drawdown.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    create_visuals()
