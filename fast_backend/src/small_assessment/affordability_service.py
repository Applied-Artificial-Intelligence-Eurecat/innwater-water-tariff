import numpy as np
from pydantic import BaseModel

from src.small_assessment.new_calculator_service import NewSimulation


class AffordabilityRow(BaseModel):
    ibt: float
    tbse: float


class AffordabilityGeneral(BaseModel):
    """
    Attributes:
        headcount_ratio: Represents the headcount ratio as an affordability metric.
        aparent_deficit: Represents the apparent deficit as an affordability metric.
        efective_deficit: Represents the effective deficit as an affordability metric.
        gini_index: Represents the Gini index as an affordability metric.
    """
    headcount_ratio: AffordabilityRow
    aparent_deficit: AffordabilityRow
    efective_deficit: AffordabilityRow
    gini_index: AffordabilityRow


def affordability_general(simulation: NewSimulation) -> AffordabilityGeneral:
    cov_ibt = np.cov(simulation.ibt_par_excess, simulation.ibt_par_excess_rank, bias=True)[0, 1]
    cov_tbse = np.cov(simulation.tbse_par_excess, simulation.tbse_par_excess_rank, bias=True)[0, 1]
    return AffordabilityGeneral(
        headcount_ratio=AffordabilityRow(
            ibt=simulation.ibt_par_headcount.sum() * 100 / len(simulation.ibt_par_headcount),
            tbse=simulation.tbse_par_headcount.sum() * 100 / len(simulation.tbse_par_headcount),
        ),
        aparent_deficit=AffordabilityRow(
            ibt=simulation.ibt_par_excess.mean(),
            tbse=simulation.tbse_par_excess.mean()
        ),
        efective_deficit=AffordabilityRow(
            ibt=simulation.ibt_par_excess[simulation.ibt_par_excess > 0].mean(),
            tbse=simulation.tbse_par_excess[simulation.tbse_par_excess > 0].mean()
        ),
        gini_index=AffordabilityRow(
            ibt=2 * cov_ibt / simulation.ibt_par_excess.mean(),
            tbse=2 * cov_tbse / simulation.tbse_par_excess.mean()
        )
    )
