import dash_mantine_components as dmc
from dash_iconify import DashIconify


# ============================
# HEADER
# ============================
def render_header():

    header = dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Burger(
                    id="navbar-burger",
                    size="sm",
                    hiddenFrom="sm",
                ),

                dmc.ThemeIcon(
                    DashIconify(icon="mdi:finance"),
                    size="lg",
                    radius="xl",
                    color="blue",
                ),

                dmc.Title(
                    "Stock Analytics Dashboard",
                    order=2,
                ),
            ],

            px="lg",
            h="100%",
        ),
    )

    return header