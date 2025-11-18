"""
Visualization module for weather analysis
Create various plots for temporal trends, correlations, and comparisons
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import COLORS, FIGURES_DIR, ANALYSIS_CONFIG

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = ANALYSIS_CONFIG['figure_dpi']


def plot_temperature_trend(df, column='temp_mean', title='Temperature Trend',
                           trend_line=None, save_path=None):
    """
    Plot temperature time series with optional trend line

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe
    column : str
        Temperature column to plot
    title : str
        Plot title
    trend_line : np.array
        Trend line values
    save_path : str
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot temperature
    ax.plot(df.index, df[column], alpha=0.6, linewidth=0.8,
            color=COLORS['primary'], label='Actual')

    # Plot trend line if provided
    if trend_line is not None:
        ax.plot(df.index, trend_line, color=COLORS['danger'],
                linewidth=2, label='Trend')

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, ax


def plot_moving_averages(df, column='temp_mean', windows=[365, 1825],
                        title='Temperature with Moving Averages', save_path=None):
    """
    Plot temperature with multiple moving averages

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with moving averages
    column : str
        Temperature column
    windows : list
        List of window sizes
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot original data with low alpha
    ax.plot(df.index, df[column], alpha=0.2, linewidth=0.5,
            color='gray', label='Daily')

    # Plot moving averages
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['success']]
    for i, window in enumerate(windows):
        ma_col = f'{column}_ma_{window}d'
        if ma_col in df.columns:
            label = f'{window}-day MA'
            ax.plot(df.index, df[ma_col], linewidth=2,
                   color=colors[i % len(colors)], label=label)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, ax


def plot_seasonal_decomposition(decomposition, title='Time Series Decomposition',
                                save_path=None):
    """
    Plot time series decomposition components

    Parameters:
    -----------
    decomposition : statsmodels DecomposeResult
        Decomposition result
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, axes = plt.subplots(4, 1, figsize=(14, 10))

    # Original
    decomposition.observed.plot(ax=axes[0], color=COLORS['primary'])
    axes[0].set_ylabel('Observed')
    axes[0].set_title(title, fontsize=14, fontweight='bold')

    # Trend
    decomposition.trend.plot(ax=axes[1], color=COLORS['secondary'])
    axes[1].set_ylabel('Trend')

    # Seasonal
    decomposition.seasonal.plot(ax=axes[2], color=COLORS['success'])
    axes[2].set_ylabel('Seasonal')

    # Residual
    decomposition.resid.plot(ax=axes[3], color=COLORS['danger'])
    axes[3].set_ylabel('Residual')
    axes[3].set_xlabel('Date')

    for ax in axes:
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, axes


def plot_temperature_by_decade(df, column='temp_mean', save_path=None):
    """
    Plot temperature comparison by decade

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with decade column
    column : str
        Temperature column
    save_path : str
        Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Box plot
    decades = sorted(df['decade_label'].unique())
    data_to_plot = [df[df['decade_label'] == d][column].dropna() for d in decades]

    bp = ax1.boxplot(data_to_plot, labels=decades, patch_artist=True)

    # Color boxes
    decade_colors = [COLORS['decades'].get(d, COLORS['primary']) for d in decades]
    for patch, color in zip(bp['boxes'], decade_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax1.set_xlabel('Decade', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.set_title('Temperature Distribution by Decade', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Mean temperature by decade
    decade_means = df.groupby('decade_label')[column].mean().reindex(decades)

    bars = ax2.bar(decades, decade_means, color=decade_colors, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Decade', fontsize=12)
    ax2.set_ylabel('Mean Temperature (°C)', fontsize=12)
    ax2.set_title('Mean Temperature by Decade', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}°C', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, (ax1, ax2)


def plot_temperature_by_season(df, column='temp_mean', save_path=None):
    """
    Plot temperature comparison by season

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with season column
    column : str
        Temperature column
    save_path : str
        Path to save figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()

    seasons = ['Winter', 'Spring', 'Summer', 'Fall']

    for idx, season in enumerate(seasons):
        season_data = df[df['season'] == season].copy()
        season_data['year'] = season_data.index.year

        # Yearly average for this season
        yearly_avg = season_data.groupby('year')[column].mean()

        ax = axes[idx]
        ax.plot(yearly_avg.index, yearly_avg.values, marker='o',
                color=COLORS['seasons'][season], linewidth=2, markersize=4)

        # Add trend line
        from src.analysis.temporal_analysis import calculate_trend
        trend_result = calculate_trend(pd.DataFrame({column: yearly_avg}),
                                       column=column, method='linear')

        if trend_result:
            trend_line = trend_result['slope'] * np.arange(len(yearly_avg)) + trend_result['intercept']
            ax.plot(yearly_avg.index, trend_line, '--',
                   color=COLORS['danger'], linewidth=2,
                   label=f"Trend: {trend_result['slope']*10:.3f}°C/decade")

        ax.set_xlabel('Year', fontsize=11)
        ax.set_ylabel('Temperature (°C)', fontsize=11)
        ax.set_title(f'{season} Temperature Trend', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, axes


def plot_correlation_matrix(corr_matrix, title='Correlation Matrix', save_path=None):
    """
    Plot correlation matrix heatmap

    Parameters:
    -----------
    corr_matrix : pd.DataFrame
        Correlation matrix
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, vmin=-1, vmax=1, square=True,
                linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, ax


def plot_temperature_anomalies(df, anomaly_column='temp_mean_anomaly',
                               title='Temperature Anomalies', save_path=None):
    """
    Plot temperature anomalies

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with anomaly column
    anomaly_column : str
        Anomaly column name
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # Get anomalies
    anomalies = df[anomaly_column]

    # Plot bars colored by sign
    colors = [COLORS['danger'] if x > 0 else COLORS['primary'] for x in anomalies]
    ax.bar(df.index, anomalies, color=colors, alpha=0.7, width=20)

    # Add zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature Anomaly (°C)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, ax


def plot_comparison_with_global(ub_data, global_data,
                                ub_col='temp_mean', global_col='global_temp',
                                title='Ulaanbaatar vs Global Temperature',
                                save_path=None):
    """
    Plot comparison between Ulaanbaatar and global temperature

    Parameters:
    -----------
    ub_data : pd.DataFrame
        Ulaanbaatar data
    global_data : pd.DataFrame
        Global temperature data
    ub_col : str
        UB temperature column
    global_col : str
        Global temperature column
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Merge data
    from src.analysis.correlation_analysis import merge_external_data
    merged = merge_external_data(ub_data, global_data, on='year')

    # Plot 1: Both temperatures
    ax1_twin = ax1.twinx()

    line1 = ax1.plot(merged.index, merged[ub_col], color=COLORS['primary'],
                     linewidth=2, label='Ulaanbaatar')
    line2 = ax1_twin.plot(merged.index, merged[global_col], color=COLORS['secondary'],
                          linewidth=2, label='Global')

    ax1.set_ylabel('Ulaanbaatar Temp (°C)', fontsize=12, color=COLORS['primary'])
    ax1_twin.set_ylabel('Global Temp (°C)', fontsize=12, color=COLORS['secondary'])
    ax1.set_title(title, fontsize=14, fontweight='bold')

    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1_twin.tick_params(axis='y', labelcolor=COLORS['secondary'])

    # Plot 2: Scatter plot
    ax2.scatter(merged[global_col], merged[ub_col], alpha=0.6,
                s=50, color=COLORS['primary'])

    # Add trend line
    z = np.polyfit(merged[global_col].dropna(), merged[ub_col].dropna(), 1)
    p = np.poly1d(z)
    ax2.plot(merged[global_col], p(merged[global_col]), "r--",
             linewidth=2, label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')

    ax2.set_xlabel('Global Temperature (°C)', fontsize=12)
    ax2.set_ylabel('Ulaanbaatar Temperature (°C)', fontsize=12)
    ax2.set_title('Correlation between Ulaanbaatar and Global Temperature',
                  fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, (ax1, ax2)


def plot_cross_correlation(cross_corr_result, var1_name, var2_name,
                           title='Cross-Correlation', save_path=None):
    """
    Plot cross-correlation results

    Parameters:
    -----------
    cross_corr_result : dict
        Result from calculate_cross_correlation
    var1_name, var2_name : str
        Variable names
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    lags = cross_corr_result['lags']
    correlations = cross_corr_result['correlations']
    best_lag = cross_corr_result['best_lag']

    # Plot cross-correlation
    ax.stem(lags, correlations, basefmt=' ')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

    # Highlight best lag
    best_idx = lags.index(best_lag)
    ax.plot(best_lag, correlations[best_idx], 'ro', markersize=10,
            label=f'Best lag: {best_lag} (r={correlations[best_idx]:.3f})')

    ax.set_xlabel('Lag', fontsize=12)
    ax.set_ylabel('Correlation', fontsize=12)
    ax.set_title(f'{title}: {var1_name} vs {var2_name}',
                fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, ax


def plot_autocorrelation(acf_result, title='Autocorrelation', save_path=None):
    """
    Plot ACF and PACF

    Parameters:
    -----------
    acf_result : dict
        Result from calculate_autocorrelation
    title : str
        Plot title
    save_path : str
        Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    lags = acf_result['lags']
    acf_values = acf_result['acf']
    pacf_values = acf_result['pacf']

    # Plot ACF
    ax1.stem(lags, acf_values, basefmt=' ')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax1.axhline(y=1.96/np.sqrt(len(acf_values)), color='red',
                linestyle='--', linewidth=1, alpha=0.5)
    ax1.axhline(y=-1.96/np.sqrt(len(acf_values)), color='red',
                linestyle='--', linewidth=1, alpha=0.5)
    ax1.set_ylabel('ACF', fontsize=12)
    ax1.set_title(f'{title} - ACF', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Plot PACF
    ax2.stem(lags, pacf_values, basefmt=' ')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax2.axhline(y=1.96/np.sqrt(len(pacf_values)), color='red',
                linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(y=-1.96/np.sqrt(len(pacf_values)), color='red',
                linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_xlabel('Lag', fontsize=12)
    ax2.set_ylabel('PACF', fontsize=12)
    ax2.set_title(f'{title} - PACF', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig, (ax1, ax2)


def create_dashboard(data_dict, save_path=None):
    """
    Create comprehensive dashboard with multiple plots

    Parameters:
    -----------
    data_dict : dict
        Dictionary with all required data
    save_path : str
        Path to save figure
    """
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # Your dashboard code here - customize based on available data

    plt.suptitle('Ulaanbaatar Weather Analysis Dashboard',
                 fontsize=16, fontweight='bold', y=0.995)

    if save_path:
        plt.savefig(save_path, dpi=ANALYSIS_CONFIG['figure_dpi'], bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def save_all_plots(data_dict, output_dir=None):
    """
    Generate and save all plots

    Parameters:
    -----------
    data_dict : dict
        Dictionary with all data
    output_dir : Path
        Output directory (default: FIGURES_DIR)
    """
    if output_dir is None:
        output_dir = FIGURES_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("GENERATING ALL PLOTS")
    print("="*60)

    # Generate each plot type based on available data
    # This will be customized based on the actual analysis results

    print(f"\nAll plots saved to: {output_dir}")
