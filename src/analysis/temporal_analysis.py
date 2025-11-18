"""
Temporal analysis module for weather data
Includes trend detection, cyclical patterns, and time series decomposition
"""
import pandas as pd
import numpy as np
from scipy import stats, signal
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf
import warnings
warnings.filterwarnings('ignore')


def calculate_trend(df, column='temp_mean', method='linear'):
    """
    Calculate trend in temperature data

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to analyze
    method : str
        Trend calculation method ('linear', 'polynomial')

    Returns:
    --------
    dict
        Trend statistics including slope, intercept, r-value, p-value
    """
    print(f"Calculating {method} trend for {column}...")

    # Remove NaN values
    data = df[[column]].dropna()

    # Create numeric index (days since start)
    x = np.arange(len(data))
    y = data[column].values

    if method == 'linear':
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # Calculate trend line
        trend_line = slope * x + intercept

        result = {
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'std_err': std_err,
            'trend_line': trend_line,
            'x': x,
            'y': y
        }

        # Calculate change over period
        total_change = slope * len(data)
        result['total_change'] = total_change

        print(f"  Slope: {slope:.6f} per time unit")
        print(f"  R²: {r_value**2:.4f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"  Total change: {total_change:.2f}°C")

        return result

    elif method == 'polynomial':
        # Fit 2nd degree polynomial
        coefficients = np.polyfit(x, y, 2)
        trend_line = np.polyval(coefficients, x)

        # Calculate R²
        ss_res = np.sum((y - trend_line) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        result = {
            'coefficients': coefficients,
            'trend_line': trend_line,
            'r_squared': r_squared,
            'x': x,
            'y': y
        }

        print(f"  R²: {r_squared:.4f}")
        return result


def mann_kendall_test(df, column='temp_mean'):
    """
    Perform Mann-Kendall test for trend significance

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to test

    Returns:
    --------
    dict
        Test results
    """
    print(f"Performing Mann-Kendall test for {column}...")

    data = df[column].dropna().values
    n = len(data)

    # Calculate S statistic
    S = 0
    for i in range(n-1):
        for j in range(i+1, n):
            S += np.sign(data[j] - data[i])

    # Calculate variance
    var_S = n * (n - 1) * (2 * n + 5) / 18

    # Calculate Z statistic
    if S > 0:
        Z = (S - 1) / np.sqrt(var_S)
    elif S < 0:
        Z = (S + 1) / np.sqrt(var_S)
    else:
        Z = 0

    # Calculate p-value (two-tailed test)
    p_value = 2 * (1 - stats.norm.cdf(abs(Z)))

    result = {
        'S': S,
        'Z': Z,
        'p_value': p_value,
        'trend': 'increasing' if S > 0 else 'decreasing' if S < 0 else 'no trend',
        'significant': p_value < 0.05
    }

    print(f"  S: {S}")
    print(f"  Z: {Z:.4f}")
    print(f"  p-value: {p_value:.6f}")
    print(f"  Trend: {result['trend']}")
    print(f"  Significant (α=0.05): {result['significant']}")

    return result


def calculate_moving_averages(df, column='temp_mean', windows=[30, 365, 1825]):
    """
    Calculate moving averages for different windows

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to calculate moving averages for
    windows : list
        List of window sizes (in days)

    Returns:
    --------
    pd.DataFrame
        DataFrame with moving averages
    """
    print(f"Calculating moving averages for {column}...")

    result_df = df[[column]].copy()

    for window in windows:
        col_name = f'{column}_ma_{window}d'
        result_df[col_name] = result_df[column].rolling(window=window, center=True).mean()
        print(f"  Added {window}-day moving average")

    return result_df


def decompose_time_series(df, column='temp_mean', model='additive', period=365):
    """
    Decompose time series into trend, seasonal, and residual components

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to decompose
    model : str
        'additive' or 'multiplicative'
    period : int
        Seasonal period (365 for yearly)

    Returns:
    --------
    statsmodels.tsa.seasonal.DecomposeResult
        Decomposition result
    """
    print(f"Decomposing time series for {column}...")

    # Remove NaN values
    data = df[column].dropna()

    # Perform decomposition
    decomposition = seasonal_decompose(data, model=model, period=period, extrapolate_trend='freq')

    print(f"  Model: {model}")
    print(f"  Period: {period}")
    print("  Components: trend, seasonal, residual")

    return decomposition


def detect_cyclical_patterns(df, column='temp_mean', method='fft'):
    """
    Detect cyclical patterns using Fourier analysis

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to analyze
    method : str
        Method to use ('fft' for Fast Fourier Transform)

    Returns:
    --------
    dict
        Detected periods and their strengths
    """
    print(f"Detecting cyclical patterns in {column}...")

    # Remove NaN values and detrend
    data = df[column].dropna()
    detrended = signal.detrend(data.values)

    if method == 'fft':
        # Perform FFT
        fft_values = np.fft.fft(detrended)
        fft_freq = np.fft.fftfreq(len(detrended))

        # Get power spectrum
        power = np.abs(fft_values) ** 2

        # Find peaks (exclude DC component)
        positive_freq_idx = fft_freq > 0
        freq = fft_freq[positive_freq_idx]
        power = power[positive_freq_idx]

        # Find top peaks
        peaks_idx = signal.find_peaks(power, height=np.percentile(power, 95))[0]

        # Convert frequency to period (in data points)
        periods = []
        for idx in peaks_idx:
            if freq[idx] != 0:
                period = 1 / freq[idx]
                periods.append({
                    'period_points': period,
                    'period_days': period,  # Assuming daily data
                    'power': power[idx],
                    'frequency': freq[idx]
                })

        # Sort by power
        periods = sorted(periods, key=lambda x: x['power'], reverse=True)

        print(f"  Detected {len(periods)} significant cyclical patterns")
        for i, p in enumerate(periods[:5], 1):
            print(f"    {i}. Period: {p['period_days']:.1f} days (Power: {p['power']:.2e})")

        return {
            'periods': periods,
            'frequencies': freq,
            'power_spectrum': power
        }


def calculate_autocorrelation(df, column='temp_mean', nlags=365):
    """
    Calculate autocorrelation function

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Column to analyze
    nlags : int
        Number of lags

    Returns:
    --------
    dict
        ACF and PACF values
    """
    print(f"Calculating autocorrelation for {column}...")

    data = df[column].dropna()

    # Calculate ACF and PACF
    acf_values = acf(data, nlags=nlags, fft=True)
    pacf_values = pacf(data, nlags=nlags)

    result = {
        'acf': acf_values,
        'pacf': pacf_values,
        'lags': np.arange(nlags + 1)
    }

    print(f"  Calculated ACF and PACF for {nlags} lags")

    return result


def analyze_temperature_by_period(df, column='temp_mean', groupby='decade'):
    """
    Analyze temperature statistics by time period

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with temporal features
    column : str
        Temperature column to analyze
    groupby : str
        Column to group by ('decade', 'year', 'season')

    Returns:
    --------
    pd.DataFrame
        Statistics by period
    """
    print(f"Analyzing {column} by {groupby}...")

    if groupby not in df.columns:
        print(f"  Warning: '{groupby}' column not found")
        return None

    stats_df = df.groupby(groupby)[column].agg([
        'count', 'mean', 'std', 'min', 'max',
        ('q25', lambda x: x.quantile(0.25)),
        ('q75', lambda x: x.quantile(0.75))
    ]).round(2)

    print(f"\n{stats_df}")

    return stats_df


def calculate_temperature_anomalies(df, column='temp_mean', baseline_period=None):
    """
    Calculate temperature anomalies relative to baseline period

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Temperature column
    baseline_period : tuple
        (start_year, end_year) for baseline, or None for full period

    Returns:
    --------
    pd.DataFrame
        DataFrame with anomalies
    """
    print(f"Calculating temperature anomalies for {column}...")

    result_df = df.copy()

    if baseline_period:
        start_year, end_year = baseline_period
        baseline_data = df[(df.index.year >= start_year) & (df.index.year <= end_year)]
        print(f"  Baseline period: {start_year}-{end_year}")
    else:
        baseline_data = df
        print(f"  Baseline period: entire dataset")

    baseline_mean = baseline_data[column].mean()
    print(f"  Baseline mean: {baseline_mean:.2f}°C")

    result_df[f'{column}_anomaly'] = result_df[column] - baseline_mean

    return result_df


def detect_extreme_events(df, column='temp_mean', threshold_percentile=95):
    """
    Detect extreme temperature events

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Temperature column
    threshold_percentile : float
        Percentile threshold for extremes

    Returns:
    --------
    dict
        Extreme events statistics
    """
    print(f"Detecting extreme events in {column}...")

    data = df[column].dropna()

    # Calculate thresholds
    high_threshold = data.quantile(threshold_percentile / 100)
    low_threshold = data.quantile((100 - threshold_percentile) / 100)

    # Detect events
    hot_events = df[df[column] > high_threshold]
    cold_events = df[df[column] < low_threshold]

    result = {
        'high_threshold': high_threshold,
        'low_threshold': low_threshold,
        'hot_events_count': len(hot_events),
        'cold_events_count': len(cold_events),
        'hot_events': hot_events,
        'cold_events': cold_events
    }

    print(f"  High threshold (P{threshold_percentile}): {high_threshold:.2f}°C")
    print(f"  Low threshold (P{100-threshold_percentile}): {low_threshold:.2f}°C")
    print(f"  Hot events: {len(hot_events)}")
    print(f"  Cold events: {len(cold_events)}")

    return result


def analyze_seasonal_trends(df, temp_column='temp_mean'):
    """
    Analyze temperature trends by season

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with season column
    temp_column : str
        Temperature column to analyze

    Returns:
    --------
    dict
        Trends for each season
    """
    print(f"Analyzing seasonal trends in {temp_column}...")

    if 'season' not in df.columns:
        print("  Warning: 'season' column not found")
        return None

    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_trends = {}

    for season in seasons:
        season_data = df[df['season'] == season].copy()

        if len(season_data) > 0:
            trend = calculate_trend(season_data, column=temp_column, method='linear')
            seasonal_trends[season] = trend

    return seasonal_trends
