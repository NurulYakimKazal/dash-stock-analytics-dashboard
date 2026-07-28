import dash_mantine_components as dmc
from dash import dcc


def render_two_plot_container(figure_1, figure_2):
    rendered_plot = [
        dmc.GridCol(
            dmc.Paper(
                [
                    dmc.Title(
                        "Daily Return Over Time",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dcc.Graph(figure=figure_1)
                ],
                withBorder=True,
                radius="md",
                p="sm"
            ),
            span={"base": 12, "lg": 6},
        ),
        dmc.GridCol(
            dmc.Paper(
                [
                    dmc.Title(
                        "Return Distribution",
                        order=4,
                        fz={
                            "base": "h5",  # mobile
                            "sm": "h4",  # tablet
                            "md": "h4",  # desktop
                        }
                    ),
                    dcc.Graph(figure=figure_2)
                ],
                withBorder=True,
                radius="md",
                p="sm"
            ),
            span={"base": 12, "lg": 6},
        ),
    ]

    return rendered_plot