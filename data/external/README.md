# External Data Directory

Place your external datasets here for correlation analysis.

## Required Data Files

### 1. Global Temperature Data

**File**: `global_temperature.csv`

**Required Columns**:
- `year` (integer): Year
- `global_temp` (float): Global temperature or anomaly

**Example**:
```csv
year,global_temp
1990,14.42
1991,14.38
1992,14.15
...
```

**Sources**:
- NASA GISS: https://data.giss.nasa.gov/gistemp/
- NOAA: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series
- Berkeley Earth: http://berkeleyearth.org/data/

---

### 2. World Population Data

**File**: `world_population.csv`

**Required Columns**:
- `year` (integer): Year
- `population` (integer): World population

**Example**:
```csv
year,population
1990,5327231061
1991,5414289444
1992,5498919809
...
```

**Sources**:
- World Bank: https://data.worldbank.org/indicator/SP.POP.TOTL
- UN: https://population.un.org/wpp/Download/Standard/CSV/

---

### 3. Russia & China Economic Data

**File**: `russia_china_economic.csv`

**Required Columns**:
- `year` (integer): Year
- `russia_gdp` (float): Russia GDP (current USD)
- `china_gdp` (float): China GDP (current USD)
- `russia_emissions` (float): Russia CO2 emissions (optional)
- `china_emissions` (float): China CO2 emissions (optional)

**Example**:
```csv
year,russia_gdp,china_gdp,russia_emissions,china_emissions
1990,516814000000,360858000000,2389,2241
1991,509380000000,383373000000,2298,2307
...
```

**Sources**:
- World Bank: https://data.worldbank.org/country
- IMF: https://www.imf.org/en/Data
- EDGAR Emissions: https://edgar.jrc.ec.europa.eu/

---

## Template Files

Copy these templates and fill with your data:

### global_temperature_template.csv
```csv
year,global_temp
1990,
1991,
1992,
...
2024,
```

### world_population_template.csv
```csv
year,population
1990,
1991,
...
2024,
```

### russia_china_economic_template.csv
```csv
year,russia_gdp,china_gdp,russia_emissions,china_emissions
1990,,,,
1991,,,,
...
2024,,,,
```

---

## Data Processing Tips

1. **Ensure year ranges match**: 1990-2024
2. **Use consistent units**: Check source documentation
3. **Handle missing data**: Use NA or leave blank (preprocessing will handle)
4. **Validate data**: Check for outliers and anomalies

## Notes

- External data is **optional** but required for correlation analysis (Notebook 03)
- You can run temporal analysis (Notebooks 01-02) without external data
- The analysis will skip correlation tests if external data is not available
