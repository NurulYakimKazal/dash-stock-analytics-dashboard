import pandas as pd


DEFAULT_COMPANY_DATA = {
    "company": {
        "name": "N/A",
        "ticker": "N/A",
        "sector": "N/A",
        "industry": "N/A",
    },
    "market_cap": "N/A",
    "trailing_pe": "N/A",
    "dividend": "N/A",
    "beta": "N/A",
}


REQUIRED_COLUMNS = [
    "name",
    "ticker",
    "sector",
    "industry",
    "market_cap",
    "trailing_pe",
    "dividend_yield",
    "beta",
]


def format_market_cap(value):
    """Format market capitalization into a human-readable string."""

    if pd.isna(value):
        return "N/A"

    elif value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    else:
        return f"${value:,.0f}"


def format_number(value):
    """Format a numeric value with two decimal places."""

    return f"{value:.2f}" if pd.notna(value) else "N/A"


def format_percentage(value):
    """Format a percentage value."""

    return f"{value:.2f}%" if pd.notna(value) else "N/A"


def prepare_company_data(company_df):
    """Prepare company information for display."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in company_df.columns
    ]

    if company_df.empty or missing_columns:
        return DEFAULT_COMPANY_DATA

    company = company_df.iloc[0].to_dict()

    return {
        "company": company,
        "market_cap": format_market_cap(company["market_cap"]),
        "trailing_pe": format_number(company["trailing_pe"]),
        "dividend": format_percentage(company["dividend_yield"]),
        "beta": format_number(company["beta"]),
    }


def prepare_company_kpi_cards(company_data):
    """Prepare KPI cards for the company overview."""

    return {
        "Market Cap": company_data["market_cap"],
        "P/E Ratio": company_data["trailing_pe"],
        "Dividend Yield": company_data["dividend"],
        "Beta": company_data["beta"],
    }