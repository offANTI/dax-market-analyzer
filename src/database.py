from sqlalchemy import create_engine

def save_to_db(df, table_name, db_name="dax_market_data.db"):
    engine = create_engine(f"sqlite:///{db_name}")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Daten in Tabelle '{table_name}' gespeichert.")