import dash
from dash import Input, Output, State, dcc, callback
import dash_mantine_components as dmc
import pandas as pd

from components.page_title import render_page_title
from components.company_details import render_company_details
from components.kpis import render_kpis
from components.one_plot_container import render_one_plot_container
from components.descriptive_statistics_grid import render_descriptive_statistics_grid
from components.footer import render_footer
from modules.callback_data_processing import prepare_callback_data
from modules.company_data import (
    prepare_company_data,
    prepare_company_kpi_cards,
)
from modules.performance_overview import (
    prepare_performance_overview_data,
    prepare_performance_overview_kpi_cards
)
from modules.cumulative_return_chart import render_cumulative_return
from modules.risk_analysis import (
    prepare_risk_analysis_data,
    prepare_risk_analysis_kpi_cards
)
from modules.trend_indicators_chart import render_trend_indicators
from modules.descriptive_statistics import prepare_descriptive_statistics_data
from modules.pdf_report_generator import generate_pdf_report


dash.register_page(
    __name__,
    path="/report",
)


layout = dcc.Loading(
    children=dmc.Container(
        [
            render_page_title("Report", "mdi:file-chart"),

            dmc.Space(h="xl"),

            # Company Details
            dmc.Stack(
                id="company-details-container-pg3",
                gap=2
            ),

            dmc.Space(h="xl"),

            # KPIs
            dmc.Stack(
                children=[
                    dmc.Title(
                        "Market Snapshot",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dmc.SimpleGrid(
                        id="market-snapshot",
                        cols={"base": 2, "md": 4},
                        spacing=5,
                    ),
                ]
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Stack(
                [
                    dmc.Title(
                        "Performance Summary",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dmc.SimpleGrid(
                        id="performance-summary-kpis",
                        cols={"base": 2, "md": 3},
                        spacing=5,
                    ),
                ],
                gap="sm",
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Paper(
                id="cumulative-return-pg3",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Stack(
                [
                    dmc.Title(
                        "Risk Summary",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dmc.SimpleGrid(
                        id="risk-summary-kpis",
                        cols={"base": 2, "md": 3},
                        spacing=5,
                    ),
                ],
                gap="sm",
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Paper(
                id="trend-overview",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),

            dmc.Accordion(
                children=[
                    dmc.AccordionItem(
                        id="descriptive-statistics-pg3",
                        value="dataframe",
                    )
                ],
                value="dataframe",
            ),

            dmc.Space(h="xl"),

            dmc.Group(
                justify="left",
                children=[
                    dmc.Button(
                        "Download PDF Report",
                        id="download-pdf-btn",
                        color="blue",
                        variant="filled",
                    ),
                ],
            ),

            dcc.Download(id="download-pdf"),

            dmc.Space(h="xl"),

            dmc.Divider(),

            render_footer(),
        ]
    ),
    type="default",
)


@callback(
    Output("company-details-container-pg3", "children"),
    Output("market-snapshot", "children"),
    Output("performance-summary-kpis", "children"),
    Output("cumulative-return-pg3", "children"),
    Output("risk-summary-kpis", "children"),
    Output("trend-overview", "children"),
    Output("descriptive-statistics-pg3", "children"),
    Input("ticker-dropdown", "value"),
    Input("date-range-picker", "value"),
)

def update_report(ticker, date_range):

    company_dataframe, stock_dataframe = prepare_callback_data(ticker, date_range)

    company_data = prepare_company_data(company_dataframe)
    company_kpis = prepare_company_kpi_cards(company_data)

    performance_overview_data = prepare_performance_overview_data(stock_dataframe)
    performance_overview_kpis = prepare_performance_overview_kpi_cards(performance_overview_data)

    cumulative_return_chart = render_cumulative_return(stock_dataframe)

    risk_analysis_data = prepare_risk_analysis_data(stock_dataframe)
    risk_analysis_kpis = prepare_risk_analysis_kpi_cards(risk_analysis_data)

    trend_indicators_chart = render_trend_indicators(stock_dataframe)

    descriptive_statistics_data = prepare_descriptive_statistics_data(stock_dataframe)

    return (
        render_company_details(company_data["company"]),
        render_kpis(company_kpis),
        render_kpis(performance_overview_kpis),
        render_one_plot_container("Cumulative Return", cumulative_return_chart),
        render_kpis(risk_analysis_kpis),
        render_one_plot_container("Trend Overview", trend_indicators_chart),
        render_descriptive_statistics_grid(descriptive_statistics_data)
    )


@callback(
    Output("download-pdf", "data"),
    Input("download-pdf-btn", "n_clicks"),
    State("ticker-dropdown", "value"),
    State("date-range-picker", "value"),
    prevent_initial_call=True,
)
def download_pdf(_n_clicks, ticker, date_range):

    company_dataframe, stock_dataframe = prepare_callback_data(ticker, date_range)

    company_data = prepare_company_data(company_dataframe)
    performance_data = prepare_performance_overview_data(stock_dataframe)
    risk_data = prepare_risk_analysis_data(stock_dataframe)
    descriptive_statistics = prepare_descriptive_statistics_data(stock_dataframe)

    charts = {
        "cumulative_return": render_cumulative_return(stock_dataframe),
        "trend": render_trend_indicators(stock_dataframe),
    }

    pdf = generate_pdf_report(
        company_data,
        performance_data,
        risk_data,
        descriptive_statistics,
        charts,
        pd.Timestamp(date_range[0]),
        pd.Timestamp(date_range[1]),
    )

    return dcc.send_bytes(
        lambda f: f.write(pdf),
        filename=f"{ticker}_stock_report.pdf",
    )
