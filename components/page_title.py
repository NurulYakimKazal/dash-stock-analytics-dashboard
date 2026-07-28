import dash_mantine_components as dmc
from dash_iconify import DashIconify


def render_page_title(title, icon):
    page_title = dmc.Group(
        [
            dmc.ThemeIcon(
                DashIconify(icon=icon),
                size="md",
                radius="sm",
                color="blue",
                variant="filled",
            ),

            dmc.Title(
                title,
                order=2,
                fz={
                    "base": "h4",  # mobile
                    "sm": "h3",  # tablet
                    "md": "h2",  # desktop
                }
            ),
        ],
        gap="sm",
    )

    return page_title