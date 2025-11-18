#!/usr/bin/env python3
"""
Main analysis script for Ulaanbaatar Weather Analysis Project

Usage:
    python run_analysis.py --all                    # Run complete analysis
    python run_analysis.py --preprocess             # Only preprocess data
    python run_analysis.py --temporal               # Only temporal analysis
    python run_analysis.py --visualize              # Only generate visualizations
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

from config.config import *
from src.utils.data_preprocessing import preprocess_pipeline
from src.analysis.temporal_analysis import *
from src.visualization.plots import *


def run_preprocessing(data_file):
    """Run data preprocessing pipeline"""
    print("\n" + "="*80)
    print("STEP 1: DATA PREPROCESSING")
    print("="*80 + "\n")

    if not Path(data_file).exists():
        print(f"❌ Error: Data file not found: {data_file}")
        print("\nPlease ensure your CSV file is located at:")
        print(f"  {WEATHER_DATA_FILE}")
        return None

    processed_data = preprocess_pipeline(data_file, save_processed=True)
    return processed_data


def run_temporal_analysis():
    """Run temporal analysis"""
    print("\n" + "="*80)
    print("STEP 2: TEMPORAL ANALYSIS")
    print("="*80 + "\n")

    # Load processed data
    df_daily = pd.read_csv(PROCESSED_DATA_DIR / 'daily_aggregated.csv',
                           index_col=0, parse_dates=True)
    df_yearly = pd.read_csv(PROCESSED_DATA_DIR / 'yearly_aggregated.csv',
                            index_col=0, parse_dates=True)
    df_hourly = pd.read_csv(PROCESSED_DATA_DIR / 'hourly_processed.csv',
                            index_col=0, parse_dates=True)

    results = {}

    # 1. Calculate trend
    print("\n[1/8] Calculating temperature trend...")
    trend_result = calculate_trend(df_daily, column='temp_mean', method='linear')
    results['trend'] = trend_result

    print(f"\n{'='*60}")
    print("TEMPERATURE TREND SUMMARY")
    print(f"{'='*60}")
    print(f"Warming rate: {trend_result['slope'] * 365.25 * 10:.4f}°C per decade")
    print(f"Total change (1990-2024): {trend_result['total_change']:.2f}°C")
    print(f"R²: {trend_result['r_squared']:.4f}")
    print(f"P-value: {trend_result['p_value']:.2e}")

    # 2. Mann-Kendall test
    print("\n[2/8] Performing Mann-Kendall test...")
    mk_result = mann_kendall_test(df_daily, column='temp_mean')
    results['mann_kendall'] = mk_result

    # 3. Moving averages
    print("\n[3/8] Calculating moving averages...")
    df_daily_ma = calculate_moving_averages(df_daily, column='temp_mean',
                                            windows=[30, 365, 1825])

    # 4. Time series decomposition
    print("\n[4/8] Decomposing time series...")
    decomposition = decompose_time_series(df_daily, column='temp_mean',
                                         model='additive', period=365)
    results['decomposition'] = decomposition

    # 5. Cyclical patterns
    print("\n[5/8] Detecting cyclical patterns...")
    cyclical_result = detect_cyclical_patterns(df_daily, column='temp_mean')
    results['cyclical'] = cyclical_result

    # 6. Seasonal trends
    print("\n[6/8] Analyzing seasonal trends...")
    seasonal_trends = analyze_seasonal_trends(df_hourly, temp_column='temp')
    results['seasonal_trends'] = seasonal_trends

    print(f"\n{'='*60}")
    print("SEASONAL WARMING RATES")
    print(f"{'='*60}")
    for season, trend in seasonal_trends.items():
        rate_per_decade = trend['slope'] * 365.25 * 10
        significance = "✓" if trend['p_value'] < 0.05 else "✗"
        print(f"{season:10s}: {rate_per_decade:+.4f}°C/decade  [{significance}]")

    # 7. Temperature anomalies
    print("\n[7/8] Calculating temperature anomalies...")
    df_yearly_anom = calculate_temperature_anomalies(
        df_yearly, column='temp_mean', baseline_period=(1990, 2000)
    )
    results['anomalies'] = df_yearly_anom

    # 8. Extreme events
    print("\n[8/8] Detecting extreme events...")
    extreme_events = detect_extreme_events(df_daily, column='temp_mean',
                                          threshold_percentile=95)
    results['extreme_events'] = extreme_events

    # Save results summary
    summary = {
        'warming_rate_per_decade': trend_result['slope'] * 365.25 * 10,
        'total_change_1990_2024': trend_result['total_change'],
        'r_squared': trend_result['r_squared'],
        'p_value': trend_result['p_value'],
        'mann_kendall_trend': mk_result['trend'],
        'mann_kendall_significant': mk_result['significant'],
        'seasonal_warming_rates': {
            season: trend['slope'] * 365.25 * 10
            for season, trend in seasonal_trends.items()
        },
        'extreme_hot_events': extreme_events['hot_events_count'],
        'extreme_cold_events': extreme_events['cold_events_count'],
    }

    import json
    with open(STATISTICS_DIR / 'temporal_analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n✓ Temporal analysis complete!")
    print(f"  Results saved to: {STATISTICS_DIR / 'temporal_analysis_summary.json'}")

    return results


def run_visualization(temporal_results=None):
    """Generate all visualizations"""
    print("\n" + "="*80)
    print("STEP 3: GENERATING VISUALIZATIONS")
    print("="*80 + "\n")

    # Load data
    df_daily = pd.read_csv(PROCESSED_DATA_DIR / 'daily_aggregated.csv',
                           index_col=0, parse_dates=True)
    df_yearly = pd.read_csv(PROCESSED_DATA_DIR / 'yearly_aggregated.csv',
                            index_col=0, parse_dates=True)
    df_hourly = pd.read_csv(PROCESSED_DATA_DIR / 'hourly_processed.csv',
                            index_col=0, parse_dates=True)

    plot_count = 0

    # 1. Temperature trend with line
    print(f"[{plot_count+1}] Plotting temperature trend...")
    if temporal_results and 'trend' in temporal_results:
        trend_line = temporal_results['trend']['trend_line']
    else:
        from src.analysis.temporal_analysis import calculate_trend
        trend_result = calculate_trend(df_daily, column='temp_mean')
        trend_line = trend_result['trend_line']

    plot_temperature_trend(df_daily, column='temp_mean',
                          title='Ulaanbaatar Temperature Trend (1990-2024)',
                          trend_line=trend_line,
                          save_path=FIGURES_DIR / '10_temperature_trend.png')
    plt.close()
    plot_count += 1

    # 2. Moving averages
    print(f"[{plot_count+1}] Plotting moving averages...")
    df_daily_ma = calculate_moving_averages(df_daily, column='temp_mean',
                                            windows=[365, 1825])
    plot_moving_averages(df_daily_ma, column='temp_mean',
                        windows=[365, 1825],
                        save_path=FIGURES_DIR / '11_moving_averages.png')
    plt.close()
    plot_count += 1

    # 3. Temperature by decade
    print(f"[{plot_count+1}] Plotting temperature by decade...")
    plot_temperature_by_decade(df_hourly, column='temp',
                              save_path=FIGURES_DIR / '12_by_decade.png')
    plt.close()
    plot_count += 1

    # 4. Temperature by season
    print(f"[{plot_count+1}] Plotting seasonal trends...")
    plot_temperature_by_season(df_hourly, column='temp',
                              save_path=FIGURES_DIR / '13_seasonal_trends.png')
    plt.close()
    plot_count += 1

    # 5. Decomposition
    print(f"[{plot_count+1}] Plotting time series decomposition...")
    if temporal_results and 'decomposition' in temporal_results:
        decomposition = temporal_results['decomposition']
    else:
        decomposition = decompose_time_series(df_daily, column='temp_mean',
                                              period=365)
    plot_seasonal_decomposition(decomposition,
                               title='Temperature Decomposition',
                               save_path=FIGURES_DIR / '14_decomposition.png')
    plt.close()
    plot_count += 1

    # 6. Temperature anomalies
    print(f"[{plot_count+1}] Plotting temperature anomalies...")
    df_yearly_anom = calculate_temperature_anomalies(
        df_yearly, column='temp_mean', baseline_period=(1990, 2000)
    )
    plot_temperature_anomalies(df_yearly_anom,
                              anomaly_column='temp_mean_anomaly',
                              title='Temperature Anomalies (Baseline: 1990-2000)',
                              save_path=FIGURES_DIR / '15_anomalies.png')
    plt.close()
    plot_count += 1

    print(f"\n✓ Generated {plot_count} visualizations!")
    print(f"  Saved to: {FIGURES_DIR}")


def main():
    parser = argparse.ArgumentParser(
        description='Ulaanbaatar Weather Analysis (1990-2024)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--all', action='store_true',
                       help='Run complete analysis pipeline')
    parser.add_argument('--preprocess', action='store_true',
                       help='Run data preprocessing only')
    parser.add_argument('--temporal', action='store_true',
                       help='Run temporal analysis only')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualizations only')
    parser.add_argument('--data-file', type=str, default=str(WEATHER_DATA_FILE),
                       help='Path to weather data CSV file')

    args = parser.parse_args()

    # If no arguments, show help
    if not any([args.all, args.preprocess, args.temporal, args.visualize]):
        parser.print_help()
        return

    print("\n" + "="*80)
    print("ULAANBAATAR WEATHER ANALYSIS PROJECT")
    print("Analyzing climate change patterns (1990-2024)")
    print("="*80)

    temporal_results = None

    # Run preprocessing
    if args.all or args.preprocess:
        processed_data = run_preprocessing(args.data_file)
        if processed_data is None and args.preprocess:
            return

    # Run temporal analysis
    if args.all or args.temporal:
        temporal_results = run_temporal_analysis()

    # Run visualization
    if args.all or args.visualize:
        run_visualization(temporal_results)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nResults saved to:")
    print(f"  - Processed data: {PROCESSED_DATA_DIR}")
    print(f"  - Figures: {FIGURES_DIR}")
    print(f"  - Statistics: {STATISTICS_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Explore Jupyter notebooks in: notebooks/")
    print(f"  2. Review visualizations in: {FIGURES_DIR}")
    print(f"  3. Obtain external data for correlation analysis")
    print()


if __name__ == '__main__':
    main()
