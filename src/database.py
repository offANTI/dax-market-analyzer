import logging

import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


def save_to_db(
    df: pd.DataFrame,
    table_name: str,
    db_name: str = "dax_market_data.db",
) -> None:
    engine = create_engine(f"sqlite:///{db_name}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
    )

    logger.info("Saved %s rows to table '%s'.", len(df), table_name)
