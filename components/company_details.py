import dash_mantine_components as dmc


def render_company_details(company):

    company_details = [
        dmc.Title(
            f"{company['name']} ({company['ticker']})",
            order=3,
            fz={
                "base": "h4",  # mobile
                "sm": "h4",  # tablet
                "md": "h3",  # desktop
            }
        ),

        dmc.Text(
            f"{company['sector']} • {company['industry']}",
            c="dimmed",
            fz={
                "base": "xs",
                "sm": "sm",
                "md": "sm",
                "lg": "md",
            },
        ),
    ]

    return company_details