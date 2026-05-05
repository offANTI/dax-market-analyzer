from src.extractor import fetch_data
from src.transformer import process_data
from src.database import save_to_db
from src.visualizer import create_visuals


def run_pipeline():

    dax_tickers = ['SAP.DE', 'SIE.DE', 'ALV.DE', 'BMW.DE', 'DTE.DE', 'AIR.DE']


    raw_df = fetch_data(dax_tickers)
    save_to_db(raw_df, 'raw_prices')


    analyzed_df = process_data(raw_df)


    save_to_db(analyzed_df, 'processed_analytics')


    create_visuals()


if __name__ == "__main__":
    run_pipeline()