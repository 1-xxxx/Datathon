import pandas as pd
import numpy as np

def process_interval_data_from_excel(file, portfolio_name): # Filter and format the data in 30 minutes intervals
    sheet = f"{portfolio_name} - Interval"
    df = pd.read_excel(file, sheet)
    df = df.dropna(subset=['Month', 'Day', 'Interval'])
    
    df['Day'] = df['Day'].astype(int).astype(str)
    date_string = "2024 " + df['Month'].astype(str) + " " + df['Day'] + " " + df['Interval'].astype(str)
    
    df['datetime'] = pd.to_datetime(date_string, errors='coerce')
    df = df.dropna(subset=['datetime'])
    df['datetime'] = df['datetime'].dt.tz_localize('US/Eastern', ambiguous='NaT', nonexistent='shift_forward') # standardized in EDT (UTC - 4)
    
    df = df.set_index('datetime')
    df = df.drop(columns=['Month', 'Day', 'Interval'], errors='ignore')

    resampled = df.resample('30min').asfreq()
    resampled['Portfolio'] = portfolio_name # Make the portfolios as a column entry instead of a sheet label to make everything in one .csv
    return resampled


file = "Data for Datathon (Revised).xlsx" 
portfolios = ['A', 'B', 'C', 'D']
dfs = []

for p in portfolios:
    df = process_interval_data_from_excel(file, p)
    dfs.append(df)
        
cleaned = pd.concat(dfs)

cleaned = cleaned.dropna()

def outliers(series):
    limit = series.quantile(0.99)
    return np.where(series > limit, limit, series)
        
for col in ['Abandoned Rate', 'CCT']:
    cleaned[col] = cleaned.groupby('Portfolio')[col].transform(outliers)

output = "Cleaned_Intervals.csv"
cleaned.to_csv(output)
print("Cleaned")


