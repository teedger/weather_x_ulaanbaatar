"""
Configuration file for Mongolia Weather Analysis Project
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# Results directories
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
REPORTS_DIR = RESULTS_DIR / "reports"
STATISTICS_DIR = RESULTS_DIR / "statistics"

# Data file paths
WEATHER_DATA_FILE = RAW_DATA_DIR / "ulaanbaatar_weather_1990_2024.csv"

# Expected data columns (OpenWeather format)
DATA_COLUMNS = {
    # Time and location
    'dt': 'Unix timestamp',
    'dt_iso': 'ISO datetime (e.g., 1990-11-25 00:00:00 +0000 UTC)',
    'timezone': 'Timezone offset in seconds',
    'city_name': 'City name',
    'lat': 'Latitude',
    'lon': 'Longitude',

    # Temperature variables (°C)
    'temp': 'Temperature',
    'feels_like': 'Feels like temperature',
    'temp_min': 'Minimum temperature',
    'temp_max': 'Maximum temperature',
    'dew_point': 'Dew point temperature',

    # Pressure variables (hPa)
    'pressure': 'Atmospheric pressure',
    'sea_level': 'Atmospheric pressure at sea level (optional)',
    'grnd_level': 'Atmospheric pressure at ground level (optional)',

    # Other meteorological variables
    'humidity': 'Relative humidity (%)',
    'visibility': 'Visibility (meters)',
    'clouds_all': 'Cloud coverage (%)',

    # Wind variables
    'wind_speed': 'Wind speed (m/s)',
    'wind_deg': 'Wind direction (degrees)',
    'wind_gust': 'Wind gust speed (m/s, optional)',

    # Precipitation variables (optional)
    'rain_1h': 'Rain volume for last hour (mm)',
    'rain_3h': 'Rain volume for last 3 hours (mm)',
    'snow_1h': 'Snow volume for last hour (mm)',
    'snow_3h': 'Snow volume for last 3 hours (mm)',

    # Weather condition
    'weather_id': 'Weather condition ID',
    'weather_main': 'Weather condition main category',
    'weather_description': 'Weather condition description',
    'weather_icon': 'Weather icon code',
}

# Analysis parameters
ANALYSIS_CONFIG = {
    "start_year": 1990,
    "end_year": 2024,
    "city_name": "Ulaanbaatar",
    "timezone": "Asia/Ulaanbaatar",

    # Temperature analysis
    "temp_column": "temp",
    "feels_like_column": "feels_like",

    # Aggregation periods
    "aggregation_periods": ["daily", "monthly", "seasonal", "yearly"],

    # Seasonal definitions (Northern Hemisphere - Mongolia)
    "seasons": {
        "Winter": [12, 1, 2],
        "Spring": [3, 4, 5],
        "Summer": [6, 7, 8],
        "Fall": [9, 10, 11]
    },

    # Trend analysis
    "moving_average_windows": [30, 365, 1825],  # 30 days, 1 year, 5 years (in days)

    # Cyclical analysis
    "fourier_analysis": {
        "max_periods": 10,  # Number of top periods to identify
    },

    # Statistical tests
    "significance_level": 0.05,

    # Visualization
    "figure_dpi": 300,
    "figure_format": "png",
}

# External data sources (URLs for reference)
EXTERNAL_DATA_SOURCES = {
    "global_temperature": {
        "NASA_GISTEMP": "https://data.giss.nasa.gov/gistemp/",
        "NOAA": "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series",
        "Berkeley_Earth": "http://berkeleyearth.org/data/",
    },
    "population": {
        "World_Bank": "https://data.worldbank.org/indicator/SP.POP.TOTL",
        "UN_Data": "https://population.un.org/wpp/Download/Standard/CSV/",
    },
    "emissions": {
        "Global_Carbon_Project": "https://globalcarbonbudget.org/",
        "EDGAR": "https://edgar.jrc.ec.europa.eu/",
    },
    "economic_russia_china": {
        "World_Bank": "https://data.worldbank.org/country",
        "IMF": "https://www.imf.org/en/Data",
    }
}

# Color schemes for visualization
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8",
    "decades": {
        "1990s": "#8c564b",
        "2000s": "#e377c2",
        "2010s": "#7f7f7f",
        "2020s": "#bcbd22",
    },
    "seasons": {
        "Winter": "#3498db",
        "Spring": "#2ecc71",
        "Summer": "#f39c12",
        "Fall": "#e74c3c",
    }
}

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR,
                  FIGURES_DIR, REPORTS_DIR, STATISTICS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
