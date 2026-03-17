"""
Service layer for calculating gross subsidies and margins from NewSimulation data.

This module extracts the necessary data from NewSimulation and prepares it
for equity indicator calculations.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

from src.results.equity.equity_indicators import calculate_full_equity_indicators
from src.small_assessment.new_calculator_service import NewSimulation


def calculate_gross_subsidy_consumption_afe(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross subsidies on consumption (Access Fee Excluded).

    This represents subsidies on variable consumption only, excluding the subscription/access fee.
    """
    # Use the difference between first tier (efficient) cost and actual consumption cost
    # Only where the user pays less than the efficient cost
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    consumption = simulation.bcp_consumptions[simulation.simulation.launch.periods]

    # Efficient cost for their consumption
    efficient_total = consumption * efficient_cost_per_m3

    # Actual consumption payment (excluding subscription)
    actual_consumption_payment = simulation.potable_water_ibt_bcp_consumption_receipt

    # Subsidy is when efficient cost > actual payment
    gross_subsidy = (efficient_total - actual_consumption_payment).clip(lower=0)

    return gross_subsidy


def calculate_gross_subsidy_service_afi(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross subsidies on EP/EPA service (Access Fee Included).

    This includes subsidies on both consumption and subscription.
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    consumption = simulation.bcp_consumptions[simulation.simulation.launch.periods]

    # Efficient cost for their consumption plus fixed costs allocation
    num_subscribers = simulation.simulation.primitives.drinking_water.number_of_subscribers
    efficient_subscription = simulation.simulation.primitives.drinking_water.fixed_costs / (num_subscribers * 4)

    efficient_total = consumption * efficient_cost_per_m3 + efficient_subscription

    # Actual total payment (including subscription)
    actual_total_payment = simulation.potable_water_ibt_bcp_receipt

    # Subsidy is when efficient cost > actual payment
    gross_subsidy = (efficient_total - actual_total_payment).clip(lower=0)

    return gross_subsidy


def calculate_gross_margin_consumption_afe(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross margins/taxes on consumption (Access Fee Excluded).

    This represents the margin when users pay more than the efficient cost (variable only).
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    consumption = simulation.bcp_consumptions[simulation.simulation.launch.periods]

    # Efficient cost for their consumption
    efficient_total = consumption * efficient_cost_per_m3

    # Actual consumption payment (excluding subscription)
    actual_consumption_payment = simulation.potable_water_ibt_bcp_consumption_receipt

    # Margin is when actual payment > efficient cost
    gross_margin = (actual_consumption_payment - efficient_total).clip(lower=0)

    return gross_margin


def calculate_gross_margin_service_afi(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross margins/taxes on EP/EPA service (Access Fee Included).

    This includes margins on both consumption and subscription.
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    consumption = simulation.bcp_consumptions[simulation.simulation.launch.periods]

    # Efficient cost for their consumption plus fixed costs allocation
    num_subscribers = simulation.simulation.primitives.drinking_water.number_of_subscribers
    efficient_subscription = simulation.simulation.primitives.drinking_water.fixed_costs / (num_subscribers * 4)

    efficient_total = consumption * efficient_cost_per_m3 + efficient_subscription

    # Actual total payment (including subscription)
    actual_total_payment = simulation.potable_water_ibt_bcp_receipt

    # Margin is when actual payment > efficient cost
    gross_margin = (actual_total_payment - efficient_total).clip(lower=0)

    return gross_margin


def calculate_gross_subsidy_basic_consumption_dae(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross subsidies on basic consumption (Access Fee Excluded).

    Basic consumption is typically the first tier or essential consumption level.
    """
    # Use base consumption as "basic consumption"
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    base_consumption = simulation.base_consumption_per_trim

    # Calculate what they would pay for base consumption with current tariff
    # We need to calculate the bill for base_consumption using the tariff structure
    from src.small_assessment.new_calculator_service import decompose_value

    thresholds_ep = [t.threshold for t in simulation.simulation.tariff.drinking_water.usage_tiers]

    actual_base_payments = []
    for consumption_value in base_consumption:
        payment = 0
        for ttc_tier, consumption_tier in zip(simulation.simulation.potable_water_prix_tiers_ttc,
                                              decompose_value(consumption_value, thresholds_ep)):
            payment += consumption_tier * ttc_tier
        actual_base_payments.append(payment)

    actual_base_payment = pd.Series(actual_base_payments, index=simulation.df.index)

    # Efficient cost for base consumption
    efficient_total = base_consumption * efficient_cost_per_m3

    # Subsidy is when efficient cost > actual payment
    gross_subsidy = (efficient_total - actual_base_payment).clip(lower=0)

    return gross_subsidy


def calculate_gross_subsidy_basic_service_dai(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross subsidies on basic service (Access Fee Included).
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    base_consumption = simulation.base_consumption_per_trim

    # Calculate actual payment including subscription
    from src.small_assessment.new_calculator_service import decompose_value

    thresholds_ep = [t.threshold for t in simulation.simulation.tariff.drinking_water.usage_tiers]

    actual_base_payments = []
    for consumption_value in base_consumption:
        payment = simulation.simulation.tariff.drinking_water.subscription
        for ttc_tier, consumption_tier in zip(simulation.simulation.potable_water_prix_tiers_ttc,
                                              decompose_value(consumption_value, thresholds_ep)):
            payment += consumption_tier * ttc_tier
        actual_base_payments.append(payment)

    actual_base_payment = pd.Series(actual_base_payments, index=simulation.df.index)

    # Efficient cost plus subscription allocation
    num_subscribers = simulation.simulation.primitives.drinking_water.number_of_subscribers
    efficient_subscription = simulation.simulation.primitives.drinking_water.fixed_costs / (num_subscribers * 4)
    efficient_total = base_consumption * efficient_cost_per_m3 + efficient_subscription

    # Subsidy is when efficient cost > actual payment
    gross_subsidy = (efficient_total - actual_base_payment).clip(lower=0)

    return gross_subsidy


def calculate_gross_margin_basic_consumption_dae(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross margins on basic consumption (Access Fee Excluded).
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    base_consumption = simulation.base_consumption_per_trim

    # Calculate actual payment for base consumption
    from src.small_assessment.new_calculator_service import decompose_value

    thresholds_ep = [t.threshold for t in simulation.simulation.tariff.drinking_water.usage_tiers]

    actual_base_payments = []
    for consumption_value in base_consumption:
        payment = 0
        for ttc_tier, consumption_tier in zip(simulation.simulation.potable_water_prix_tiers_ttc,
                                              decompose_value(consumption_value, thresholds_ep)):
            payment += consumption_tier * ttc_tier
        actual_base_payments.append(payment)

    actual_base_payment = pd.Series(actual_base_payments, index=simulation.df.index)

    # Efficient cost for base consumption
    efficient_total = base_consumption * efficient_cost_per_m3

    # Margin is when actual payment > efficient cost
    gross_margin = (actual_base_payment - efficient_total).clip(lower=0)

    return gross_margin


def calculate_gross_margin_basic_service_dai(simulation: NewSimulation) -> pd.Series:
    """
    Calculate gross margins on basic service (Access Fee Included).
    """
    efficient_cost_per_m3 = (simulation.simulation.primitives.drinking_water.variable_costs +
                             simulation.simulation.primitives.environment.average_variable_cost)

    base_consumption = simulation.base_consumption_per_trim

    # Calculate actual payment including subscription
    from src.small_assessment.new_calculator_service import decompose_value

    thresholds_ep = [t.threshold for t in simulation.simulation.tariff.drinking_water.usage_tiers]

    actual_base_payments = []
    for consumption_value in base_consumption:
        payment = simulation.simulation.tariff.drinking_water.subscription
        for ttc_tier, consumption_tier in zip(simulation.simulation.potable_water_prix_tiers_ttc,
                                              decompose_value(consumption_value, thresholds_ep)):
            payment += consumption_tier * ttc_tier
        actual_base_payments.append(payment)

    actual_base_payment = pd.Series(actual_base_payments, index=simulation.df.index)

    # Efficient cost plus subscription allocation
    num_subscribers = simulation.simulation.primitives.drinking_water.number_of_subscribers
    efficient_subscription = simulation.simulation.primitives.drinking_water.fixed_costs / (num_subscribers * 4)
    efficient_total = base_consumption * efficient_cost_per_m3 + efficient_subscription

    # Margin is when actual payment > efficient cost
    gross_margin = (actual_base_payment - efficient_total).clip(lower=0)

    return gross_margin


def calculate_equity_from_simulation(simulation: NewSimulation) -> Dict[str, Any]:
    """
    Main function to calculate all equity indicators from a NewSimulation object.

    Args:
        simulation: NewSimulation object with calculated consumption and receipts

    Returns:
        Dictionary with both basic and full consumption equity indicators
    """
    # Calculate gross subsidies and margins for general consumption/service
    gross_subsidy_consumption = calculate_gross_subsidy_consumption_afe(simulation)
    gross_subsidy_service = calculate_gross_subsidy_service_afi(simulation)
    gross_margin_consumption = calculate_gross_margin_consumption_afe(simulation)
    gross_margin_service = calculate_gross_margin_service_afi(simulation)

    # Calculate gross subsidies and margins for basic consumption/service
    gross_subsidy_basic_consumption = calculate_gross_subsidy_basic_consumption_dae(simulation)
    gross_subsidy_basic_service = calculate_gross_subsidy_basic_service_dai(simulation)
    gross_margin_basic_consumption = calculate_gross_margin_basic_consumption_dae(simulation)
    gross_margin_basic_service = calculate_gross_margin_basic_service_dai(simulation)

    # Calculate equity indicators
    equity_indicators = calculate_full_equity_indicators(
        gross_subsidy_consumption=gross_subsidy_consumption,
        gross_subsidy_service=gross_subsidy_service,
        gross_margin_consumption=gross_margin_consumption,
        gross_margin_service=gross_margin_service,
        gross_subsidy_basic_consumption=gross_subsidy_basic_consumption,
        gross_subsidy_basic_service=gross_subsidy_basic_service,
        gross_margin_basic_consumption=gross_margin_basic_consumption,
        gross_margin_basic_service=gross_margin_basic_service,
        is_poor=simulation.is_poor
    )

    return equity_indicators
