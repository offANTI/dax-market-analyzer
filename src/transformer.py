import pandas as pd
import numpy as np

def process_data(df):
    print("--- [TRANSFORMATION] Berechne Finanz-Metriken...")


    performance = df.groupby('Ticker')['Close'].apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1)


    df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change()

    volatility = df.groupby('Ticker')['Daily_Return'].std() * np.sqrt(252)


    def calculate_max_drawdown(series):
        rolling_max = series.cummax()
        drawdown = (series - rolling_max) / rolling_max
        return drawdown.min()

    max_dd = df.groupby('Ticker')['Close'].apply(calculate_max_drawdown)


    metrics_df = pd.DataFrame({
        'Ticker': performance.index,
        'Gesamtrendite': performance.values,
        'Risiko_Volatilitaet': volatility.values,
        'Max_Drawdown': max_dd.values
    })


    metrics_df = metrics_df.reset_index(drop=True)

    return metrics_df