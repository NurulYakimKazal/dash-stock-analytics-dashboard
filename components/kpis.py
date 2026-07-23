import dash_mantine_components as dmc


def render_kpis(kpis):
    rendered_kpis = [
        dmc.Paper(
            [
                dmc.Text(
                    kpi_name,
                ),
                dmc.Title(
                    kpi_value,
                    order=3,
                ),
            ],
            p="md",
            shadow="xs",
            withBorder=True,
        )
        for kpi_name, kpi_value in kpis.items()
    ]

    return rendered_kpis