import dash
from dash import Input, Output, dcc, callback
import dash_mantine_components as dmc

from components.page_title import render_page_title
from components.company_details import render_company_details
from components.kpis import render_kpis
from components.one_plot_container import render_one_plot_container
from components.historical_price_grid import render_historical_price_grid
from components.footer import render_footer
from modules.callback_data_processing import prepare_callback_data
from modules.company_data import (
    prepare_company_data,
    prepare_company_kpi_cards
)
from modules.historical_price_chart import render_historical_price


dash.register_page(
    __name__,
    path="/",
)


layout = dcc.Loading(
    children=dmc.Container(
        [
            render_page_title("Stock Explorer", "mdi:chart-line"),

            dmc.Space(h="xl"),

            # Company Details
            dmc.Stack(
                id="company-details-container-pg1",
                gap=2
            ),

            dmc.Space(h="xl"),

            # KPIs
            dmc.SimpleGrid(
                id="company-kpis",
                cols={"base": 2, "md": 4},
                spacing=5,
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Paper(
                id="historical-price",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),

            dmc.Accordion(
                children=[
                    dmc.AccordionItem(
                        id="historical-price-grid",
                        value="dataframe",
                    )
                ]
            ),

            render_footer()
        ]
    ),
    type="default",
)


@callback(
    Output("company-details-container-pg1", "children"),
    Output("company-kpis", "children"),
    Output("historical-price", "children"),
    Output("historical-price-grid", "children"),
    Input("ticker-dropdown", "value"),
    Input("date-range-picker", "value"),
)

def update_stock_explorer(ticker, date_range):

    company_dataframe, stock_dataframe = prepare_callback_data(ticker, date_range)

    company_data = prepare_company_data(company_dataframe)
    company_kpis = prepare_company_kpi_cards(company_data)

    historical_price_chart = render_historical_price(stock_dataframe)

    return (
        render_company_details(company_data["company"]),
        render_kpis(company_kpis),
        render_one_plot_container("Historical Price", historical_price_chart),
        render_historical_price_grid(stock_dataframe)
    )