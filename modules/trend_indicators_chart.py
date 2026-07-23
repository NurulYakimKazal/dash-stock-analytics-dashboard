import plotly.graph_objects as go
from utils.empty_graph import empty_chart


REQUIRED_COLUMNS = ["date", "close"]


def render_trend_indicators(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return empty_chart("No historical price data available")

    elif missing_columns:
        return empty_chart(f"Missing stock data: {', '.join(missing_columns)}")

    df = stock_df.iloc[::-1].copy()

    info_message = None

    if len(df) < 50:
        info_message = (
            "Less than 50 trading days available. "
            "Moving average lines may be incomplete."
        )

    df["MA20"] = (
        df["close"]
        .rolling(window=20)
        .mean()
    )

    df["MA50"] = (
        df["close"]
        .rolling(window=50)
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["close"],
            name="Close Price",
            line=dict(
                color="#636EFA",
                width=2,
            ),
            hovertemplate=(
                "Close: $%{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["MA20"],
            name="20-Day MA",
            line=dict(
                color="#EF553B",
                width=2,
            ),
            hovertemplate=(
                "MA-20: $%{y:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["MA50"],
            name="50-Day MA",
            line=dict(
                color="#00CC96",
                width=2,
            ),
            hovertemplate=(
                "MA-50: $%{y:.2f}"
                "<extra></extra>"
            )
        )
    )

    if info_message:
        fig.add_annotation(
            text=info_message,
            x=0.5,
            y=1.06,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(
                size=12,
                color="gray",
            ),
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=400,
        hovermode="x unified",
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    return fig