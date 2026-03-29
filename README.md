# Contact Center Volume & Performance Forecasting
Develop a model to forecast intraday contact center metrics at the portfolio level. 
## Objective
The model predicts the following targets in strict 30-minute intervals for August 2024:
- Call Volume (CV)
- Customer Care Time (CCT)
- Abandon Rate (ABD)
- The data contains 4 independent portfolios (A, B, C, D) of varied sizes.

## Intuitions
Before modeling, we had several key intuitions:
- Approximately 90% of inbound call volume occurs between 9:00 AM and 9:00 PM EST, with "morning rushes" and "lunch dips."
- Volume is high on weekdays. Weekends have a decline, and major holidays (like Christmas/Thanksgiving) have minimal calls. (Note: There is no holidays in August)
- The four portfolios are independent. Larger portfolios have lower variance, while smaller portfolios (Portfolio D) are highly variant with many zero-volume intervals.
- Daily staffing directly impacts the Abandon Rate (ABD) and Service Level. But staffing does not impact Call Volume (CV).
- Outliers: Extreme values in Abandon Rate on 01/02/24.

## Data Cleaning
### Step 1: Standardization
- All raw timestamps were strictly localized to US/Eastern to comply with project requirements and accurately capture daylight saving time shifts.
- The raw event logs were resampled into rigid 30-minute intervals (.resample('30min').asfreq()).

### Step 2: Missing Values & Outlier Handling
- Missing intervals for Call Volume and Abandoned Calls were filled with 0. If an interval was entirely unlogged, it is assumed the lines were closed or zero demand occurred.
- Missing intervals for CCT (Average Handle Time) and Service Level were imputed using linear interpolation. Filling these with zero would falsely signal to the model that agents resolved calls in 0 seconds, destroying moving averages. We connected the dots between known performance periods instead.
- To prevent extreme values from impacting the model, Abandoned Rate and CCT were capped at the 99th percentile of their respective portfolios.

## Core Architecture

### 1. The ML Baseline Engine (The `v04` Foundation)
All baseline predictions (like `v123`) are generated using our foundational `v04` XGBoost architecture. This base model was engineered with three critical strategies:
* **Isolated Portfolio Training:** It trains completely separate models for Portfolios A, B, C, and D, ensuring the algorithm never confuses the unique seasonal behaviors and volume scales of different business units.
* **Two-Stage Volume Prediction:** Instead of guessing raw numbers directly, it first predicts the *total daily call volume*, and then predicts the *interval share* (the % of calls arriving in each 30-minute window). 
* **Cyclical Time Features:** It translates timestamps into sine and cosine waves, allowing the XGBoost trees to mathematically understand repeating daily and seasonal time patterns.

### 2. Recent Historical Profiling (June Isolation)
Caller behavior drifts over time. Rather than taking an average of the entire year, the final script dynamically isolates historical data strictly from **June 2025**. By calculating the median call distribution for this recent period, we align the predicted intraday arrival shape with the most current caller trends.

### 3. Rolling Median Smoothing (Noise Reduction)
Raw historical data is inherently noisy. To prevent the model from overfitting to random historical spikes (e.g., a single 30-minute surge on a random Tuesday), the script applies a **Rolling Median Smooth** to the June profile. This mathematically "irons out" erratic intervals, ensuring a realistic staffing curve.

### 4. 50/50 Shape Blending
The script takes the base ML prediction's shape and blends it with the newly smoothed June historical shape at exactly a **50% / 50% weight**. This "wisdom of crowds" approach prevents extreme errors; the historical data keeps the ML grounded, while the ML accounts for new variables history can't foresee.

### 5. Final Portfolio Scalars
Finally, the pipeline applies targeted multipliers to correct known, persistent baseline under-predictions. 
* **Portfolio A:** Scaled by `1.04` (+4%)
* **Portfolio C:** Scaled by `1.02` (+2%)

## Execution
Ensure the base prediction (`forecast_v123.csv`) and history (`data/processed/interval_portfolio_clean.csv`) are present in the working directory.

Run the script to generate the final model:
```bash
python datathon_forecast_final.py
