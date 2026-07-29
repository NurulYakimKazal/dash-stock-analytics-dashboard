import dash
from dash import Input, Output, dcc, callback
import dash_mantine_components as dmc

from components.page_title import render_page_title
from components.company_details import render_company_details
from components.kpis import render_kpis
from components.one_plot_container import render_one_plot_container
from components.two_plot_container import render_two_plot_container
from components.descriptive_statistics_grid import render_descriptive_statistics_grid
from components.footer import render_footer
from modules.callback_data_processing import prepare_callback_data
from modules.company_data import prepare_company_data
from modules.performance_overview import (
    prepare_performance_overview_data,
    prepare_performance_overview_kpi_cards
)
from modules.cumulative_return_chart import render_cumulative_return
from modules.return_analysis_charts import (
    render_daily_returns,
    render_return_histogram
)
from modules.risk_analysis import (
    prepare_risk_analysis_data,
    prepare_risk_analysis_kpi_cards
)
from modules.trend_indicators_chart import render_trend_indicators
from modules.volume_activity_chart import render_volume_activity
from modules.descriptive_statistics import prepare_descriptive_statistics_data


dash.register_page(
    __name__,
    path="/analytics",
)


layout = dcc.Loading(
    children=dmc.Container(
        [
            render_page_title("Analytics", "mdi:chart-box"),

            dmc.Space(h="xl"),

            # Company Details
            dmc.Stack(
                id="company-details-container-pg2",
                gap=2
            ),

            dmc.Space(h="xl"),

            dmc.Stack(
                [
                    dmc.Title(
                        "Performance Overview",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dmc.SimpleGrid(
                        id="performance-overview-kpis",
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
                id="cumulative-return-pg2",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="xl"),

            dmc.Stack(
                [
                    dmc.Grid(
                        id="return-analysis",
                        gutter=10
                    ),
                ],
                gap="sm",
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),
            dmc.Space(h="lg"),

            dmc.Stack(
                [
                    dmc.Title(
                        "Risk Analysis",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dmc.SimpleGrid(
                        id="risk-analysis-kpis",
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
                id="trend-indicators",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="xl"),

            dmc.Paper(
                id="volume-activity",
                withBorder=True,
                radius="md",
                p="sm"
            ),

            dmc.Space(h="lg"),
            dmc.Divider(),

            dmc.Accordion(
                children=[
                    dmc.AccordionItem(
                        id="descriptive-statistics-pg2",
                        value="dataframe",
                    )
                ],
                value="dataframe",
            ),

            render_footer()
        ]
    ),
    type="default",
)


@callback(
    Output("company-details-container-pg2", "children"),
    Output("performance-overview-kpis", "children"),
    Output("cumulative-return-pg2", "children"),
    Output("return-analysis", "children"),
    Output("risk-analysis-kpis", "children"),
    Output("trend-indicators", "children"),
    Output("volume-activity", "children"),
    Output("descriptive-statistics-pg2", "children"),
    Input("ticker-dropdown", "value"),
    Input("date-range-picker", "value"),
)

def update_analytics(ticker, date_range):

    company_dataframe, stock_dataframe = prepare_callback_data(ticker, date_range)

    company_data = prepare_company_data(company_dataframe)

    performance_overview_data = prepare_performance_overview_data(stock_dataframe)
    performance_overview_kpis = prepare_performance_overview_kpi_cards(performance_overview_data)

    cumulative_return_chart = render_cumulative_return(stock_dataframe)

    daily_return_chart = render_daily_returns(stock_dataframe)
    return_histogram_chart = render_return_histogram(stock_dataframe)

    risk_analysis_data = prepare_risk_analysis_data(stock_dataframe)
    risk_analysis_kpis = prepare_risk_analysis_kpi_cards(risk_analysis_data)

    trend_indicators_chart = render_trend_indicators(stock_dataframe)
    volume_activity_chart = render_volume_activity(stock_dataframe)

    descriptive_statistics_data = prepare_descriptive_statistics_data(stock_dataframe)

    return (
        render_company_details(company_data["company"]),
        render_kpis(performance_overview_kpis),
        render_one_plot_container("Cumulative Return", cumulative_return_chart),
        render_two_plot_container(daily_return_chart, return_histogram_chart),
        render_kpis(risk_analysis_kpis),
        render_one_plot_container("Trend Indicators", trend_indicators_chart),
        render_one_plot_container("Volume Activity", volume_activity_chart),
        render_descriptive_statistics_grid(descriptive_statistics_data)
    )