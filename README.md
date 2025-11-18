# Ulaanbaatar Weather Analysis Project (1990-2024)

A comprehensive analysis of climate change patterns in Ulaanbaatar, Mongolia, examining temperature trends, cyclical patterns, and correlations with global warming and external factors.

## Project Overview

This project analyzes 34 years of hourly weather data from Ulaanbaatar (1990-2024) to answer critical questions:

1. **How has Mongolia's climate changed?**
   - Long-term temperature trends
   - Warming rates by decade and season
   - Cyclical patterns identification

2. **How does Ulaanbaatar's warming compare to global trends?**
   - Correlation with global temperature data
   - Comparative warming rates

3. **What external factors influence local climate?**
   - Global population growth
   - Political and economic events
   - Russia & China economic/political indicators
   - Cross-border environmental effects

## Data Description

**Source**: OpenWeather historical data (1990-2024)
**Location**: Ulaanbaatar, Mongolia (47.92°N, 106.92°E)
**Records**: 299,122 hourly observations
**Variables**: Temperature, humidity, pressure, wind speed, cloud coverage, and more

### Data Columns

| Column | Description | Unit |
|--------|-------------|------|
| dt | Unix timestamp | - |
| dt_iso | ISO datetime | - |
| temp | Temperature | °C |
| feels_like | Apparent temperature | °C |
| humidity | Relative humidity | % |
| pressure | Atmospheric pressure | hPa |
| wind_speed | Wind speed | m/s |
| clouds_all | Cloud coverage | % |
| weather_main | Weather condition | - |

## Project Structure

```
weather_x_ulaanbaatar/
├── config/
│   └── config.py                    # Configuration settings
├── data/
│   ├── raw/                         # Raw weather data (place your CSV here)
│   ├── processed/                   # Processed data files
│   └── external/                    # External data (global temp, GDP, etc.)
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Initial data exploration
│   ├── 02_temporal_analysis.ipynb   # Trend and cyclical analysis
│   └── 03_correlation_analysis.ipynb # External factors correlation
├── src/
│   ├── analysis/
│   │   ├── temporal_analysis.py     # Temporal analysis functions
│   │   └── correlation_analysis.py  # Correlation analysis functions
│   ├── utils/
│   │   └── data_preprocessing.py    # Data preprocessing utilities
│   └── visualization/
│       └── plots.py                 # Visualization functions
├── results/
│   ├── figures/                     # Generated plots
│   ├── reports/                     # Analysis reports
│   └── statistics/                  # Statistical results
├── run_analysis.py                  # Main analysis script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation & Setup

### 1. Prerequisites

- Python 3.8+
- pip package manager
- Jupyter Notebook (optional, for interactive analysis)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Your Data

Place your Ulaanbaatar weather CSV file in the `data/raw/` directory:

```bash
# Your file should be named:
data/raw/ulaanbaatar_weather_1990_2024.csv

# Or update the path in config/config.py
```

## Quick Start

### Option 1: Run Complete Analysis (Command Line)

```bash
# Run the entire analysis pipeline
python run_analysis.py --all

# Or run specific steps:
python run_analysis.py --preprocess    # Only preprocess data
python run_analysis.py --temporal      # Only temporal analysis
python run_analysis.py --visualize     # Only generate plots
```

### Option 2: Interactive Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Then open notebooks in order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_temporal_analysis.ipynb
# 3. notebooks/03_correlation_analysis.ipynb
```

## Analysis Modules

### 1. Data Preprocessing

**Module**: `src/utils/data_preprocessing.py`

Functions:
- `load_weather_data()` - Load raw CSV data
- `convert_datetime()` - Convert to datetime index
- `check_data_quality()` - Quality assessment
- `handle_missing_values()` - Handle NaN values
- `add_temporal_features()` - Add year, month, season, etc.
- `aggregate_to_daily/monthly/yearly()` - Aggregate hourly data
- `preprocess_pipeline()` - Complete preprocessing

### 2. Temporal Analysis

**Module**: `src/analysis/temporal_analysis.py`

Functions:
- `calculate_trend()` - Linear/polynomial trend calculation
- `mann_kendall_test()` - Trend significance testing
- `calculate_moving_averages()` - Smooth data with moving windows
- `decompose_time_series()` - Decompose into trend/seasonal/residual
- `detect_cyclical_patterns()` - FFT-based pattern detection
- `analyze_seasonal_trends()` - Season-specific trend analysis
- `calculate_temperature_anomalies()` - Anomaly calculation
- `detect_extreme_events()` - Extreme temperature event detection

### 3. Correlation Analysis

**Module**: `src/analysis/correlation_analysis.py`

Functions:
- `calculate_correlation_matrix()` - Pairwise correlations
- `calculate_pairwise_correlation()` - Two-variable correlation with significance
- `calculate_cross_correlation()` - Time-lagged correlation
- `merge_external_data()` - Merge with external datasets
- `analyze_global_temperature_correlation()` - Compare with global trends
- `granger_causality_test()` - Test for causal relationships

### 4. Visualization

**Module**: `src/visualization/plots.py`

Functions:
- `plot_temperature_trend()` - Time series with trend line
- `plot_moving_averages()` - Multiple moving averages
- `plot_seasonal_decomposition()` - Decomposition components
- `plot_temperature_by_decade()` - Decade comparison
- `plot_temperature_by_season()` - Seasonal trends
- `plot_correlation_matrix()` - Heatmap of correlations
- `plot_temperature_anomalies()` - Anomaly visualization
- `plot_comparison_with_global()` - UB vs global temperature

## External Data Sources

For comprehensive correlation analysis, obtain the following datasets:

### Global Temperature Data

1. **NASA GISS Surface Temperature**
   - URL: https://data.giss.nasa.gov/gistemp/
   - Format: CSV
   - Variables: Global temperature anomalies

2. **NOAA Global Temperature**
   - URL: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series
   - Format: CSV
   - Variables: Land+ocean temperature

3. **Berkeley Earth**
   - URL: http://berkeleyearth.org/data/
   - Format: CSV
   - Variables: Global land temperature

### Population Data

- **World Bank**: https://data.worldbank.org/indicator/SP.POP.TOTL
- **UN Population Division**: https://population.un.org/wpp/Download/Standard/CSV/

### Economic & Emissions Data

1. **Russia & China GDP**
   - World Bank: https://data.worldbank.org/country
   - IMF: https://www.imf.org/en/Data

2. **CO2 Emissions**
   - Global Carbon Project: https://globalcarbonbudget.org/
   - EDGAR: https://edgar.jrc.ec.europa.eu/

3. **Energy Consumption**
   - World Bank Energy Data
   - BP Statistical Review of World Energy

### Data Format

Save external data as CSV files in `data/external/` with standardized columns:

```
data/external/
├── global_temperature.csv    # Columns: year, global_temp
├── world_population.csv      # Columns: year, population
├── russia_china_economic.csv # Columns: year, russia_gdp, china_gdp, russia_emissions, china_emissions
```

## Expected Results

### Temporal Analysis Outputs

1. **Warming Rate**: °C per decade
2. **Total Temperature Change**: 1990-2024
3. **Seasonal Warming Rates**: By season
4. **Cyclical Patterns**: Dominant periods (yearly, multi-year)
5. **Extreme Events**: Hot/cold event frequency
6. **Statistical Significance**: p-values for all trends

### Visualizations

Generated in `results/figures/`:

- `10_temperature_trend.png` - Long-term temperature trend
- `11_moving_averages.png` - Smoothed temperature curves
- `12_by_decade.png` - Temperature distribution by decade
- `13_seasonal_trends.png` - Seasonal warming patterns
- `14_decomposition.png` - Time series decomposition
- `15_anomalies.png` - Temperature anomalies
- `20_ub_vs_global.png` - UB vs global comparison
- `21_temp_vs_population.png` - Temperature vs population
- `22_correlation_matrix.png` - Comprehensive correlations

### Statistical Reports

Saved in `results/statistics/`:

- `temporal_analysis_summary.json` - All temporal analysis metrics
- `quality_report.json` - Data quality assessment

## Research Questions & Methods

### Q1: Has Ulaanbaatar's temperature increased?

**Methods**:
- Linear regression on daily/yearly averages
- Mann-Kendall trend test
- Calculate warming rate per decade
- Compare to baseline period (1990-2000)

### Q2: What cyclical patterns exist?

**Methods**:
- Seasonal decomposition (STL)
- Fourier analysis (FFT)
- Autocorrelation analysis (ACF/PACF)
- Identify multi-year cycles

### Q3: How does UB warming compare to global trends?

**Methods**:
- Pearson/Spearman correlation
- Compare warming rates
- Cross-correlation with lags
- Visual trend comparison

### Q4: Do external factors correlate with temperature?

**Methods**:
- Correlation analysis (population, GDP, emissions)
- Partial correlation (controlling for time trend)
- Granger causality tests
- Cross-border pollution analysis

## Customization

### Change Configuration

Edit `config/config.py` to customize:

```python
# Analysis parameters
ANALYSIS_CONFIG = {
    "start_year": 1990,
    "end_year": 2024,

    # Seasonal definitions
    "seasons": {
        "Winter": [12, 1, 2],
        "Spring": [3, 4, 5],
        "Summer": [6, 7, 8],
        "Fall": [9, 10, 11]
    },

    # Moving average windows (in days)
    "moving_average_windows": [30, 365, 1825],

    # Statistical significance level
    "significance_level": 0.05,
}
```

### Add Custom Analysis

Create new modules in `src/analysis/` or add cells to notebooks.

## Troubleshooting

### Common Issues

1. **"File not found" error**
   - Ensure CSV file is in `data/raw/`
   - Check filename matches configuration

2. **Missing values in data**
   - Preprocessing handles this automatically
   - Review `quality_report.json` for details

3. **Import errors**
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check Python version >= 3.8

4. **Plots not displaying in Jupyter**
   - Add `%matplotlib inline` at the start
   - Try restarting kernel

### Getting Help

- Check documentation in code comments
- Review example notebooks
- Inspect `results/statistics/` for analysis outputs

## Contributing

Feel free to extend this project:

1. Add new analysis methods
2. Improve visualizations
3. Incorporate additional external datasets
4. Create automated reporting

## License

This project is for research and educational purposes.

## Citation

If you use this analysis framework, please cite:

```
Ulaanbaatar Weather Analysis Project (1990-2024)
Data Source: OpenWeather
Analysis Period: 1990-11-25 to 2024-present
```

## Acknowledgments

- **Data Source**: OpenWeather historical data
- **External Data**: NASA GISS, NOAA, World Bank, UN
- **Tools**: Python, pandas, statsmodels, matplotlib, seaborn

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Place your data in `data/raw/`
3. ✅ Run preprocessing: `python run_analysis.py --preprocess`
4. ✅ Explore notebooks: `jupyter notebook`
5. ✅ Run full analysis: `python run_analysis.py --all`
6. ⏳ Obtain external data for correlation analysis
7. ⏳ Complete notebook 03 with external data
8. ⏳ Compile final research report

---

**Questions?** Review the code documentation and example notebooks for detailed guidance.

**Happy Analyzing!** 🌡️📊
