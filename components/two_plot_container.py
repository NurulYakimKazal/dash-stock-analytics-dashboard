import dash_mantine_components as dmc
from dash import dcc


def render_two_plot_container(figure_1, figure_2):
    rendered_plot = [
        dmc.GridCol(
            dcc.Graph(figure=figure_1),
            span=6,
        ),
        dmc.GridCol(
            dcc.Graph(figure=figure_2),
            span=6,
        ),
    ]

    return rendered_plot