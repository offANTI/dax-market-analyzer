import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def create_visuals():
    """Erstellt ein professionelles Risiko-Rendite-Diagramm."""
    engine = create_engine('sqlite:///dax_market_data.db')
    df = pd.read_sql('processed_analytics', engine)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # Scatterplot Erstellung
    sns.scatterplot(
        data=df,
        x='Risiko_Volatilitaet',
        y='Gesamtrendite',
        hue='Ticker',
        size='Gesamtrendite',
        sizes=(100, 400),
        palette='viridis',
        legend=False
    )

   
    for i in range(len(df)):
        plt.text(df.Risiko_Volatilitaet[i] + 0.0002, df.Gesamtrendite[i], df.Ticker[i],
                 fontsize=11, weight='bold')

    # Deutsche Achsenbeschriftung
    plt.title('DAX 40: Risiko-Rendite-Profil (2 Jahre)', fontsize=16, weight='bold')
    plt.xlabel('Risiko (Annualisierte Volatilität)', fontsize=12)
    plt.ylabel('Gesamtrendite (Performance)', fontsize=12)

    plt.tight_layout()
    plt.savefig('dax_analysis_report.png', dpi=300)
    print("--- [ANALYSE] Visueller Bericht 'dax_analysis_report.png' wurde erstellt.")