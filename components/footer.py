import dash_mantine_components as dmc


def render_footer():

    return dmc.Stack(
        [
            dmc.Text(
                [
                    "Data Source: Yahoo Finance (",
                    dmc.Code("yfinance"),
                    ")",
                    dmc.Space(h=4),
                    "Historical stock prices, trading volume, and company information "
                    "are retrieved through the ",
                    dmc.Code("yfinance"),
                    " Python library. Data availability and accuracy are subject "
                    "to Yahoo Finance services.",
                ],
                c="dimmed",
                fz={
                    "base": "xs",
                    "sm": "sm",
                    "md": "sm",
                },
            ),
        ],
        gap="sm",
        mt="xl",
        mb="md",
    )
