"""
Data preprocessing utilities for Ulaanbaatar weather data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import ANALYSIS_CONFIG


def load_weather_data(filepath):
    """
    Load weather data from CSV file

    Parameters:
    -----------
    filepath : str or Path
        Path to the weather data CSV file

    Returns:
    --------
    pd.DataFrame
        Loaded weather data
    """
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    return df


def convert_datetime(df):
    """
    Convert dt_iso column to datetime and set as index

    Parameters:
    -----------
    df : pd.DataFrame
        Raw weather dataframe

    Returns:
    --------
    pd.DataFrame
        DataFrame with datetime index
    """
    print("Converting datetime...")
    df = df.copy()

    # Convert dt_iso to datetime
    df['datetime'] = pd.to_datetime(df['dt_iso'])

    # Set datetime as index
    df.set_index('datetime', inplace=True)

    # Sort by datetime
    df.sort_index(inplace=True)

    print(f"Date range: {df.index.min()} to {df.index.max()}")
    return df


def check_data_quality(df):
    """
    Check data quality and report issues

    Parameters:
    -----------
    df : pd.DataFrame
        Weather dataframe

    Returns:
    --------
    dict
        Dictionary with data quality metrics
    """
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)

    quality_report = {}

    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    print("\nMissing Values:")
    print("-" * 60)
    for col in missing[missing > 0].index:
        print(f"  {col}: {missing[col]:,} ({missing_pct[col]:.2f}%)")

    quality_report['missing_values'] = missing.to_dict()

    # Duplicates
    duplicates = df.index.duplicated().sum()
    print(f"\nDuplicate timestamps: {duplicates:,}")
    quality_report['duplicates'] = duplicates

    # Data range
    print(f"\nDate range: {df.index.min()} to {df.index.max()}")
    print(f"Total days: {(df.index.max() - df.index.min()).days:,}")
    quality_report['date_range'] = {
        'start': str(df.index.min()),
        'end': str(df.index.max()),
        'days': (df.index.max() - df.index.min()).days
    }

    # Temperature statistics
    if 'temp' in df.columns:
        print(f"\nTemperature (°C):")
        print(f"  Min: {df['temp'].min():.2f}°C")
        print(f"  Max: {df['temp'].max():.2f}°C")
        print(f"  Mean: {df['temp'].mean():.2f}°C")
        print(f"  Median: {df['temp'].median():.2f}°C")

        quality_report['temperature_stats'] = {
            'min': float(df['temp'].min()),
            'max': float(df['temp'].max()),
            'mean': float(df['temp'].mean()),
            'median': float(df['temp'].median())
        }

    print("="*60 + "\n")

    return quality_report


def handle_missing_values(df, method='interpolate'):
    """
    Handle missing values in the dataset

    Parameters:
    -----------
    df : pd.DataFrame
        Weather dataframe
    method : str
        Method to handle missing values ('interpolate', 'forward_fill', 'drop')

    Returns:
    --------
    pd.DataFrame
        DataFrame with handled missing values
    """
    print(f"Handling missing values using method: {method}")
    df = df.copy()

    # Columns that should be interpolated
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if method == 'interpolate':
        df[numeric_cols] = df[numeric_cols].interpolate(method='time', limit=24)
    elif method == 'forward_fill':
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill', limit=24)
    elif method == 'drop':
        df = df.dropna()

    remaining_missing = df.isnull().sum().sum()
    print(f"Remaining missing values: {remaining_missing:,}")

    return df


def detect_outliers(df, column='temp', method='iqr', threshold=3):
    """
    Detect outliers in specified column

    Parameters:
    -----------
    df : pd.DataFrame
        Weather dataframe
    column : str
        Column to check for outliers
    method : str
        Method to detect outliers ('iqr', 'zscore')
    threshold : float
        Threshold for outlier detection

    Returns:
    --------
    pd.Series
        Boolean series indicating outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        outliers = z_scores > threshold

    print(f"Detected {outliers.sum():,} outliers in '{column}' using {method} method")
    return outliers


def add_temporal_features(df):
    """
    Add temporal features (year, month, season, etc.)

    Parameters:
    -----------
    df : pd.DataFrame
        Weather dataframe with datetime index

    Returns:
    --------
    pd.DataFrame
        DataFrame with additional temporal features
    """
    print("Adding temporal features...")
    df = df.copy()

    # Extract temporal components
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['hour'] = df.index.hour
    df['day_of_year'] = df.index.dayofyear
    df['week_of_year'] = df.index.isocalendar().week

    # Add decade
    df['decade'] = (df['year'] // 10) * 10
    df['decade_label'] = df['decade'].astype(str) + 's'

    # Add season (Northern Hemisphere - Mongolia)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:  # [9, 10, 11]
            return 'Fall'

    df['season'] = df['month'].apply(get_season)

    # Add period of day
    def get_period_of_day(hour):
        if 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        elif 18 <= hour < 22:
            return 'Evening'
        else:
            return 'Night'

    df['period_of_day'] = df['hour'].apply(get_period_of_day)

    print(f"Added temporal features: year, month, day, hour, season, decade, etc.")
    return df


def aggregate_to_daily(df):
    """
    Aggregate hourly data to daily averages

    Parameters:
    -----------
    df : pd.DataFrame
        Hourly weather dataframe

    Returns:
    --------
    pd.DataFrame
        Daily aggregated dataframe
    """
    print("Aggregating to daily averages...")

    # Columns to aggregate - comprehensive list
    agg_dict = {
        # Temperature variables
        'temp': ['mean', 'min', 'max', 'std'],
        'feels_like': ['mean', 'min', 'max'],
        'temp_min': 'min',
        'temp_max': 'max',
        'dew_point': ['mean', 'min', 'max'],

        # Pressure variables
        'pressure': ['mean', 'min', 'max'],
        'sea_level': ['mean', 'min', 'max'],
        'grnd_level': ['mean', 'min', 'max'],

        # Humidity and visibility
        'humidity': ['mean', 'min', 'max'],
        'visibility': ['mean', 'min', 'max'],

        # Wind variables
        'wind_speed': ['mean', 'max'],
        'wind_deg': 'mean',
        'wind_gust': ['mean', 'max'],

        # Precipitation
        'rain_1h': 'sum',
        'rain_3h': 'sum',
        'snow_1h': 'sum',
        'snow_3h': 'sum',

        # Cloud coverage
        'clouds_all': 'mean',
    }

    # Remove columns that don't exist (handles optional columns gracefully)
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}

    daily = df.groupby(df.index.date).agg(agg_dict)

    # Flatten column names
    daily.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col
                     for col in daily.columns.values]

    # Convert index to datetime
    daily.index = pd.to_datetime(daily.index)

    print(f"Created daily dataset with {len(daily):,} rows")
    return daily


def aggregate_to_monthly(df):
    """
    Aggregate hourly data to monthly averages

    Parameters:
    -----------
    df : pd.DataFrame
        Hourly weather dataframe

    Returns:
    --------
    pd.DataFrame
        Monthly aggregated dataframe
    """
    print("Aggregating to monthly averages...")

    # Columns to aggregate - comprehensive list
    agg_dict = {
        # Temperature variables
        'temp': ['mean', 'min', 'max', 'std'],
        'feels_like': ['mean', 'min', 'max'],
        'temp_min': 'min',
        'temp_max': 'max',
        'dew_point': ['mean', 'min', 'max'],

        # Pressure variables
        'pressure': ['mean', 'min', 'max'],
        'sea_level': ['mean', 'min', 'max'],
        'grnd_level': ['mean', 'min', 'max'],

        # Humidity and visibility
        'humidity': ['mean', 'min', 'max'],
        'visibility': ['mean', 'min', 'max'],

        # Wind variables
        'wind_speed': ['mean', 'max'],
        'wind_deg': 'mean',
        'wind_gust': ['mean', 'max'],

        # Precipitation
        'rain_1h': 'sum',
        'rain_3h': 'sum',
        'snow_1h': 'sum',
        'snow_3h': 'sum',

        # Cloud coverage
        'clouds_all': 'mean',
    }

    # Remove columns that don't exist (handles optional columns gracefully)
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}

    monthly = df.groupby(pd.Grouper(freq='M')).agg(agg_dict)

    # Flatten column names
    monthly.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col
                       for col in monthly.columns.values]

    print(f"Created monthly dataset with {len(monthly):,} rows")
    return monthly


def aggregate_to_yearly(df):
    """
    Aggregate hourly data to yearly averages

    Parameters:
    -----------
    df : pd.DataFrame
        Hourly weather dataframe

    Returns:
    --------
    pd.DataFrame
        Yearly aggregated dataframe
    """
    print("Aggregating to yearly averages...")

    # Columns to aggregate - comprehensive list
    agg_dict = {
        # Temperature variables
        'temp': ['mean', 'min', 'max', 'std'],
        'feels_like': ['mean', 'min', 'max'],
        'temp_min': 'min',
        'temp_max': 'max',
        'dew_point': ['mean', 'min', 'max'],

        # Pressure variables
        'pressure': ['mean', 'min', 'max'],
        'sea_level': ['mean', 'min', 'max'],
        'grnd_level': ['mean', 'min', 'max'],

        # Humidity and visibility
        'humidity': ['mean', 'min', 'max'],
        'visibility': ['mean', 'min', 'max'],

        # Wind variables
        'wind_speed': ['mean', 'max'],
        'wind_deg': 'mean',
        'wind_gust': ['mean', 'max'],

        # Precipitation
        'rain_1h': 'sum',
        'rain_3h': 'sum',
        'snow_1h': 'sum',
        'snow_3h': 'sum',

        # Cloud coverage
        'clouds_all': 'mean',
    }

    # Remove columns that don't exist (handles optional columns gracefully)
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}

    yearly = df.groupby(pd.Grouper(freq='Y')).agg(agg_dict)

    # Flatten column names
    yearly.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col
                      for col in yearly.columns.values]

    # Add year column
    yearly['year'] = yearly.index.year

    print(f"Created yearly dataset with {len(yearly):,} rows")
    return yearly


def preprocess_pipeline(filepath, save_processed=True):
    """
    Complete preprocessing pipeline

    Parameters:
    -----------
    filepath : str or Path
        Path to raw weather data
    save_processed : bool
        Whether to save processed data

    Returns:
    --------
    dict
        Dictionary containing all processed dataframes
    """
    print("\n" + "="*60)
    print("STARTING DATA PREPROCESSING PIPELINE")
    print("="*60 + "\n")

    # Load data
    df = load_weather_data(filepath)

    # Convert datetime
    df = convert_datetime(df)

    # Check quality
    quality_report = check_data_quality(df)

    # Handle missing values
    df = handle_missing_values(df, method='interpolate')

    # Add temporal features
    df = add_temporal_features(df)

    # Create aggregated datasets
    daily = aggregate_to_daily(df)
    monthly = aggregate_to_monthly(df)
    yearly = aggregate_to_yearly(df)

    # Save processed data
    if save_processed:
        from config.config import PROCESSED_DATA_DIR

        print("\nSaving processed data...")
        df.to_csv(PROCESSED_DATA_DIR / 'hourly_processed.csv')
        daily.to_csv(PROCESSED_DATA_DIR / 'daily_aggregated.csv')
        monthly.to_csv(PROCESSED_DATA_DIR / 'monthly_aggregated.csv')
        yearly.to_csv(PROCESSED_DATA_DIR / 'yearly_aggregated.csv')

        # Save quality report
        import json
        with open(PROCESSED_DATA_DIR / 'quality_report.json', 'w') as f:
            json.dump(quality_report, f, indent=2)

        print(f"Saved processed data to {PROCESSED_DATA_DIR}")

    print("\n" + "="*60)
    print("PREPROCESSING COMPLETE")
    print("="*60 + "\n")

    return {
        'hourly': df,
        'daily': daily,
        'monthly': monthly,
        'yearly': yearly,
        'quality_report': quality_report
    }
