import dash_mantine_components as dmc
import dash_ag_grid as dag


REQUIRED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def render_historical_price_grid(df):

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if df.empty or missing_columns:
        return [
            dmc.AccordionControl(
                "Historical Price Data"
            ),
            dmc.AccordionPanel(
                dmc.Text(
                    "Historical price data unavailable",
                    c="dimmed",
                )
            ),
        ]

    elif missing_columns:
        return [
            dmc.AccordionControl(
                "Historical Price Data"
            ),
            dmc.AccordionPanel(
                dmc.Text(
                    f"Missing stock data: {', '.join(missing_columns)}",
                    c="dimmed",
                )
            ),
        ]

    else:
        return [
            dmc.AccordionControl(
                "Historical Price Data"
            ),
            dmc.AccordionPanel(
                dag.AgGrid(
                    rowData=df.to_dict("records"),
                    columnDefs=[
                        {
                            "field": col,
                            **(
                                {}
                                if col in ["date", "volume"]
                                else {
                                    "valueFormatter": {
                                        "function": "Number(params.value).toFixed(2)"
                                    }
                                }
                            ),
                        }
                        for col in df.columns
                        if col != "ticker"
                    ],
                    dashGridOptions={
                        "pagination": False,
                        "paginationPageSize": 10,
                        "suppressHorizontalScroll": False,
                    },
                    style={
                        "width": "100%",
                    },
                )
            ),
        ]