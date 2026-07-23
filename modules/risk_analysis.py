import numpy as np
import pandas as pd


DEFAULT_VALUES = {
    "volatility": "N/A",
    "maximum_drawdown": "N/A",
    "best_trading_day": "N/A",
    "worst_trading_day": "N/A",
    "annualized_volatility": "N/A",
}


REQUIRED_COLUMNS = ["close"]


def prepare_risk_analysis_data(stock_df):

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in stock_df.columns
    ]

    if stock_df.empty or missing_columns:
        return DEFAULT_VALUES

    # Reverse dataframe for chronological calculations
    df = stock_df.iloc[::-1].copy()

    # Daily Returns
    daily_returns = df["close"].pct_change().dropna()

    # Volatility
    volatility = (
        f"{daily_returns.std() * 100:.2f}%"
        if not daily_returns.empty
        else "N/A"
    )

    # Maximum Drawdown
    cumulative_max = df["close"].cummax()
    drawdown = (
            (df["close"] - cumulative_max)
            / cumulative_max
    )

    max_drawdown_value = drawdown.min()

    maximum_drawdown = (
        f"{max_drawdown_value * 100:.2f}%"
        if pd.notna(max_drawdown_value)
        else "N/A"
    )

    # Best Trading Day
    best_day = daily_returns.max()

    best_trading_day = (
        f"{best_day * 100:.2f}%"
        if pd.notna(best_day)
        else "N/A"
    )

    # Worst Trading Day
    worst_day = daily_returns.min()

    worst_trading_day = (
        f"{worst_day * 100:.2f}%"
        if pd.notna(worst_day)
        else "N/A"
    )

    # Annualized Volatility
    annualized_volatility = (
        f"{daily_returns.std() * np.sqrt(252) * 100:.2f}%"
        if not daily_returns.empty
        else "N/A"
    )

    return {
        "volatility": volatility,
        "annualized_volatility": annualized_volatility,
        "maximum_drawdown": maximum_drawdown,
        "best_trading_day": best_trading_day,
        "worst_trading_day": worst_trading_day,
    }



def prepare_risk_analysis_kpi_cards(risk_analysis_data):
    return {
        "Volatility": risk_analysis_data["volatility"],
        "Annualized Volatility": risk_analysis_data["annualized_volatility"],
        "Maximum Drawdown": risk_analysis_data["maximum_drawdown"],
        "Best Trading Day": risk_analysis_data["best_trading_day"],
        "Worst Tranding Day": risk_analysis_data["worst_trading_day"],
    }