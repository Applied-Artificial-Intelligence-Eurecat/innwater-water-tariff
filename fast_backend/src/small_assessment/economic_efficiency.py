import numpy as np

from src.results.schemas import EconomicEfficiencyTable, EconomicEfficiencyRow
from src.small_assessment.new_calculator_service import NewSimulation


def economic_efficiency_dashboard(calculator: NewSimulation) -> EconomicEfficiencyTable:
    return EconomicEfficiencyTable(
        first_best=EconomicEfficiencyRow(
            conso=np.mean(calculator.first_tier_consumption_per_trim),
            delta_w=None
        ),
        delta_tbse_a=EconomicEfficiencyRow(
            conso=7.858,
            delta_w=-4.63,
        ),
        delta_ibt_a=EconomicEfficiencyRow(
            conso=-3.639,
            delta_w=-3.32,
        ),
        delta_ibt_pp_a=EconomicEfficiencyRow(
            conso=-6.017,
            delta_w=-6.14,
        ),
        impact_overconsumption=EconomicEfficiencyRow(
            conso=2.378,
            delta_w=2.38,
        )
    )
