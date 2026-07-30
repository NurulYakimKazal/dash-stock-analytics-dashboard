import plotly.graph_objects as go
import numpy as np

from utils.empty_graph import empty_chart


DAILY_RETURNS_REQUIRED_COLUMNS = ["date", "close"]


def render_daily_returns(stock_df):

    missing_columns = [
        col for col in DAILY_RETURNS_REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return empty_chart(
            "No stock data available."
        )

    elif missing_columns:
        return empty_chart(
            f"Missing stock data: {', '.join(missing_columns)}"
        )

    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
        df["close"]
        .pct_change()
        * 100
    )

    df = df.dropna(subset=["daily_return"])

    if df.empty:
        return empty_chart(
            "At least two trading days required<br>"
            "to calculate daily returns."
        )

    df["color"] = df["daily_return"].apply(
        lambda x: "#00CC96" if x >= 0 else "#EF553B"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["daily_return"],
            marker_color=df["color"],
            name="Daily Return",
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
        yaxis_title="Daily Return (%)",
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
        height=350,
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
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        zeroline=False,
    )

    return fig


RETURN_HISTOGRAM_REQUIRED_COLUMNS = ["close"]


def render_return_histogram(stock_df):

    missing_columns = [
        col for col in RETURN_HISTOGRAM_REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return empty_chart(
            "No stock data available."
        )

    elif missing_columns:
        return empty_chart(
            f"Missing stock data: {', '.join(missing_columns)}"
        )

    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
        df["close"]
        .pct_change()
        * 100
    )

    df = df.dropna(subset=["daily_return"])

    if df.empty:
        return empty_chart(
            "At least two trading days required<br>"
            "to calculate daily returns."
        )

    edges = np.arange(-10, 11, 1)

    counts, edges = np.histogram(
        df["daily_return"],
        bins=edges
    )

    centers = (
        edges[:-1] + edges[1:]
    ) / 2

    widths = np.diff(edges)

    bin_labels = [
        f"{left:.2f}% to {right:.2f}%"
        for left, right in zip(
            edges[:-1],
            edges[1:]
        )
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=centers,
            y=counts,
            width=widths,
            marker=dict(
                color="#636EFA",
                line=dict(
                    color="white",
                    width=1,
                ),
            ),
            customdata=bin_labels,
            hovertemplate=(
                "Return Range: %{customdata}<br>"
                "Frequency: %{y}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.add_vline(
        x=df["daily_return"].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text="Average",
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#374151",
            font=dict(
                color="#374151",
                size=13,
            ),
        ),
        showlegend=False,
        height=350,
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
        gridcolor="rgba(0,0,0,0.08)",
        gridwidth=1,
        zeroline=False,
    )

    return fig