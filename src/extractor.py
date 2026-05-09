import yfinance as yf
import pandas as pd


def fetch_data(tickers):

    print(f"--- [EXTRAKTION] Starte Download für: {tickers}")
    data_list = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")
        hist['Ticker'] = ticker
        data_list.append(hist)

    full_data = pd.concat(data_list)
    full_data = full_data.reset_index()
    return full_data