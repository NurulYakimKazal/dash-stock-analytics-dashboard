import dash_mantine_components as dmc
from dash_iconify import DashIconify
from utils.config import TICKERS


# ============================
# SIDEBAR
# ============================
def render_sidebar():
    sidebar = dmc.AppShellNavbar(
        dmc.Stack(
            [

                dmc.NavLink(
                    label="Stock Explorer",
                    href="/",
                    leftSection=DashIconify(icon="mdi:chart-line"),
                ),

                dmc.NavLink(
                    label="Analytics",
                    href="/analytics",
                    leftSection=DashIconify(icon="mdi:chart-box"),
                ),

                dmc.NavLink(
                    label="Report",
                    href="/report",
                    leftSection=DashIconify(icon="mdi:file-chart"),
                ),

                dmc.Divider(),

                dmc.Title(
                    "Ticker and Date Range Filter",
                    order=5,
                ),

                # Stock selector
                dmc.Select(
                    id="ticker-dropdown",
                    label="Ticker",
                    placeholder="Select a ticker",
                    data=[{"label": ticker, "value": ticker} for ticker in TICKERS],
                    value="AAPL",
                    searchable=True,
                    clearable=False,
                    nothingFoundMessage="No matching ticker",
                    maxDropdownHeight=200,
                ),

                dmc.Space(h=0),

                dmc.DatePickerInput(
                    label="Date Range",
                    type="range",
                    clearable=False,
                    closeOnChange=True,
                    id="date-range-picker",
                )

            ],

            gap="sm",
        ),


        p="lg",

    )

    return sidebar