import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.empty_graph import empty_chart


REQUIRED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def render_historical_price(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return empty_chart("No historical price data available")

    elif missing_columns:
        return empty_chart(f"Missing stock data: {', '.join(missing_columns)}")

    # Reverse database order:
    # latest → oldest becomes oldest → latest
    stock_df = stock_df.iloc[::-1].copy()


    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
    )


    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=stock_df["date"],
            open=stock_df["open"],
            high=stock_df["high"],
            low=stock_df["low"],
            close=stock_df["close"],
            name="Price",
            hovertemplate=(
                "Open: $%{open:.2f}<br>"
                "High: $%{high:.2f}<br>"
                "Low: $%{low:.2f}<br>"
                "Close: $%{close:.2f}"
                "<extra></extra>"
            ),
        ),
        row=1,
        col=1,
    )


    # Volume
    fig.add_trace(
        go.Bar(
            x=stock_df["date"],
            y=stock_df["volume"],
            name="Volume",
            marker=dict(
                color="#636EFA"
            ),
            hovertemplate=(
                "Volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        ),
        row=2,
        col=1,
    )


    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False,
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
        height=700,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        row=1,
        col=1,
    )

    fig.update_xaxes(
        title=dict(
            text="Date",
            standoff=20,
        ),
        showgrid=False,
        row=2,
        col=1,
    )

    fig.update_yaxes(
        title=dict(
            text="Price",
            standoff=15,
        ),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        zeroline=False,
        row=1,
        col=1,
    )

    fig.update_yaxes(
        title=dict(
            text="Volume",
            standoff=15,
        ),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        zeroline=False,
        row=2,
        col=1,
    )

    return fig