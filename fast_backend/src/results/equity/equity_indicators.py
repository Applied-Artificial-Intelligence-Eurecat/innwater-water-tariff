"""
Equity Indicators Calculation for Aggregate Dashboard

This module calculates equity indicators based on gross subsidies and gross taxes/margins.
Follows the 6-step process outlined by Michel for calculating net subsidies, net taxes,
and Omega ratios for both general and basic consumption/services.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any


def calculate_net_values(gross_subsidy: pd.Series, gross_margin: pd.Series) -> pd.Series:
    """
    Calculate net subsidies/taxes from gross values.

    Step 2: Net = Gross Subsidy - Gross Margin

    Args:
        gross_subsidy: Series of gross subsidies
        gross_margin: Series of gross margins (taxes)

    Returns:
        Series of net values (subsidy - margin)
    """
    return gross_subsidy - gross_margin


def truncate_positive(net_value: pd.Series) -> pd.Series:
    """
    Truncate to keep only positive values (net subsidies).

    Step 3: Max[net_value, 0]

    Args:
        net_value: Series of net values

    Returns:
        Series with only positive values (0 for negative)
    """
    return net_value.clip(lower=0)


def truncate_negative(net_value: pd.Series) -> pd.Series:
    """
    Truncate to keep only negative values as positive (net margins).

    Step 3: -Min[net_value, 0]

    Args:
        net_value: Series of net values

    Returns:
        Series with absolute value of negative values (0 for positive)
    """
    return (-net_value).clip(lower=0)


def calculate_omega_ratio(mean_poor: float, mean_population: float) -> float:
    """
    Calculate Omega ratio.

    Step 4: Omega = mean_poor / mean_population

    Args:
        mean_poor: Average for poor households
        mean_population: Average for all households

    Returns:
        Omega ratio (returns 0 if mean_population is 0)
    """
    if mean_population == 0:
        return 0.0
    return mean_poor / mean_population


def calculate_equity_indicators(
    gross_subsidy_consumption: pd.Series,
    gross_subsidy_service: pd.Series,
    gross_margin_consumption: pd.Series,
    gross_margin_service: pd.Series,
    is_poor: pd.Series
) -> Dict[str, Any]:
    """
    Calculate equity indicators for consumption and services.

    Steps 2-5: Calculate net subsidies, net margins, averages, and Omega ratios.

    Args:
        gross_subsidy_consumption: Gross subsidies on consumption (Access Fee Excluded)
        gross_subsidy_service: Gross subsidies on EP/EPA service (Access Fee Included)
        gross_margin_consumption: Gross margins on consumption (Access Fee Excluded)
        gross_margin_service: Gross margins on EP/EPA service (Access Fee Included)
        is_poor: Boolean series indicating if household is poor

    Returns:
        Dictionary with:
        - net_subsidy_consumption_mean: Average net subsidy on consumption (all)
        - net_subsidy_service_mean: Average net subsidy on service (all)
        - net_margin_consumption_mean: Average net margin on consumption (all)
        - net_margin_service_mean: Average net margin on service (all)
        - omega_net_subsidy_consumption: Omega ratio for net subsidy on consumption
        - omega_net_subsidy_service: Omega ratio for net subsidy on service
        - omega_net_margin_consumption: Omega ratio for net margin on consumption
        - omega_net_margin_service: Omega ratio for net margin on service
    """
    # Step 2: Calculate net values
    net_consumption = calculate_net_values(gross_subsidy_consumption, gross_margin_consumption)
    net_service = calculate_net_values(gross_subsidy_service, gross_margin_service)

    # Step 3: Truncate to get net subsidies and net margins
    net_subsidy_consumption = truncate_positive(net_consumption)
    net_subsidy_service = truncate_positive(net_service)
    net_margin_consumption = truncate_negative(net_consumption)
    net_margin_service = truncate_negative(net_service)

    # Step 4: Calculate averages for population and poor households
    results = {}

    # Population means
    results['net_subsidy_consumption_mean'] = net_subsidy_consumption.mean()
    results['net_subsidy_service_mean'] = net_subsidy_service.mean()
    results['net_margin_consumption_mean'] = net_margin_consumption.mean()
    results['net_margin_service_mean'] = net_margin_service.mean()

    # Poor households means
    net_subsidy_consumption_poor_mean = net_subsidy_consumption[is_poor].mean() if is_poor.any() else 0
    net_subsidy_service_poor_mean = net_subsidy_service[is_poor].mean() if is_poor.any() else 0
    net_margin_consumption_poor_mean = net_margin_consumption[is_poor].mean() if is_poor.any() else 0
    net_margin_service_poor_mean = net_margin_service[is_poor].mean() if is_poor.any() else 0

    # Omega ratios
    results['omega_net_subsidy_consumption'] = calculate_omega_ratio(
        net_subsidy_consumption_poor_mean, results['net_subsidy_consumption_mean']
    )
    results['omega_net_subsidy_service'] = calculate_omega_ratio(
        net_subsidy_service_poor_mean, results['net_subsidy_service_mean']
    )
    results['omega_net_margin_consumption'] = calculate_omega_ratio(
        net_margin_consumption_poor_mean, results['net_margin_consumption_mean']
    )
    results['omega_net_margin_service'] = calculate_omega_ratio(
        net_margin_service_poor_mean, results['net_margin_service_mean']
    )

    return results


def calculate_full_equity_indicators(
    # General consumption/service (Steps 1-5)
    gross_subsidy_consumption: pd.Series,
    gross_subsidy_service: pd.Series,
    gross_margin_consumption: pd.Series,
    gross_margin_service: pd.Series,
    # Basic consumption/service (Step 6)
    gross_subsidy_basic_consumption: pd.Series,
    gross_subsidy_basic_service: pd.Series,
    gross_margin_basic_consumption: pd.Series,
    gross_margin_basic_service: pd.Series,
    # Household information
    is_poor: pd.Series
) -> Dict[str, Any]:
    """
    Calculate complete equity indicators for both general and basic consumption/services.

    This function implements all 6 steps:
    - Steps 1-5: General consumption and services
    - Step 6: Basic consumption and services

    Args:
        gross_subsidy_consumption: Gross subsidies on consumption (Access Fee Excluded)
        gross_subsidy_service: Gross subsidies on EP/EPA service (Access Fee Included)
        gross_margin_consumption: Gross margins on consumption (Access Fee Excluded)
        gross_margin_service: Gross margins on EP/EPA service (Access Fee Included)
        gross_subsidy_basic_consumption: Gross subsidies on basic consumption (Access Fee Excluded)
        gross_subsidy_basic_service: Gross subsidies on basic service (Access Fee Included)
        gross_margin_basic_consumption: Gross margins on basic consumption (Access Fee Excluded)
        gross_margin_basic_service: Gross margins on basic service (Access Fee Included)
        is_poor: Boolean series indicating if household is poor

    Returns:
        Dictionary with equity indicators for both general and basic:
        - general: Dict with general equity indicators
        - basic: Dict with basic equity indicators
    """
    # Steps 1-5: General consumption/service indicators
    general_indicators = calculate_equity_indicators(
        gross_subsidy_consumption,
        gross_subsidy_service,
        gross_margin_consumption,
        gross_margin_service,
        is_poor
    )

    # Step 6: Basic consumption/service indicators
    basic_indicators = calculate_equity_indicators(
        gross_subsidy_basic_consumption,
        gross_subsidy_basic_service,
        gross_margin_basic_consumption,
        gross_margin_basic_service,
        is_poor
    )

    return {
        'general': general_indicators,
        'basic': basic_indicators
    }


def format_equity_table(indicators: Dict[str, Any]) -> pd.DataFrame:
    """
    Format equity indicators as a table for display in Aggregate Dashboard.

    Step 5: Display the four averages and four Omega ratios in a table.

    Args:
        indicators: Dictionary with general and basic indicators

    Returns:
        DataFrame formatted for Aggregate Dashboard display
    """
    general = indicators['general']
    basic = indicators['basic']

    # Create table with rows for each metric type
    table_data = {
        'Indicator': [
            'Net Subsidy on Consumption (mean)',
            'Net Subsidy on Service (mean)',
            'Net Margin on Consumption (mean)',
            'Net Margin on Service (mean)',
            'Omega - Net Subsidy on Consumption',
            'Omega - Net Subsidy on Service',
            'Omega - Net Margin on Consumption',
            'Omega - Net Margin on Service'
        ],
        'General': [
            general['net_subsidy_consumption_mean'],
            general['net_subsidy_service_mean'],
            general['net_margin_consumption_mean'],
            general['net_margin_service_mean'],
            general['omega_net_subsidy_consumption'],
            general['omega_net_subsidy_service'],
            general['omega_net_margin_consumption'],
            general['omega_net_margin_service']
        ],
        'Basic': [
            basic['net_subsidy_consumption_mean'],
            basic['net_subsidy_service_mean'],
            basic['net_margin_consumption_mean'],
            basic['net_margin_service_mean'],
            basic['omega_net_subsidy_consumption'],
            basic['omega_net_subsidy_service'],
            basic['omega_net_margin_consumption'],
            basic['omega_net_margin_service']
        ]
    }

    return pd.DataFrame(table_data)
