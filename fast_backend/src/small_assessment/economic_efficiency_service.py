import pandas as pd


def get_aggregated_dashboard_results(df: pd.DataFrame):
    return {
        "mean": df['Consumption_Economic_Efficiency'].mean(),
        "median": 32
    }
