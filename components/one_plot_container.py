from dash import dcc
import dash_mantine_components as dmc


def render_one_plot_container(title, plot_id):
    one_plot_container = dmc.Paper(
        [
            dmc.Title(
                title,
                order=4,
                fz={
                    "base": "h5",  # mobile
                    "sm": "h4",  # tablet
                    "md": "h4",  # desktop
                }
            ),
            dcc.Graph(id=plot_id),
        ],
        withBorder=True,
        radius="md",
        p="sm"
    )

    return one_plot_container