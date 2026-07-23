import dash_mantine_components as dmc
from dash_iconify import DashIconify


def render_page_title(title, icon):
    page_title = dmc.Group(
        [
            dmc.ThemeIcon(
                DashIconify(icon=icon),
                color="blue",
                variant="light",
                radius="xl",
            ),

            dmc.Title(
                title,
                order=2,
            ),
        ],
        gap="sm",
    )

    return page_title