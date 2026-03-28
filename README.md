# 📞 Contact Center Volume & Performance Forecasting
Develop a model to forecast intraday contact center metrics at the portfolio level. 
## 🎯 Objective
The model predicts the following targets in strict 30-minute intervals for August 2024:
- Call Volume (CV)
- Customer Care Time (CCT)
- Abandon Rate (ABD)
- The data contains 4 independent portfolios (A, B, C, D) of varied sizes.

## 🧠 Intuitions
Before modeling, we had several key intuitions:
- Approximately 90% of inbound call volume occurs between 9:00 AM and 9:00 PM EST, with "morning rushes" and "lunch dips."
- Volume is high on weekdays. Weekends have a decline, and major holidays (like Christmas/Thanksgiving) have minimal calls. (Note: There is no holidays in August)
- The four portfolios are independent. Larger portfolios have lower variance, while smaller portfolios (Portfolio D) are highly variant with many zero-volume intervals.
- Daily staffing directly impacts the Abandon Rate (ABD) and Service Level. But staffing does not impact Call Volume (CV).
- Outliers: Extreme values in Abandon Rate on 01/02/24.

## 🧹 Data Cleaning
### Step 1: Standardization
- All raw timestamps were strictly localized to US/Eastern to comply with project requirements and accurately capture daylight saving time shifts.
- The raw event logs were resampled into rigid 30-minute intervals (.resample('30min').asfreq()).

### Step 2: Missing Values & Outlier Handling
- Missing intervals for Call Volume and Abandoned Calls were filled with 0. If an interval was entirely unlogged, it is assumed the lines were closed or zero demand occurred.
- Missing intervals for CCT (Average Handle Time) and Service Level were imputed using linear interpolation. Filling these with zero would falsely signal to the model that agents resolved calls in 0 seconds, destroying moving averages. We connected the dots between known performance periods instead.
- To prevent extreme values from impacting the model, Abandoned Rate and CCT were capped at the 99th percentile of their respective portfolios.
