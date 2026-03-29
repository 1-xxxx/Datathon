# Contact Center Volume & Performance Forecasting

We developed a portfolio-level forecasting pipeline for intraday contact center metrics in 30-minute intervals.

## Objective
Our goal was to predict the following targets for August 2024:

- Call Volume (CV)
- Customer Care Time (CCT)
- Abandon Rate (ABD)

The dataset contains four portfolios: **A, B, C, and D**, each with different traffic scales and variance patterns.

## Key Intuitions
Before modeling, we identified several operational patterns in the data:

- Most inbound call volume occurs during daytime hours, with clear intraday structure such as morning surges and midday dips.
- Weekdays have much higher traffic than weekends.
- The portfolios behave differently in both scale and volatility. Larger portfolios are more stable, while smaller portfolios, especially Portfolio D, contain more sparse and irregular intervals.
- Staffing affects performance-related metrics such as **Abandon Rate**, but does not directly drive inbound call volume.
- Some extreme values, especially in early-year abandonment-related fields, appeared to be outliers and required careful handling.

## Data Cleaning

### 1. Timestamp Standardization
- All timestamps were converted to **US/Eastern** time.
- Raw event logs were resampled into fixed **30-minute intervals** using a regular interval structure.

### 2. Missing Values
- Missing intervals for **Call Volume** and **Abandoned Calls** were filled with `0`.
- Missing intervals for **CCT** and service-related performance fields were imputed using **linear interpolation** to preserve continuity and avoid unrealistic zero values.

### 3. Outlier Handling
- Extreme values in **Abandon Rate** and **CCT** were capped at the **99th percentile** within each portfolio.

## Core Architecture

### 1. Baseline ML Engine
Our baseline forecasts were generated from an **XGBoost-based architecture**.

This base model used three main design choices:

- **Separate portfolio models:** each portfolio was modeled independently to preserve its own seasonal and variance structure.
- **Two-stage volume prediction:** the model first predicted **daily total volume**, then predicted the **intraday interval share** for each 30-minute period.
- **Cyclical time features:** timestamps were encoded using sine/cosine transformations so the model could capture repeating time-of-day and calendar patterns.

### 2. Recent Historical Profiling
To keep the final forecast aligned with more recent behavior, we built a recent historical intraday profile rather than relying on long-run averages. We used the median call distribution from a recent comparison window to estimate realistic interval-level shapes.

### 3. Rolling Median Smoothing
Historical interval shapes can be noisy. To reduce sensitivity to one-off spikes, we applied **rolling median smoothing** to the recent profile. This helped create a more stable and realistic intraday demand curve.

### 4. Final Portfolio Scalars
After generating the baseline shape, we applied small portfolio-level correction factors to address persistent bias:

- **Portfolio A:** `1.04`
- **Portfolio C:** `1.02`

These final scalars were used to correct underprediction observed during validation.

## Final Pipeline
The final workflow can be summarized as:

1. Clean and standardize the raw interval data
2. Train baseline XGBoost models by portfolio
3. Predict daily totals and intraday shares
4. Build a recent historical intraday profile
5. Smooth the profile with rolling medians
6. Blend model output with recent historical shape
7. Apply final portfolio-level correction scalars
8. Export the final August 2024 submission forecast

## Execution
Ensure the following files are available in the working directory:

- `forecast_v123.csv`
- `data/processed/interval_portfolio_clean.csv`

Run the final script:

```bash
python datathon_forecast_final.py
