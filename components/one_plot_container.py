import dash_mantine_components as dmc
from dash import dcc


def render_one_plot_container(title, figure):
    rendered_plot = [
        dmc.Title(
            title,
            order=4,
        ),
        dcc.Graph(figure=figure),
    ]

    return rendered_plot