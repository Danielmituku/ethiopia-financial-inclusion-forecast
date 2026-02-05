"""
Visualization utilities for Ethiopia Financial Inclusion Forecasting System
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple
import warnings

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def setup_plot_style():
    """Configure matplotlib style for consistent visualizations."""
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 100
    })


def plot_account_ownership_trajectory(df: pd.DataFrame, 
                                       save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot Ethiopia's account ownership trajectory over time.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with ACC_OWNERSHIP observations.
    save_path : str, optional
        Path to save the figure.
        
    Returns
    -------
    matplotlib.Figure
        The figure object.
    """
    # Filter for account ownership
    acc_data = df[(df['record_type'] == 'observation') & 
                  (df['indicator_code'] == 'ACC_OWNERSHIP')].copy()
    acc_data = acc_data.sort_values('observation_date')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot main trajectory
    ax.plot(acc_data['observation_date'], acc_data['value_numeric'], 
            marker='o', markersize=10, linewidth=2, color='#2E86AB', label='Account Ownership')
    
    # Add value labels
    for _, row in acc_data.iterrows():
        ax.annotate(f"{row['value_numeric']:.0f}%", 
                   (row['observation_date'], row['value_numeric']),
                   textcoords="offset points", xytext=(0, 10),
                   ha='center', fontsize=11, fontweight='bold')
    
    # Add growth annotations
    for i in range(1, len(acc_data)):
        prev = acc_data.iloc[i-1]
        curr = acc_data.iloc[i]
        growth = curr['value_numeric'] - prev['value_numeric']
        mid_date = prev['observation_date'] + (curr['observation_date'] - prev['observation_date']) / 2
        mid_value = (prev['value_numeric'] + curr['value_numeric']) / 2
        ax.annotate(f"+{growth:.0f}pp", (mid_date, mid_value),
                   fontsize=9, color='#28A745', ha='center', style='italic')
    
    # Add target line (NFIS-II: 60% by 2025)
    ax.axhline(y=60, color='#DC3545', linestyle='--', linewidth=1.5, alpha=0.7, label='NFIS-II Target (60%)')
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Account Ownership Rate (%)')
    ax.set_title("Ethiopia's Account Ownership Trajectory (2011-2024)\nGlobal Findex Data", fontsize=14)
    ax.legend(loc='lower right')
    ax.set_ylim(0, 70)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_indicator_trends(df: pd.DataFrame, 
                           indicator_codes: List[str],
                           title: str = "Financial Inclusion Indicators Over Time",
                           save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot multiple indicators on the same chart.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with observations.
    indicator_codes : list
        List of indicator codes to plot.
    title : str
        Chart title.
    save_path : str, optional
        Path to save the figure.
        
    Returns
    -------
    matplotlib.Figure
        The figure object.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(indicator_codes)))
    
    for idx, code in enumerate(indicator_codes):
        data = df[(df['record_type'] == 'observation') & 
                  (df['indicator_code'] == code)].copy()
        data = data.sort_values('observation_date')
        
        if len(data) > 0:
            ax.plot(data['observation_date'], data['value_numeric'],
                   marker='o', linewidth=2, color=colors[idx],
                   label=data['indicator'].iloc[0] if 'indicator' in data.columns else code)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Rate (%)')
    ax.set_title(title, fontsize=14)
    ax.legend(loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_gender_gap(df: pd.DataFrame,
                     save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot gender gap in account ownership.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with gender-disaggregated observations.
    save_path : str, optional
        Path to save the figure.
        
    Returns
    -------
    matplotlib.Figure
        The figure object.
    """
    male_data = df[(df['record_type'] == 'observation') & 
                   (df['indicator_code'] == 'ACC_OWNERSHIP_M')].copy()
    female_data = df[(df['record_type'] == 'observation') & 
                     (df['indicator_code'] == 'ACC_OWNERSHIP_F')].copy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(male_data) > 0 and len(female_data) > 0:
        x = np.arange(len(male_data))
        width = 0.35
        
        years = male_data['observation_date'].dt.year.values
        
        bars1 = ax.bar(x - width/2, male_data['value_numeric'].values, width, 
                      label='Male', color='#2E86AB')
        bars2 = ax.bar(x + width/2, female_data['value_numeric'].values, width,
                      label='Female', color='#E91E63')
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Account Ownership Rate (%)')
        ax.set_title('Gender Gap in Account Ownership', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend()
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
        for bar in bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
    else:
        ax.text(0.5, 0.5, 'Insufficient gender-disaggregated data', 
               ha='center', va='center', fontsize=12)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_record_type_distribution(df: pd.DataFrame,
                                   save_path: Optional[str] = None) -> plt.Figure:
    """
    Create pie chart showing distribution of record types.
    
    Parameters
    ----------
    df : pd.DataFrame
        Unified dataset.
    save_path : str, optional
        Path to save the figure.
        
    Returns
    -------
    matplotlib.Figure
        The figure object.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Record type distribution
    record_counts = df['record_type'].value_counts()
    colors = ['#2E86AB', '#28A745', '#FFC107', '#DC3545']
    
    axes[0].pie(record_counts.values, labels=record_counts.index, autopct='%1.1f%%',
               colors=colors, explode=[0.05] * len(record_counts), shadow=True)
    axes[0].set_title('Distribution by Record Type', fontsize=12)
    
    # Source type distribution (for observations)
    obs = df[df['record_type'] == 'observation']
    if 'source_type' in obs.columns:
        source_counts = obs['source_type'].value_counts()
        axes[1].pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%',
                   colors=plt.cm.Set3(np.linspace(0, 1, len(source_counts))),
                   explode=[0.05] * len(source_counts), shadow=True)
        axes[1].set_title('Observations by Source Type', fontsize=12)
    
    plt.suptitle('Dataset Composition', fontsize=14, y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig
