import plotly.graph_objects as go
from utils.empty_graph import empty_chart

REQUIRED_COLUMNS = ["date", "volume"]

def render_volume_activity(stock_df):

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

    if len(df) < 20:
        info_message = (
            "Less than 20 trading days available. "
            "Moving average lines may be incomplete."
        )

    df["average_volume"] = (
        df["volume"]
        .rolling(window=20)
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Daily Volume",
            marker=dict(
                color="#636EFA",
            ),
            hovertemplate=(
                "Volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["average_volume"],
            mode="lines",
            name="20-Day Average Volume",
            line=dict(
                color="#EF553B",
                width=2,
            ),
            hovertemplate=(
                "20-Day Avg: %{y:,.0f}"
                "<extra></extra>"
            ),
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
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#374151",
            font=dict(
                color="#374151",
                size=13,
            ),
        ),
        showlegend=False,
        height=400,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
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
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig