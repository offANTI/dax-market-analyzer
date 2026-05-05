def generate_recommendations(df_metrics):
    recommendations = []
    for _, row in df_metrics.iterrows():
        if row['Gesamtrendite'] > 0.2 and row['Risiko_Volatilitaet'] < 0.25:
            rec = "Stable Growth (Top Pick)"
        elif row['Risiko_Volatilitaet'] > 0.35:
            rec = "High Volatility (Speculative)"
        else:
            rec = "Neutral"
        recommendations.append(rec)
    df_metrics['Empfehlung'] = recommendations
    return df_metrics