# 📞 Contact Center Volume & Performance Forecasting
Develop a model to forecast intraday contact center metrics at the portfolio level. 
## 🎯 Objective Parameters
The model predicts the following targets in strict 30-minute intervals for August 2024:
- Call Volume (CV)
- Customer Care Time (CCT)
- Abandon Rate (ABD)
- The data encompasses 4 independent portfolios (A, B, C, D) of varying sizes within the Diversified & Value platform.

## 🧠 Core Intuitions & Business Logic
Before modeling, we established several key assumptions based on the exploratory data analysis and contact center operational realities:
- Demand is highly cyclical. Approximately 90% of inbound call volume occurs between 9:00 AM and 9:00 PM EST, with distinct "morning rushes" and "lunch dips."
- Volume is heavily concentrated on weekdays. Weekends see a steep drop-off, and major holidays (like Christmas/Thanksgiving) see near-zero volume. (Note: There is no holidays in August, holiday's data must be treated carefully so they do not skew standard weekday predictions.)
- The four portfolios are independent. Portfolio size influences variance: larger portfolios have predictable volume curves, while smaller portfolios (Portfolio D) are highly variant with frequent zero-volume intervals.
- Daily scheduled staffing directly impacts the Abandon Rate (ABD) and Service Level. However, staffing does not impact inbound Call Volume (CV), as customer demand is independent of center capacity.
- Outliers: Extreme values in Abandon Rate (e.g., 01/02/24) represent mismatches between demand and staffing rather than systemic trends.

## 🧹 Data Processing & Cleaning Pipeline
To ensure continuous, mathematically sound time-series data, we executed a two-phase data preparation pipeline.
### Phase 1: Standardization
- All raw timestamps were strictly localized to US/Eastern to comply with project requirements and accurately capture daylight saving time shifts.
- The raw event logs were resampled into rigid 30-minute intervals (.resample('30min').asfreq()).

### Phase 2: Smart Imputation & Outlier Handling
- Missing intervals for Call Volume and Abandoned Calls were filled with 0. If an interval was entirely unlogged, it is assumed the lines were closed or zero demand occurred.
- Missing intervals for CCT (Average Handle Time) and Service Level were imputed using linear interpolation. Filling these with zero would falsely signal to the model that agents resolved calls in 0 seconds, destroying moving averages. We connected the dots between known performance periods instead.
- To prevent extreme values from impacting the model, Abandoned Rate and CCT were capped at the 99th percentile of their respective portfolios.
