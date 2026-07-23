from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from io import BytesIO
from datetime import datetime


def generate_pdf_report(
    company_kpis,
    performance_kpis,
    risk_kpis,
    descriptive_stats,
    charts,
    start_date,
    end_date,
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
    )

    doc.title = f"{company_kpis['company']['name']} Stock Report"
    doc.author = "Stock Dashboard"
    doc.subject = "Financial analysis report"

    styles = getSampleStyleSheet()

    story = []

    company = company_kpis["company"]


    # Title
    story.append(
        Paragraph(
            "Stock Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 10)
    )


    # Company information

    story.append(
        Paragraph(
            f"<b>{company['name']} ({company['ticker']})</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"{company['sector']} | {company['industry']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Analysis Period: {start_date:%d %b %Y} - {end_date:%d %b %Y}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now():%d %b %Y}",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 5)
    )


    # Market snapshot

    add_section(
        story,
        "Market Snapshot",
        styles
    )

    add_metrics(
        story,
        {
            "Market Cap": company_kpis["market_cap"],
            "P/E Ratio": company_kpis["trailing_pe"],
            "Dividend Yield": company_kpis["dividend"],
            "Beta": company_kpis["beta"],
        }
    )


    # Performance

    add_section(
        story,
        "Performance Summary",
        styles
    )

    add_metrics(
        story,
        {
            "Total Return": performance_kpis["total_return"],
            "Highest Close": performance_kpis["highest_close"],
            "Lowest Close": performance_kpis["lowest_close"],
        }
    )


    # Cumulative Return
    add_section(
        story,
        "Cumulative Return",
        styles
    )

    add_plot(
        story,
        charts.get("cumulative_return"),
        styles,
    )


    # Risk

    add_section(
        story,
        "Risk Summary",
        styles
    )

    add_metrics(
        story,
        {
            "Volatility": risk_kpis["volatility"],
            "Annualized Volatility": risk_kpis["annualized_volatility"],
            "Maximum Drawdown": risk_kpis["maximum_drawdown"],
            "Best Trading Day": risk_kpis["best_trading_day"],
            "Worst Trading Day": risk_kpis["worst_trading_day"],
        }
    )


    # Trend Overview
    add_section(
        story,
        "Trend Overview",
        styles
    )

    add_plot(
        story,
        charts.get("trend"),
        styles,
    )


    # Statistics

    add_section(
        story,
        "Descriptive Statistics",
        styles
    )

    add_dataframe(
        story,
        descriptive_stats
    )

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            "Data Source: Yahoo Finance (yfinance). "
            "Historical stock prices, trading volume, and company information "
            "are retrieved through the yfinance Python library. "
            "Data availability and accuracy are subject to Yahoo Finance services.",
            styles["BodyText"],
        )
    )


    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()



def add_section(
    story,
    title,
    styles
):

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            title,
            styles["Heading2"]
        )
    )



def add_metrics(
    story,
    metrics
):

    data = [
        ["Metric", "Value"]
    ]

    for key, value in metrics.items():

        data.append(
            [
                key,
                str(value)
            ]
        )


    table = Table(
        data,
        colWidths=[150, 250]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.grey
                ),
            ]
        )
    )

    story.append(table)



def add_dataframe(
    story,
    df
):

    if df.empty:
        story.append(
            Paragraph(
                "No descriptive statistics available.",
                getSampleStyleSheet()["BodyText"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        return


    data = [
        list(df.columns)
    ]

    for _, row in df.iterrows():

        data.append(
            list(row.values)
        )


    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.25,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.lightgrey
                ),
            ]
        )
    )

    story.append(table)



def add_plot(
    story,
    fig,
    styles,
):

    if fig is None:
        story.append(
            Paragraph(
                "<i>Chart unavailable.</i>",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 12))
        return

    fig.update_xaxes(
        nticks=6,
        tickformat="%b %Y",
        tickangle=45,
    )

    fig.update_layout(
        margin=dict(
            l=60,
            r=40,
            t=50,
            b=80,
        ),
    )

    image_buffer = BytesIO()

    fig.write_image(
        image_buffer,
        format="png",
        width=800,
        height=450,
    )

    image_buffer.seek(0)

    story.append(
        Image(
            image_buffer,
            width=450,
            height=190,
        )
    )

    story.append(
        Spacer(1, 12)
    )