"""
Forecasting utilities for Ethiopia Financial Inclusion Forecasting System
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def linear_trend_forecast(years: np.ndarray, values: np.ndarray, 
                          forecast_years: List[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fit a linear trend and forecast future values.
    
    Parameters
    ----------
    years : np.ndarray
        Historical years
    values : np.ndarray
        Historical values
    forecast_years : list
        Years to forecast
        
    Returns
    -------
    tuple
        (forecast values, lower bound, upper bound)
    """
    # Fit linear regression
    coeffs = np.polyfit(years, values, 1)
    slope, intercept = coeffs
    
    # Forecast
    forecast = np.array([slope * y + intercept for y in forecast_years])
    
    # Calculate residual standard error for confidence intervals
    fitted = slope * years + intercept
    residuals = values - fitted
    std_error = np.std(residuals)
    
    # 95% confidence interval
    margin = 1.96 * std_error * np.sqrt(1 + 1/len(years) + 
                                         (np.array(forecast_years) - years.mean())**2 / 
                                         np.sum((years - years.mean())**2))
    
    lower = forecast - margin
    upper = forecast + margin
    
    return forecast, lower, upper


def log_trend_forecast(years: np.ndarray, values: np.ndarray,
                       forecast_years: List[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fit a logarithmic trend (modeling diminishing returns).
    
    Parameters
    ----------
    years : np.ndarray
        Historical years
    values : np.ndarray
        Historical values  
    forecast_years : list
        Years to forecast
        
    Returns
    -------
    tuple
        (forecast values, lower bound, upper bound)
    """
    # Transform years to log scale (relative to first year)
    base_year = years.min()
    log_years = np.log1p(years - base_year + 1)
    log_forecast_years = np.log1p(np.array(forecast_years) - base_year + 1)
    
    # Fit linear regression on log-transformed years
    coeffs = np.polyfit(log_years, values, 1)
    slope, intercept = coeffs
    
    # Forecast
    forecast = slope * log_forecast_years + intercept
    
    # Calculate residual standard error
    fitted = slope * log_years + intercept
    residuals = values - fitted
    std_error = np.std(residuals)
    
    # Confidence intervals
    margin = 1.96 * std_error
    lower = forecast - margin
    upper = forecast + margin
    
    return forecast, lower, upper


def scenario_forecast(current_value: float, 
                      target_value: float,
                      target_year: int,
                      current_year: int = 2024,
                      scenarios: Dict[str, float] = None) -> Dict:
    """
    Generate scenario-based forecasts.
    
    Parameters
    ----------
    current_value : float
        Current indicator value
    target_value : float
        Policy target value
    target_year : int
        Target year
    current_year : int
        Current year
    scenarios : dict, optional
        Custom scenario growth rates (annual pp)
        
    Returns
    -------
    dict
        Forecasts for each scenario
    """
    if scenarios is None:
        scenarios = {
            'optimistic': 4.0,    # 4pp per year
            'base': 2.5,          # 2.5pp per year
            'pessimistic': 1.0    # 1pp per year
        }
    
    forecast_years = list(range(current_year + 1, target_year + 1))
    results = {'years': forecast_years}
    
    for scenario, annual_growth in scenarios.items():
        forecasts = []
        value = current_value
        for year in forecast_years:
            value = min(value + annual_growth, 100)  # Cap at 100%
            forecasts.append(value)
        results[scenario] = forecasts
    
    return results


def calculate_growth_rates(years: np.ndarray, values: np.ndarray) -> pd.DataFrame:
    """
    Calculate period-over-period growth rates.
    
    Parameters
    ----------
    years : np.ndarray
        Years
    values : np.ndarray
        Values
        
    Returns
    -------
    pd.DataFrame
        Growth rate analysis
    """
    data = []
    for i in range(1, len(years)):
        period_years = years[i] - years[i-1]
        total_growth = values[i] - values[i-1]
        annual_growth = total_growth / period_years
        
        data.append({
            'period_start': years[i-1],
            'period_end': years[i],
            'period_years': period_years,
            'start_value': values[i-1],
            'end_value': values[i],
            'total_growth_pp': total_growth,
            'annual_growth_pp': annual_growth
        })
    
    return pd.DataFrame(data)


def forecast_access_usage(df: pd.DataFrame, forecast_years: List[int] = [2025, 2026, 2027]) -> Dict:
    """
    Generate forecasts for Access (Account Ownership) and Usage (Digital Payments).
    
    Parameters
    ----------
    df : pd.DataFrame
        Unified dataset
    forecast_years : list
        Years to forecast
        
    Returns
    -------
    dict
        Forecasts for both indicators
    """
    observations = df[df['record_type'] == 'observation']
    
    results = {}
    
    # Access (Account Ownership)
    acc_data = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
    acc_years = acc_data['observation_date'].dt.year.values
    acc_values = acc_data['value_numeric'].values
    
    # Linear trend
    acc_linear, acc_lower, acc_upper = linear_trend_forecast(acc_years, acc_values, forecast_years)
    
    # Log trend (diminishing returns)
    acc_log, acc_log_lower, acc_log_upper = log_trend_forecast(acc_years, acc_values, forecast_years)
    
    results['access'] = {
        'indicator': 'Account Ownership Rate',
        'code': 'ACC_OWNERSHIP',
        'current_value': acc_values[-1],
        'current_year': acc_years[-1],
        'historical_years': acc_years.tolist(),
        'historical_values': acc_values.tolist(),
        'forecast_years': forecast_years,
        'linear_forecast': acc_linear.tolist(),
        'linear_lower': acc_lower.tolist(),
        'linear_upper': acc_upper.tolist(),
        'log_forecast': acc_log.tolist(),
        'log_lower': acc_log_lower.tolist(),
        'log_upper': acc_log_upper.tolist(),
        'target': 60.0,
        'target_year': 2025
    }
    
    # Usage (Digital Payments)
    usg_data = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT'].sort_values('observation_date')
    if len(usg_data) >= 2:
        usg_years = usg_data['observation_date'].dt.year.values
        usg_values = usg_data['value_numeric'].values
        
        usg_linear, usg_lower, usg_upper = linear_trend_forecast(usg_years, usg_values, forecast_years)
        usg_log, usg_log_lower, usg_log_upper = log_trend_forecast(usg_years, usg_values, forecast_years)
        
        results['usage'] = {
            'indicator': 'Digital Payment Adoption',
            'code': 'USG_DIGITAL_PAYMENT',
            'current_value': usg_values[-1],
            'current_year': usg_years[-1],
            'historical_years': usg_years.tolist(),
            'historical_values': usg_values.tolist(),
            'forecast_years': forecast_years,
            'linear_forecast': usg_linear.tolist(),
            'linear_lower': usg_lower.tolist(),
            'linear_upper': usg_upper.tolist(),
            'log_forecast': usg_log.tolist(),
            'log_lower': usg_log_lower.tolist(),
            'log_upper': usg_log_upper.tolist(),
            'target': 50.0,
            'target_year': 2025
        }
    
    return results


def create_forecast_table(forecasts: Dict) -> pd.DataFrame:
    """
    Create a formatted forecast table.
    
    Parameters
    ----------
    forecasts : dict
        Forecast results from forecast_access_usage
        
    Returns
    -------
    pd.DataFrame
        Formatted forecast table
    """
    rows = []
    
    for indicator_key, data in forecasts.items():
        for i, year in enumerate(data['forecast_years']):
            rows.append({
                'Indicator': data['indicator'],
                'Year': year,
                'Linear Forecast': f"{data['linear_forecast'][i]:.1f}%",
                'CI (95%)': f"[{data['linear_lower'][i]:.1f}%, {data['linear_upper'][i]:.1f}%]",
                'Log Forecast': f"{data['log_forecast'][i]:.1f}%",
                'Target': f"{data['target']:.0f}%" if year == data['target_year'] else '-'
            })
    
    return pd.DataFrame(rows)
