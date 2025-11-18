"""
Correlation analysis module
Analyze relationships between weather data and external factors
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


def calculate_correlation_matrix(df, columns=None, method='pearson'):
    """
    Calculate correlation matrix for selected columns

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with variables
    columns : list
        List of columns to include (None for all numeric)
    method : str
        Correlation method ('pearson', 'spearman', 'kendall')

    Returns:
    --------
    pd.DataFrame
        Correlation matrix
    """
    print(f"Calculating {method} correlation matrix...")

    if columns is None:
        # Use all numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
    else:
        numeric_df = df[columns]

    corr_matrix = numeric_df.corr(method=method)

    print(f"  Matrix size: {corr_matrix.shape[0]}x{corr_matrix.shape[1]}")

    return corr_matrix


def calculate_pairwise_correlation(df, col1, col2, method='pearson'):
    """
    Calculate correlation between two variables with significance test

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe
    col1, col2 : str
        Column names
    method : str
        Correlation method

    Returns:
    --------
    dict
        Correlation coefficient, p-value, and interpretation
    """
    # Remove rows with NaN in either column
    data = df[[col1, col2]].dropna()

    if method == 'pearson':
        corr, p_value = stats.pearsonr(data[col1], data[col2])
    elif method == 'spearman':
        corr, p_value = stats.spearmanr(data[col1], data[col2])
    elif method == 'kendall':
        corr, p_value = stats.kendalltau(data[col1], data[col2])

    # Interpretation
    abs_corr = abs(corr)
    if abs_corr < 0.3:
        strength = "weak"
    elif abs_corr < 0.7:
        strength = "moderate"
    else:
        strength = "strong"

    direction = "positive" if corr > 0 else "negative"

    result = {
        'correlation': corr,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'strength': strength,
        'direction': direction,
        'n_samples': len(data),
        'interpretation': f"{strength} {direction} correlation"
    }

    print(f"\nCorrelation between {col1} and {col2}:")
    print(f"  Method: {method}")
    print(f"  Correlation: {corr:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Significant (α=0.05): {result['significant']}")
    print(f"  Interpretation: {result['interpretation']}")

    return result


def calculate_cross_correlation(series1, series2, max_lag=12):
    """
    Calculate cross-correlation between two time series with lags

    Parameters:
    -----------
    series1, series2 : pd.Series
        Time series data
    max_lag : int
        Maximum lag to test

    Returns:
    --------
    dict
        Cross-correlation values and best lag
    """
    print(f"Calculating cross-correlation (max lag: {max_lag})...")

    # Align series
    aligned = pd.DataFrame({'s1': series1, 's2': series2}).dropna()

    # Standardize
    s1_std = (aligned['s1'] - aligned['s1'].mean()) / aligned['s1'].std()
    s2_std = (aligned['s2'] - aligned['s2'].mean()) / aligned['s2'].std()

    # Calculate cross-correlation for different lags
    lags = range(-max_lag, max_lag + 1)
    correlations = []

    for lag in lags:
        if lag < 0:
            corr = np.corrcoef(s1_std[:lag], s2_std[-lag:])[0, 1]
        elif lag > 0:
            corr = np.corrcoef(s1_std[lag:], s2_std[:-lag])[0, 1]
        else:
            corr = np.corrcoef(s1_std, s2_std)[0, 1]

        correlations.append(corr)

    correlations = np.array(correlations)

    # Find best lag
    best_lag_idx = np.argmax(np.abs(correlations))
    best_lag = lags[best_lag_idx]
    best_corr = correlations[best_lag_idx]

    result = {
        'lags': list(lags),
        'correlations': list(correlations),
        'best_lag': best_lag,
        'best_correlation': best_corr
    }

    print(f"  Best lag: {best_lag}")
    print(f"  Correlation at best lag: {best_corr:.4f}")

    return result


def merge_external_data(weather_df, external_df, on='year', how='left'):
    """
    Merge weather data with external data (e.g., global temperature, GDP)

    Parameters:
    -----------
    weather_df : pd.DataFrame
        Weather dataframe
    external_df : pd.DataFrame
        External data (e.g., global temp, emissions)
    on : str
        Column to merge on
    how : str
        Merge method

    Returns:
    --------
    pd.DataFrame
        Merged dataframe
    """
    print(f"Merging weather data with external data on '{on}'...")

    # Ensure merge column exists
    if on == 'year' and on not in weather_df.columns:
        if isinstance(weather_df.index, pd.DatetimeIndex):
            weather_df = weather_df.copy()
            weather_df['year'] = weather_df.index.year

    merged = pd.merge(weather_df, external_df, on=on, how=how)

    print(f"  Weather data rows: {len(weather_df)}")
    print(f"  External data rows: {len(external_df)}")
    print(f"  Merged rows: {len(merged)}")

    return merged


def analyze_global_temperature_correlation(ulaanbaatar_df, global_df,
                                           ub_col='temp_mean', global_col='global_temp'):
    """
    Analyze correlation between Ulaanbaatar and global temperature

    Parameters:
    -----------
    ulaanbaatar_df : pd.DataFrame
        Ulaanbaatar temperature data
    global_df : pd.DataFrame
        Global temperature data
    ub_col : str
        Ulaanbaatar temperature column
    global_col : str
        Global temperature column

    Returns:
    --------
    dict
        Correlation analysis results
    """
    print("="*60)
    print("ULAANBAATAR vs GLOBAL TEMPERATURE CORRELATION ANALYSIS")
    print("="*60)

    # Merge data
    merged = merge_external_data(ulaanbaatar_df, global_df, on='year')

    if global_col not in merged.columns:
        print(f"  Error: '{global_col}' not found in merged data")
        return None

    # Calculate correlation
    corr_result = calculate_pairwise_correlation(merged, ub_col, global_col, method='pearson')

    # Calculate warming rates
    ub_trend = calculate_trend_rate(ulaanbaatar_df, ub_col)
    global_trend = calculate_trend_rate(global_df, global_col)

    result = {
        'correlation': corr_result,
        'ub_warming_rate': ub_trend,
        'global_warming_rate': global_trend,
        'merged_data': merged
    }

    print(f"\nWarming Rates:")
    print(f"  Ulaanbaatar: {ub_trend['rate_per_decade']:.4f}°C/decade")
    print(f"  Global: {global_trend['rate_per_decade']:.4f}°C/decade")
    print(f"  Ratio (UB/Global): {ub_trend['rate_per_decade']/global_trend['rate_per_decade']:.2f}x")

    return result


def calculate_trend_rate(df, column, decade_multiplier=10):
    """
    Calculate warming/cooling rate per decade

    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    column : str
        Column to analyze
    decade_multiplier : int
        Multiplier for rate (10 for per decade)

    Returns:
    --------
    dict
        Trend rate statistics
    """
    from src.analysis.temporal_analysis import calculate_trend

    data = df[[column]].dropna()

    # Assume daily data, calculate days per decade
    total_days = len(data)
    trend = calculate_trend(data, column=column, method='linear')

    # Calculate rate per decade
    # slope is per day, multiply by days in a decade
    days_per_decade = 365.25 * decade_multiplier
    rate_per_decade = trend['slope'] * days_per_decade

    return {
        'slope': trend['slope'],
        'rate_per_decade': rate_per_decade,
        'r_squared': trend['r_squared'],
        'p_value': trend['p_value']
    }


def analyze_population_correlation(weather_df, population_df,
                                   temp_col='temp_mean', pop_col='population'):
    """
    Analyze correlation between temperature and population

    Parameters:
    -----------
    weather_df : pd.DataFrame
        Weather data
    population_df : pd.DataFrame
        Population data
    temp_col : str
        Temperature column
    pop_col : str
        Population column

    Returns:
    --------
    dict
        Correlation results
    """
    print("="*60)
    print("TEMPERATURE vs POPULATION CORRELATION ANALYSIS")
    print("="*60)

    # Merge data
    merged = merge_external_data(weather_df, population_df, on='year')

    if pop_col not in merged.columns:
        print(f"  Error: '{pop_col}' not found in merged data")
        return None

    # Calculate correlations
    pearson = calculate_pairwise_correlation(merged, temp_col, pop_col, method='pearson')
    spearman = calculate_pairwise_correlation(merged, temp_col, pop_col, method='spearman')

    result = {
        'pearson': pearson,
        'spearman': spearman,
        'merged_data': merged
    }

    return result


def analyze_economic_correlation(weather_df, economic_df,
                                 temp_col='temp_mean', econ_cols=['gdp', 'emissions']):
    """
    Analyze correlation between temperature and economic indicators

    Parameters:
    -----------
    weather_df : pd.DataFrame
        Weather data
    economic_df : pd.DataFrame
        Economic data (GDP, emissions, etc.)
    temp_col : str
        Temperature column
    econ_cols : list
        Economic indicator columns

    Returns:
    --------
    dict
        Correlation results for each indicator
    """
    print("="*60)
    print("TEMPERATURE vs ECONOMIC INDICATORS CORRELATION ANALYSIS")
    print("="*60)

    # Merge data
    merged = merge_external_data(weather_df, economic_df, on='year')

    results = {}

    for econ_col in econ_cols:
        if econ_col in merged.columns:
            print(f"\nAnalyzing: {econ_col}")
            corr = calculate_pairwise_correlation(merged, temp_col, econ_col, method='pearson')
            cross_corr = calculate_cross_correlation(merged[temp_col], merged[econ_col], max_lag=5)

            results[econ_col] = {
                'correlation': corr,
                'cross_correlation': cross_corr
            }
        else:
            print(f"  Warning: '{econ_col}' not found in data")

    results['merged_data'] = merged

    return results


def granger_causality_test(df, col1, col2, max_lag=5):
    """
    Perform Granger causality test

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with both variables
    col1, col2 : str
        Column names (test if col1 Granger-causes col2)
    max_lag : int
        Maximum lag to test

    Returns:
    --------
    dict
        Test results
    """
    from statsmodels.tsa.stattools import grangercausalitytests

    print(f"Performing Granger causality test: Does {col1} cause {col2}?")

    # Prepare data
    data = df[[col2, col1]].dropna()

    try:
        # Perform test
        results = grangercausalitytests(data, max_lag, verbose=False)

        # Extract p-values
        p_values = []
        for lag in range(1, max_lag + 1):
            p_value = results[lag][0]['ssr_ftest'][1]
            p_values.append(p_value)

        # Check if significant at any lag
        min_p_value = min(p_values)
        significant = min_p_value < 0.05

        result = {
            'p_values': p_values,
            'min_p_value': min_p_value,
            'significant': significant,
            'best_lag': p_values.index(min_p_value) + 1
        }

        print(f"  Min p-value: {min_p_value:.6f} at lag {result['best_lag']}")
        print(f"  Granger-causes: {significant}")

        return result

    except Exception as e:
        print(f"  Error in Granger causality test: {e}")
        return None


def partial_correlation(df, x, y, z):
    """
    Calculate partial correlation between x and y controlling for z

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe
    x, y, z : str
        Variable names

    Returns:
    --------
    float
        Partial correlation coefficient
    """
    print(f"Calculating partial correlation: {x} and {y} controlling for {z}")

    # Remove NaN
    data = df[[x, y, z]].dropna()

    # Calculate correlations
    rxy = data[x].corr(data[y])
    rxz = data[x].corr(data[z])
    ryz = data[y].corr(data[z])

    # Calculate partial correlation
    partial_corr = (rxy - rxz * ryz) / (np.sqrt(1 - rxz**2) * np.sqrt(1 - ryz**2))

    print(f"  Partial correlation: {partial_corr:.4f}")
    print(f"  Zero-order correlation (without control): {rxy:.4f}")

    return partial_corr


def create_correlation_summary(weather_df, external_data_dict):
    """
    Create comprehensive correlation summary with all external factors

    Parameters:
    -----------
    weather_df : pd.DataFrame
        Weather data
    external_data_dict : dict
        Dictionary of external dataframes {'name': df}

    Returns:
    --------
    pd.DataFrame
        Summary of all correlations
    """
    print("="*60)
    print("COMPREHENSIVE CORRELATION SUMMARY")
    print("="*60)

    summary_rows = []

    for name, ext_df in external_data_dict.items():
        print(f"\nProcessing: {name}")

        # Merge with weather data
        merged = merge_external_data(weather_df, ext_df, on='year')

        # Get numeric columns from external data
        ext_cols = ext_df.select_dtypes(include=[np.number]).columns

        for col in ext_cols:
            if col in merged.columns and col != 'year':
                try:
                    corr = calculate_pairwise_correlation(
                        merged, 'temp_mean', col, method='pearson'
                    )

                    summary_rows.append({
                        'external_factor': name,
                        'variable': col,
                        'correlation': corr['correlation'],
                        'p_value': corr['p_value'],
                        'significant': corr['significant'],
                        'strength': corr['strength'],
                        'direction': corr['direction']
                    })
                except Exception as e:
                    print(f"  Error with {col}: {e}")

    summary_df = pd.DataFrame(summary_rows)

    # Sort by absolute correlation
    summary_df['abs_correlation'] = summary_df['correlation'].abs()
    summary_df = summary_df.sort_values('abs_correlation', ascending=False)

    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    print(summary_df[['external_factor', 'variable', 'correlation',
                     'p_value', 'significant']].to_string())

    return summary_df
