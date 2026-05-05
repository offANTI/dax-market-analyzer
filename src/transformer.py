import pandas as pd
import numpy as np


def process_data(df):
    """Transformiert Rohdaten in Risiko- und Rendite-Kennzahlen."""
    print("--- [TRANSFORMATION] Berechne Performance-Metriken...")

    analytics = df.groupby('Ticker')['Close'].agg([
        lambda x: ((x.iloc[-1] - x.iloc[0]) / x.iloc[0]),  # Gesamtrendite
        lambda x: x.pct_change().std() * np.sqrt(252)  # Volatilität
    ]).reset_index()


    analytics.columns = ['Ticker', 'Gesamtrendite', 'Risiko_Volatilitaet']

    print("--- [TRANSFORMATION] Analyse abgeschlossen.")
    return analytics