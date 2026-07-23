import pandas as pd


DEFAULT_VALUES = {
        "total_return": "N/A",
        "highest_close": "N/A",
        "lowest_close": "N/A",
        "avg_volume": "N/A",
        "trading_days": "0",
        "avg_daily_return": "N/A",
}


REQUIRED_COLUMNS = ["close", "volume"]


def prepare_performance_overview_data(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty or missing_columns:
        return DEFAULT_VALUES

    # Total Return
    # Table is descending:
    # iloc[-1] = earliest date
    # iloc[0]  = latest date
    first_close = stock_df["close"].iloc[-1]
    last_close = stock_df["close"].iloc[0]

    total_return = (
        f"{((last_close - first_close) / first_close * 100):.2f}%"
        if (
                pd.notna(first_close)
                and pd.notna(last_close)
                and first_close != 0
        )
        else "N/A"
    )

    # Highest Close
    highest_close_value = stock_df["close"].max()

    highest_close = (
        f"{highest_close_value:.2f}"
        if pd.notna(highest_close_value)
        else "N/A"
    )

    # Lowest Close
    lowest_close_value = stock_df["close"].min()

    lowest_close = (
        f"{lowest_close_value:.2f}"
        if pd.notna(lowest_close_value)
        else "N/A"
    )

    # Average Daily Volume
    avg_volume_value = stock_df["volume"].mean()

    if pd.isna(avg_volume_value):
        avg_volume = "N/A"

    elif avg_volume_value >= 1_000_000_000_000:
        avg_volume = f"{avg_volume_value / 1_000_000_000_000:.2f}T"

    elif avg_volume_value >= 1_000_000_000:
        avg_volume = f"{avg_volume_value / 1_000_000_000:.2f}B"

    elif avg_volume_value >= 1_000_000:
        avg_volume = f"{avg_volume_value / 1_000_000:.2f}M"

    else:
        avg_volume = f"{avg_volume_value:,.0f}"

    # Trading Days
    trading_days = str(len(stock_df))

    # Average Daily Return
    # pct_change requires chronological order
    df = stock_df.iloc[::-1].copy()

    daily_returns = df["close"].pct_change().dropna()

    avg_daily_return = (
        f"{daily_returns.mean() * 100:.2f}%"
        if not daily_returns.empty
        else "N/A"
    )

    return {
        "total_return": total_return,
        "avg_daily_return": avg_daily_return,
        "avg_volume": avg_volume,
        "trading_days": trading_days,
        "highest_close": highest_close,
        "lowest_close": lowest_close,
    }



def prepare_performance_overview_kpi_cards(performance_overview_data):
    return {
        "Total Return": performance_overview_data["total_return"],
        "Average Daily Return": performance_overview_data["avg_daily_return"],
        "Average Volume": performance_overview_data["avg_volume"],
        "Trading Days": performance_overview_data["trading_days"],
        "Highest Close": performance_overview_data["highest_close"],
        "lowest Close": performance_overview_data["lowest_close"],
    }