import dash_mantine_components as dmc
import dash_ag_grid as dag


REQUIRED_COLUMNS = [
    "Metric",
    "Value",
    "Unit"
]


def render_descriptive_statistics_grid(df):

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if df.empty:
        return [
            dmc.AccordionControl(
                "Descriptive Statistics",
            ),
            dmc.AccordionPanel(
                dmc.Text(
                    "Descriptive statistics data unavailable",
                    c="dimmed",
                )
            ),
        ]

    elif missing_columns:
        return [
            dmc.AccordionControl(
                "Descriptive Statistics",
            ),
            dmc.AccordionPanel(
                dmc.Text(
                    f"Missing descriptive statistics data: {', '.join(missing_columns)}",
                    c="dimmed",
                )
            ),
        ]

    else:
        return [
            dmc.AccordionControl(
                "Descriptive Statistics"
            ),
            dmc.AccordionPanel(
                dag.AgGrid(
                    rowData=df.to_dict("records"),
                    columnDefs=[
                        {
                            "field": col,
                        }
                        for col in df.columns
                    ],
                    defaultColDef={
                        "flex": 1,
                        "minWidth": 100,
                        "resizable": True,
                    },

                    dashGridOptions={
                        "pagination": False,
                        "suppressHorizontalScroll": False,
                    },

                    style={
                        "width": "100%",
                        "height": "302px",
                    },
                )
            ),
        ]