import dash_mantine_components as dmc


def render_kpis(kpis):
    rendered_kpis = [
        dmc.Paper(
            [
                dmc.Text(
                    kpi_name,
                    fz={
                        "base": "sm",
                        "sm": "sm",
                        "md": "md",
                    }
                ),
                dmc.Title(
                    kpi_value,
                    order=3,
                    fz={
                        "base": "h5",  # mobile
                        "sm": "h4",  # tablet
                        "md": "h3",  # desktop
                    }
                ),
            ],
            p="md",
            shadow="xs",
            withBorder=True,
        )
        for kpi_name, kpi_value in kpis.items()
    ]

    return rendered_kpis