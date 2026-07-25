# 📈 Stock Analytics & Financial Intelligence Platform

An interactive stock analytics system built with Dash for historical price analysis, performance evaluation, risk measurement, statistical exploration, and automated financial reporting.

The system transforms daily market data into structured insights through an end-to-end pipeline including data ingestion, database storage, financial calculations, interactive visualization, and PDF report generation.

---

## 🧭 Project Overview

This platform is an end-to-end stock analytics application that integrates:

* Historical market data management
* Financial KPI calculation
* Price trend analysis
* Statistical return analysis
* Risk and volatility analysis
* Trending indicators analysis
* Volume activity analysis
* Interactive Dash visualization
* Automated PDF reporting

It supports both investment research and exploratory financial analysis.

---

## 🏗️ System Architecture

This system follows a layered analytical approach:

```text
Market Data
   │
   ▼
Structured Database
   │
   ▼
Financial Metrics
   │
   ▼
Interactive Dash Dashboard
   │
   ▼
Automated Reporting
```

It separates different analytical perspectives:

* What happened (historical prices & performance)
* How it behaved (risk & volatility)
* What patterns exist (statistics & trends)

---

## 🔄 Data Pipeline Architecture

```text
Financial Market Data
        │
        ▼
ETL Pipeline
        │
        ▼
PostgreSQL Database (Supabase)
        │
        ├── Stock Price Table
        ├── Ticker Metadata
        │
        ▼
Selected Stock Dataset
        │
        ├── KPI Engine
        │       ├── Ticker Metadata
        │       ├── Performance Metrics
        │       ├── Risk Metrics
        │       └── Statistical Analysis
        │
        ├── Visualization Layer
        │       ├── Candlestick Chart
        │       ├── Cumulative Return
        │       ├── Return Analysis
        │       ├── Trend Indicators
        │       └── Volume Activity
        │
        ▼
Dash Application Layer
        │
        ├── Interactive Dashboard
        ├── Charts
        ├── Data Tables (AG Grid)
        ├── User Controls
        └── PDF Export
```

---

# ✨ Key Features

## 📊 Historical Price Analysis

* Interactive candlestick visualization
* Daily OHLC price tracking
* Trading volume analysis
* Historical price exploration

## 📈 Performance Analysis

* Total return calculation
* Average daily return
* Average trading volume
* Trading day count
* Highest and lowest closing price

## 📐 Return Analysis

* Cumulative return tracking
* Daily return visualization
* Return distribution histogram

## ⚠️ Risk Analysis

* Daily volatility
* Annualized volatility
* Maximum drawdown
* Best trading day
* Worst trading day

## 📉 Trend Analysis

* Long-term price trend visualization
* Moving average indicators:

  * 20-day moving average
  * 50-day moving average

## 📋 Statistical Exploration

* Median closing price
* Median daily return
* Return skewness
* Return kurtosis
* Positive/negative trading day analysis

## 📄 Automated Reporting

* Generates PDF financial reports
* Includes KPI summaries
* Embeds analytical charts
* Supports downloadable reports

---

# 🧰 Tech Stack

* Python
* Dash
* Plotly
* Plotly Express
* Pandas
* NumPy
* PostgreSQL
* Supabase
* SQLAlchemy
* psycopg2
* ReportLab
* Kaleido
* python-dotenv
* APScheduler

---

# 🧹 Data Engineering Pipeline

* Retrieves historical stock market data
* Cleans and validates financial records
* Stores structured OHLCV data
* Prevents duplicate records using database constraints
* Uses scheduled incremental synchronization via a cron-based ETL job 
* Maintains database consistency through primary keys

---

# 🗄️ Database Design

The application uses PostgreSQL hosted on Supabase.

Main table:

```text
stock_prices

ticker
date
open
high
low
close
volume
```

Primary key:

```text
(ticker, date)
```

This prevents duplicate daily records for the same stock.

---

# 🧠 Analytical Methodology

## Performance Metrics

* Return calculations are based on historical closing prices.
* Daily returns are calculated using percentage change between trading days.

## Risk Metrics

* Volatility measures daily return dispersion.
* Annualized volatility uses 252 trading days.
* Maximum drawdown measures the largest historical decline from peak value.

## Technical Indicators

Moving averages are calculated using rolling windows:

* MA20 → short-term trend
* MA50 → medium-term trend

---

# 📁 Project Structure

```text
DashStockDashboard/
├── assets/                    # dashboard styles and screenshots
├── components/                # reusable Dash UI components
├── modules/                   # Dash analytics & visualization modules
├── pages/                     # Dash pages
├── scripts/                   # batch jobs (backfill)
├── src/                       # ETL + database layer
│   ├── db/
│   └── etl/
├── utils/   
├── app.py                     # main Dash application
├── scheduler.py               # scheduled ETL jobs
├── requirements.txt
├── .env.example
└── README.md
```

---

# 📊 Design Philosophy

This system follows a layered analytical approach:

```text
Raw Market Data
      │
      ▼
Structured Financial Data
      │
      ▼
Calculated Metrics
      │
      ▼
Interactive Dash Insights
      │
      ▼
Financial Report
```

It separates analytical perspectives:

* What happened (historical price movement)
* How it performed (returns & KPIs)
* How risky it was (volatility & drawdown)
* What patterns exist (statistics & trends)

---

# 📸 Screenshots

## 📈 Stock Explorer

Stock summary, company information, company KPIs, candlestick chart, and trading volume visualization.

![Stock Explorer 1](assets/stock_explorer_1.png)

![Stock Explorer 2](assets/stock_explorer_2.png)

---

## 📊 Analytics 

Performance, risk, trend, volume, and statistical analysis.

![Analytics 1](assets/analytics_1.png)

![Analytics 2](assets/analytics_2.png)

![Analytics 3](assets/analytics_3.png)

![Analytics 4](assets/analytics_4.png)

---

## 📄 Report

Automatically generated analytical report.

![Report 1](assets/report_1.png)

![Report 2](assets/report_2.png)

![Report 3](assets/report_3.png)

![PDF Report](assets/report_4.png)

---

# ▶️ How to Run Locally

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure Environment Variables

Create `.env` based on `.env.example`.

Example:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=6543
DB_NAME=postgres
```

## 3. Run Backfill (First-Time Setup)

Run the initial data loading process in terminal:

```bash
python -m scripts.run_financial_backfill

python -m scripts.run_stock_backfill
```


## 4. Start the ETL Scheduler

The scheduler runs the incremental ETL process periodically and updates the database.

Open a terminal and run:

```bash
python scheduler.py
```

## 5. Start the Dash Application

```bash
python app.py
```

The dashboard will be available at:

```text
http://127.0.0.1:8050/
```

---

# ☁️ Deployment

The application can be deployed using platforms that support Python web applications:

* Render
* Railway
* AWS Elastic Beanstalk
* Google Cloud Run
* Azure App Service
* Docker-based hosting

For production deployment:

```bash
gunicorn app:server
```

Database credentials should be configured using environment variables.

Example:

```env
DB_USER="your_user"
DB_PASSWORD="your_password"
DB_HOST="your_host"
DB_PORT="6543"
DB_NAME="postgres"
```

Sensitive credentials should never be committed to GitHub.

---

# 👤 Author

**Nurul Yakim Kazal**  
Lecturer, Department of Mathematics, Universitas Sam Ratulangi

Focus areas:

* Numerical Linear Algebra (academic)
* Data engineering & ETL systems
* Financial analytics dashboards
* Interactive data visualization
* Time-series analysis

---

# 🚀 Final Note

This project demonstrates an end-to-end financial analytics system that integrates database engineering, quantitative analysis, interactive Dash visualization, and automated reporting into a unified platform for exploring stock market behavior.
