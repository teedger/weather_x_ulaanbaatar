# Raw Data Directory

## Place Your Weather Data Here

This directory is for the raw Ulaanbaatar weather data CSV file.

### Expected File

**Filename**: `ulaanbaatar_weather_1990_2024.csv`

**Format**: CSV with the following columns (28 columns total):

| Column | Type | Description | Required |
|--------|------|-------------|----------|
| dt | integer | Unix timestamp | ✓ |
| dt_iso | string | ISO datetime (e.g., "1990-11-25 00:00:00 +0000 UTC") | ✓ |
| timezone | integer | Timezone offset in seconds | ✓ |
| city_name | string | City name | ✓ |
| lat | float | Latitude | ✓ |
| lon | float | Longitude | ✓ |
| temp | float | Temperature (°C) | ✓ |
| visibility | integer | Visibility (meters) | ✓ |
| dew_point | float | Dew point (°C) | ✓ |
| feels_like | float | Feels like temperature (°C) | ✓ |
| temp_min | float | Minimum temperature (°C) | ✓ |
| temp_max | float | Maximum temperature (°C) | ✓ |
| pressure | integer | Atmospheric pressure (hPa) | ✓ |
| sea_level | integer | Atmospheric pressure at sea level (hPa) | Optional |
| grnd_level | integer | Atmospheric pressure at ground level (hPa) | Optional |
| humidity | integer | Relative humidity (%) | ✓ |
| wind_speed | float | Wind speed (m/s) | ✓ |
| wind_deg | integer | Wind direction (degrees) | ✓ |
| wind_gust | float | Wind gust speed (m/s) | Optional |
| rain_1h | float | Rain volume for last hour (mm) | Optional |
| rain_3h | float | Rain volume for last 3 hours (mm) | Optional |
| snow_1h | float | Snow volume for last hour (mm) | Optional |
| snow_3h | float | Snow volume for last 3 hours (mm) | Optional |
| clouds_all | integer | Cloud coverage (%) | ✓ |
| weather_id | integer | Weather condition ID | ✓ |
| weather_main | string | Weather condition main category | ✓ |
| weather_description | string | Weather description | ✓ |
| weather_icon | string | Weather icon code | ✓ |

**Notes:**
- Optional columns may be empty or missing (preprocessing handles this gracefully)
- Precipitation columns (rain_*, snow_*) are often empty for dry periods
- sea_level and grnd_level may not be available for all weather stations

### Data Specifications

- **Time Period**: 1990-11-25 to 2024 (or latest)
- **Frequency**: Hourly observations
- **Expected Records**: ~299,122 rows (for 1990-2024)
- **Location**: Ulaanbaatar, Mongolia
- **Coordinates**: ~47.92°N, 106.92°E

### Example Rows

```csv
dt,dt_iso,timezone,city_name,lat,lon,temp,visibility,dew_point,feels_like,temp_min,temp_max,pressure,sea_level,grnd_level,humidity,wind_speed,wind_deg,wind_gust,rain_1h,rain_3h,snow_1h,snow_3h,clouds_all,weather_id,weather_main,weather_description,weather_icon
659491200,1990-11-25 00:00:00 +0000 UTC,28800,Ulaanbaatar,47.922051,106.915501,-12.07,10000,-16.12,-16.52,-13.82,-10.72,1021,,,69,2,90,,,,,20,801,Clouds,few clouds,02n
659494800,1990-11-25 01:00:00 +0000 UTC,28800,Ulaanbaatar,47.922051,106.915501,-12.45,10000,-16.48,-17.12,-14.20,-11.10,1021,,,70,2,90,,,,,20,801,Clouds,few clouds,02n
```

## Getting Started

1. **Upload your CSV file** to this directory
2. **Rename it** to `ulaanbaatar_weather_1990_2024.csv`
3. **Run preprocessing**:
   ```bash
   python run_analysis.py --preprocess
   ```

## Alternative Configuration

If your file has a different name, update the path in `config/config.py`:

```python
# In config/config.py
WEATHER_DATA_FILE = RAW_DATA_DIR / "your_filename.csv"
```

## Data Source

This project expects OpenWeather historical data format. If you have data from a different source, you may need to:

1. Rename columns to match the expected format
2. Adjust the preprocessing functions in `src/utils/data_preprocessing.py`
3. Ensure datetime is in ISO format or Unix timestamp

---

**Ready?** Once you've placed your data file here, proceed with the analysis!
