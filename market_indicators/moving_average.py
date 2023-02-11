import pandas as pd

from data_handler.db_handler import Ticker


def simple_moving_average(
        dataframe: pd.DataFrame | Ticker,
        rolling_size: int = 50,
        col_name='close'
) -> Ticker | pd.DataFrame:
    df = dataframe if not isinstance(dataframe, Ticker) else dataframe.df
    df["SMA"] = df[col_name].rolling(rolling_size).mean()
    return dataframe
