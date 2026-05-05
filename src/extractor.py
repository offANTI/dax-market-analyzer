import yfinance as yf
import pandas as pd


def fetch_data(tickers):
    """Extrahiert historische Marktdaten von Yahoo Finance."""
    print(f"--- [EXTRAKTION] Starte Download für: {tickers}")
    data_list = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")
        hist['Ticker'] = ticker
        data_list.append(hist)

    full_data = pd.concat(data_list)
    print(f"--- [EXTRAKTION] {len(full_data)} Datensätze erfolgreich geladen.")
    return full_data