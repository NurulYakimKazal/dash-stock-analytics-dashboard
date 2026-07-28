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

                dmc.Select(
                    id="ticker-dropdown",
                    label="Ticker",
                    placeholder="Select a ticker",
                    data=[
                        {"label": ticker, "value": ticker}
                        for ticker in TICKERS
                    ],
                    value="AAPL",
                    searchable=False,
                    clearable=False,
                    nothingFoundMessage="No matching ticker",
                    maxDropdownHeight=200,
                ),

                dmc.Space(h=0),

                dmc.DatePickerInput(
                    id="date-range-picker",
                    label="Date Range",
                    type="range",
                    clearable=False,
                    closeOnChange=True,
                ),

                # Push everything below to the bottom
                dmc.Space(flex=1),

                dmc.Divider(),

                dmc.Center(
                    dmc.Anchor(
                        dmc.Group(
                            [
                                DashIconify(
                                    icon="mdi:github",
                                    width=20,
                                ),
                                dmc.Text(
                                    "View source on GitHub",
                                    size="sm",
                                ),
                            ],
                            gap="xs",
                        ),
                        href="https://github.com/NurulYakimKazal/dash-stock-analytics-dashboard",
                        target="_blank",
                        underline="never",
                    ),
                ),
            ],
            gap="sm",
            h="100%",
        ),
        p="lg",
    )

    return sidebar