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

    try:
        
        df_raw = pd.read_sql("SELECT Date, Ticker, Close FROM rohdaten_preise", conn)
        df_pivot = df_raw.pivot(index='Date', columns='Ticker', values='Close')
        corr_matrix = df_pivot.ffill().corr()

       
        df_perf = pd.read_sql("SELECT * FROM processed_analytics", conn)
        df_perf = df_perf.sort_values(by='Gesamtrendite', ascending=False)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 18))
        sns.set_theme(style="whitegrid")

     
        plot = sns.barplot(x='Ticker', y='Gesamtrendite', data=df_perf, palette='viridis', ax=ax1)
        ax1.set_title('DAX 40 Performance Analyse (2 Jahre)', fontsize=16, fontweight='bold')
        
      
        for p in plot.patches:
            ax1.annotate(format(p.get_height(), '.2%'),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 9), textcoords='offset points')

       
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax2)
        ax2.set_title('Korrelations-Matrix: Aktien vs. Gas (TTF)', fontsize=14, fontweight='bold')

       
        plt.text(0.5, -0.05, 'Automatisch generiert von DAX-Market-Analyzer Pipeline',
                 horizontalalignment='center', transform=ax2.transAxes, color='gray', style='italic')

        plt.tight_layout()
        
        output_file = 'dax_analysis_report.png'
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f" [VISUALISIERUNG] Bericht успешно сохранен как '{output_file}'.")

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_visuals()
