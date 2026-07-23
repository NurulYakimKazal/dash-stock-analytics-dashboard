import pandas as pd


REQUIRED_COLUMNS = ["close"]


def prepare_descriptive_statistics_data(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty or missing_columns or len(stock_df) < 2:
        pd.DataFrame()

    # Reverse database order:
    # latest -> oldest becomes oldest -> latest
    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
        df["close"]
        .pct_change()
        * 100
    )

    # Remove rows where daily return cannot be calculated
    df = df.dropna(subset=["daily_return"])

    # No valid return observations
    if df.empty:
        return pd.DataFrame()

    positive_days = (
            df["daily_return"] > 0
    ).sum()

    negative_days = (
            df["daily_return"] < 0
    ).sum()

    total_days = len(df)

    descriptive_stats = pd.DataFrame(
        {
            "Metric": [
                "Median Close",
                "Median Daily Return",
                "Return Skewness",
                "Return Kurtosis",
                "Positive Trading Days",
                "Negative Trading Days",
            ],
            "Value": [
                f"{df['close'].median():.2f}",
                f"{df['daily_return'].median():.2f}",
                f"{df['daily_return'].skew():.2f}",
                f"{df['daily_return'].kurtosis():.2f}",
                f"{positive_days / total_days * 100:.1f}",
                f"{negative_days / total_days * 100:.1f}",
            ],
            "Unit": [
                "USD",
                "%",
                "Ratio",
                "Ratio",
                "%",
                "%",
            ],
        }
    )



    return descriptive_stats