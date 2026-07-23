import dash_mantine_components as dmc


def render_company_details(company):

    company_details = [
        dmc.Title(
            f"{company['name']} ({company['ticker']})",
            order=4,
        ),

        dmc.Text(
            f"{company['sector']} • {company['industry']}",
            size="sm",
            c="dimmed",
        ),
    ]

    return company_details