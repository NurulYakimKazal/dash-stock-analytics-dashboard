from dash.exceptions import PreventUpdate
import pandas as pd
from src.db.company_database import fetch_company_data
from src.db.stock_database import fetch_stock_data


def prepare_callback_data(ticker, date_range):

    if ticker is None:
        raise PreventUpdate

    if (
        date_range is None
        or len(date_range) != 2
        or date_range[0] is None
        or date_range[1] is None
    ):
        raise PreventUpdate

    start_date, end_date = date_range

    company_dataframe = fetch_company_data(ticker).copy()
    stock_dataframe = fetch_stock_data(ticker).copy()

    stock_dataframe["date"] = pd.to_datetime(stock_dataframe["date"])

    stock_dataframe = stock_dataframe[
        stock_dataframe["date"].between(
            pd.Timestamp(start_date),
            pd.Timestamp(end_date),
        )
    ]

    return company_dataframe, stock_dataframe