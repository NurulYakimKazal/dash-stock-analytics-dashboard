import dash_mantine_components as dmc
from components.one_plot_container import render_one_plot_container


def render_chart_grid(charts):
    chart_grid = dmc.Grid(
        [
            dmc.GridCol(
                render_one_plot_container(title, plot_id),
                span={"base": 12, "lg": 6},
            )
            for title, plot_id in charts
        ],
        gutter=10,
    )

    return chart_grid