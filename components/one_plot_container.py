import dash_mantine_components as dmc
from dash import dcc


def render_one_plot_container(title, figure):
    rendered_plot = [
        dmc.Title(
            title,
            order=4,
            fz={
                "base": "h5",  # mobile
                "sm": "h4",  # tablet
                "md": "h4",  # desktop
            }
        ),
        dcc.Graph(figure=figure),
    ]

    return rendered_plot