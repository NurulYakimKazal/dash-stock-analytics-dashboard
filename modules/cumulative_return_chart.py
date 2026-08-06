import plotly.graph_objects as go
import pandas as pd
from modules.empty_graph import empty_chart


REQUIRED_COLUMNS = ["date", "close"]


def render_cumulative_return(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return empty_chart("No historical price data available")

    elif missing_columns:
        return empty_chart(f"Missing stock data: {', '.join(missing_columns)}")

    df = stock_df.copy()

    if len(df) < 2:
        return empty_chart("At least two trading days are required to plot cumulative return.")

    df["date"] = pd.to_datetime(df["date"])

    # Table is descending:
    # iloc[-1] = earliest date
    # iloc[0]  = latest date
    first_close = df["close"].iloc[-1]

    df["cumulative_return"] = (
        (df["close"] / first_close) - 1
    ) * 100

    # Reverse only for chart display (oldest → newest)
    df = df.iloc[::-1]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["cumulative_return"],
            mode="lines",
            name="Cumulative Return",
            line=dict(
                color="royalblue",
                width=2,
            ),
            hovertemplate=(
                "Return: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#374151",
            font=dict(
                color="#374151",
                size=13,
            ),
        ),
        height=400,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        )
    )

    fig.update_xaxes(
        title=dict(
            standoff=20,
        ),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(
            standoff=15,
        ),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        zeroline=False,
    )

    return fig