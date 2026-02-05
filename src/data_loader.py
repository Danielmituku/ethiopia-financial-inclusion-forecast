"""
Data loading utilities for Ethiopia Financial Inclusion Forecasting System
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def load_unified_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Load the unified Ethiopia financial inclusion dataset.
    
    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. If None, loads from default location.
        
    Returns
    -------
    pd.DataFrame
        The unified dataset with all record types.
    """
    if filepath is None:
        filepath = get_project_root() / "data" / "raw" / "ethiopia_fi_unified_data.csv"
    
    df = pd.read_csv(filepath)
    
    # Convert date columns
    date_cols = ['observation_date', 'event_date', 'collection_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


def load_reference_codes(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Load the reference codes for categorical fields.
    
    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. If None, loads from default location.
        
    Returns
    -------
    pd.DataFrame
        Reference codes dataframe.
    """
    if filepath is None:
        filepath = get_project_root() / "data" / "raw" / "reference_codes.csv"
    
    return pd.read_csv(filepath)


def split_by_record_type(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Split the unified dataset by record type.
    
    Parameters
    ----------
    df : pd.DataFrame
        The unified dataset.
        
    Returns
    -------
    dict
        Dictionary with keys 'observation', 'event', 'impact_link', 'target'.
    """
    result = {}
    for record_type in ['observation', 'event', 'impact_link', 'target']:
        result[record_type] = df[df['record_type'] == record_type].copy()
    return result


def get_observations(df: pd.DataFrame) -> pd.DataFrame:
    """Get observation records from unified dataset."""
    return df[df['record_type'] == 'observation'].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    """Get event records from unified dataset."""
    return df[df['record_type'] == 'event'].copy()


def get_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Get impact_link records from unified dataset."""
    return df[df['record_type'] == 'impact_link'].copy()


def get_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Get target records from unified dataset."""
    return df[df['record_type'] == 'target'].copy()


def get_indicator_time_series(df: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    """
    Extract time series for a specific indicator.
    
    Parameters
    ----------
    df : pd.DataFrame
        The unified dataset or observations subset.
    indicator_code : str
        The indicator code (e.g., 'ACC_OWNERSHIP').
        
    Returns
    -------
    pd.DataFrame
        Time series dataframe with date and value columns.
    """
    observations = df[df['record_type'] == 'observation'] if 'record_type' in df.columns else df
    indicator_data = observations[observations['indicator_code'] == indicator_code].copy()
    indicator_data = indicator_data.sort_values('observation_date')
    return indicator_data[['observation_date', 'value_numeric', 'source_name', 'confidence']].reset_index(drop=True)


def merge_events_with_impacts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Join events with their impact links.
    
    Parameters
    ----------
    df : pd.DataFrame
        The unified dataset.
        
    Returns
    -------
    pd.DataFrame
        Events dataframe with impact information.
    """
    events = get_events(df)
    impacts = get_impact_links(df)
    
    # Rename columns for clarity
    events_subset = events[['id', 'category', 'indicator', 'value_text', 'event_date', 
                            'source_name', 'confidence']].copy()
    events_subset = events_subset.rename(columns={
        'indicator': 'event_name',
        'value_text': 'event_description',
        'id': 'event_id'
    })
    
    impacts_subset = impacts[['parent_id', 'related_indicator', 'impact_direction', 
                               'impact_magnitude', 'lag_months', 'evidence_basis']].copy()
    
    merged = pd.merge(
        impacts_subset, 
        events_subset,
        left_on='parent_id',
        right_on='event_id',
        how='left'
    )
    
    return merged


def summarize_dataset(df: pd.DataFrame) -> Dict:
    """
    Generate summary statistics for the dataset.
    
    Parameters
    ----------
    df : pd.DataFrame
        The unified dataset.
        
    Returns
    -------
    dict
        Summary statistics.
    """
    summary = {
        'total_records': len(df),
        'record_type_counts': df['record_type'].value_counts().to_dict(),
        'pillar_counts': df['pillar'].value_counts().to_dict(),
        'confidence_counts': df['confidence'].value_counts().to_dict(),
        'unique_indicators': df['indicator_code'].nunique(),
        'date_range': {
            'min': df['observation_date'].min(),
            'max': df['observation_date'].max()
        }
    }
    return summary
