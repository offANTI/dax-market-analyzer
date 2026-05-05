import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandas as pd
import os


def create_visuals(db_path='dax_market_data.db'):
    print("--- [VISUALISIERUNG] Erstelle Analyse-Bericht...")


    if not os.path.exists(db_path):
        print(f" Fehler: Datenbank {db_path} nicht gefunden!")
        return

    conn = sqlite3.connect(db_path)

    query = "SELECT * FROM processed_analytics"
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Tabelle: {e}")
        return
    finally:
        conn.close()


    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))


    df = df.sort_values(by='Gesamtrendite', ascending=False)

    plot = sns.barplot(
        x='Ticker',
        y='Gesamtrendite',
        data=df,
        palette='viridis'
    )


    for p in plot.patches:
        plot.annotate(format(p.get_height(), '.2%'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center', va='center',
                      xytext=(0, 9),
                      textcoords='offset points')


    plt.title('DAX 40 Performance Analyse (2 Jahre)', fontsize=16, fontweight='bold')
    plt.xlabel('Unternehmen (Ticker)', fontsize=12)
    plt.ylabel('Gesamtrendite (Performance)', fontsize=12)


    plt.text(0.5, -0.15, 'Automatisch generiert von DAX-Market-Analyzer Pipeline',
             horizontalalignment='center', verticalalignment='center',
             transform=plt.gca().transAxes, color='gray', style='italic')

    plt.tight_layout()


    output_file = 'dax_analysis_report.png'
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f" [VISUALISIERUNG] Bericht erfolgreich unter '{output_file}' gespeichert.")


if __name__ == "__main__":
    create_visuals()