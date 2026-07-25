import dash
import pandas as pd
from dash import Input, Output, page_container, callback
import dash_mantine_components as dmc
from components.header import render_header
from components.sidebar import render_sidebar
from src.db.stock_database import fetch_stock_data
from modules.init_pipeline import init_db_and_sync
from src.etl.stock_incremental_etl import run_stock_etl
from src.db.stock_database import create_stock_table


app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [
            # ============================
            # HEADER
            # ============================
            render_header(),

            # ============================
            # SIDEBAR
            # ============================
            render_sidebar(),

            # ============================
            # MAIN CONTENT
            # ============================
            dmc.AppShellMain(
                page_container
            ),
        ],
        id="app-shell",
        # ============================
        # APP SHELL SETTINGS
        # ============================
        header={
            "height": 70,
        },

        navbar={
            "width": 275,
            "breakpoint": "sm",
            "collapsed": {
                "mobile": True,
                "desktop": False,
            },
        },

        padding="md",
    )
)


@callback(
    Output("app-shell", "navbar"),
    Input("navbar-burger", "opened"),
)
def toggle_sidebar(opened):

    return {
        "width": 275,
        "breakpoint": "sm",
        "collapsed": {
            "mobile": not opened,
        },
    }


@callback(
    Output("date-range-picker", "value"),
    Output("date-range-picker", "minDate"),
    Output("date-range-picker", "maxDate"),
    Input("ticker-dropdown", "value"),
)
def update_date_range(ticker):

    if ticker is None:
        return None, None, None

    stock_df = fetch_stock_data(ticker).copy()

    if stock_df.empty:
        return None, None, None

    stock_df["date"] = pd.to_datetime(stock_df["date"])

    min_date = stock_df["date"].min().date().isoformat()
    max_date = stock_df["date"].max().date().isoformat()

    return (
        [min_date, max_date],
        min_date,
        max_date,
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )