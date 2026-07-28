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
                    DashIconify(
                        icon="mdi:finance",
                        width=24,
                    ),
                    size="lg",
                    radius="sm",
                    color="blue",
                    variant="filled",
                ),

                dmc.Title(
                    "Stock Analytics Dashboard",
                    order=1,
                    fz={
                        "base": "h3",  # mobile
                        "sm": "h3",  # tablet
                        "md": "h2",  # desktop
                    },
                ),
            ],

            px="lg",
            h="100%",
        ),
    )

    return header