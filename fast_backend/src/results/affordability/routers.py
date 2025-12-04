from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import *
from ...core.auth import get_current_active_user
from ...core.database import get_db
from ...core.models import User
from ...initial.routers import get_simulation_payload_from_db
from ...small_assessment.effeco.gini_decomp import gini_decomp
from ...small_assessment.incentive_service import percentrank_inc, desvprom
from ...small_assessment.new_calculator_service import get_or_create_simulation_from_payload

affordability_router = APIRouter(prefix="/affordability",
                                 tags=["affordability"],
                                 responses={404: {"description": "Not found"}},
                                 )


def _create_gini_decomp_table(gini_data: dict) -> GiniDecompTable:
    """
    Convert raw Gini decomposition data into a structured GiniDecompTable.

    Args:
        gini_data: Dictionary containing Gini decomposition values

    Returns:
        GiniDecompTable with value and percentage fields populated
    """
    gini_total = gini_data.get('gini_total', 1.0)  # Avoid division by zero

    return GiniDecompTable(
        between=GiniDecompRow(
            value=gini_data.get('gini_between', 0.0) * 100,
            perc=(gini_data.get('gini_between', 0.0) / gini_total) * 100 if gini_total != 0 else 0.0
        ),
        within=GiniDecompRow(
            value=gini_data.get('gini_within', 0.0) * 100,
            perc=(gini_data.get('gini_within', 0.0) / gini_total) * 100 if gini_total != 0 else 0.0
        ),
        transvariation=GiniDecompRow(
            value=gini_data.get('gini_overlap', 0.0) * 100,
            perc=(gini_data.get('gini_overlap', 0.0) / gini_total) * 100 if gini_total != 0 else 0.0
        ),
        ensemble=GiniDecompRow(
            value=gini_data.get('gini_total', 0.0) * 100,
            perc=(gini_data.get('gini_total', 0.0) / gini_total) * 100 if gini_total != 0 else 0.0
        )
    )


@affordability_router.get("/{simulation_id}/gini_index_comparison")
async def gini_index_comparison(
        simulation_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
) -> OutputGiniDecomp:
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    is_sanitation = calculator.is_sanitation()

    # Process PAR IBT values
    par_ibt_gini_data = gini_decomp(calculator.par_ibt, is_sanitation)['gini_decomp']
    par_ibt_table = _create_gini_decomp_table(par_ibt_gini_data)

    # Process PAR TBSE values
    par_tbse_gini_data = gini_decomp(calculator.par_tbse, is_sanitation)['gini_decomp']
    par_tbse_table = _create_gini_decomp_table(par_tbse_gini_data)

    # Process excess PAR IBT values
    excess_par_ibt_gini_data = gini_decomp(
        calculator.par_ibt[calculator.ibt_par_excess > 0],
        is_sanitation[calculator.ibt_par_excess > 0]
    )['gini_decomp']
    excess_par_ibt_table = _create_gini_decomp_table(excess_par_ibt_gini_data)

    # Process excess PAR TBSE values (assuming this exists based on OutputGiniDecomp structure)
    excess_par_tbse_gini_data = gini_decomp(
        calculator.par_tbse[calculator.tbse_par_excess > 0],
        is_sanitation[calculator.tbse_par_excess > 0]
    )['gini_decomp']
    excess_par_tbse_table = _create_gini_decomp_table(excess_par_tbse_gini_data)

    return OutputGiniDecomp(
        par_ibt=par_ibt_table,
        par_tbse=par_tbse_table,
        excess_par_ibt=excess_par_ibt_table,
        excess_par_tbse=excess_par_tbse_table
    )


@affordability_router.get("/{simulation_id}/general_par_description")
async def general_par_description(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                  db: Session = Depends(get_db)) -> GeneralStatistic:
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    # Get PAR data for each group
    par_ibt_g1 = simulation_calculator.par_ibt[~simulation_calculator.is_sanitation()]
    par_ibt_g2 = simulation_calculator.par_ibt[simulation_calculator.is_sanitation()]
    par_tbse_g1 = simulation_calculator.par_tbse[~simulation_calculator.is_sanitation()]
    par_tbse_g2 = simulation_calculator.par_tbse[simulation_calculator.is_sanitation()]

    # Calculate delta values
    delta_par_g1 = par_ibt_g1 - par_tbse_g1
    delta_par_g2 = par_ibt_g2 - par_tbse_g2

    return GeneralStatistic(
        mean=AugmentedGeneralRow(
            par_ibt_g1=par_ibt_g1.mean(),
            par_ibt_g2=par_ibt_g2.mean(),
            par_tbse_g1=par_tbse_g1.mean(),
            par_tbse_g2=par_tbse_g2.mean(),
            delta_par_g1=delta_par_g1.mean(),
            delta_par_g2=delta_par_g2.mean(),
        ),
        median=AugmentedGeneralRow(
            par_ibt_g1=par_ibt_g1.median(),
            par_ibt_g2=par_ibt_g2.median(),
            par_tbse_g1=par_tbse_g1.median(),
            par_tbse_g2=par_tbse_g2.median(),
            delta_par_g1=delta_par_g1.median(),
            delta_par_g2=delta_par_g2.median(),
        ),
        min=GeneralRow(
            par_ibt_g1=par_ibt_g1.min(),
            par_ibt_g2=par_ibt_g2.min(),
            par_tbse_g1=par_tbse_g1.min(),
            par_tbse_g2=par_tbse_g2.min(),
        ),
        max=GeneralRow(
            par_ibt_g1=par_ibt_g1.max(),
            par_ibt_g2=par_ibt_g2.max(),
            par_tbse_g1=par_tbse_g1.max(),
            par_tbse_g2=par_tbse_g2.max(),
        ),
        q1=GeneralRow(
            par_ibt_g1=par_ibt_g1.quantile(0.25),
            par_ibt_g2=par_ibt_g2.quantile(0.25),
            par_tbse_g1=par_tbse_g1.quantile(0.25),
            par_tbse_g2=par_tbse_g2.quantile(0.25),
        ),
        q3=GeneralRow(
            par_ibt_g1=par_ibt_g1.quantile(0.75),
            par_ibt_g2=par_ibt_g2.quantile(0.75),
            par_tbse_g1=par_tbse_g1.quantile(0.75),
            par_tbse_g2=par_tbse_g2.quantile(0.75),
        ),
        d1=GeneralRow(
            par_ibt_g1=par_ibt_g1.quantile(0.1),
            par_ibt_g2=par_ibt_g2.quantile(0.1),
            par_tbse_g1=par_tbse_g1.quantile(0.1),
            par_tbse_g2=par_tbse_g2.quantile(0.1),
        ),
        d9=GeneralRow(
            par_ibt_g1=par_ibt_g1.quantile(0.9),
            par_ibt_g2=par_ibt_g2.quantile(0.9),
            par_tbse_g1=par_tbse_g1.quantile(0.9),
            par_tbse_g2=par_tbse_g2.quantile(0.9),
        ),
        f=GeneralRow(
            par_ibt_g1=percentrank_inc(par_ibt_g1, par_ibt_g1.mean()),
            par_ibt_g2=percentrank_inc(par_ibt_g2, par_ibt_g2.mean()),
            par_tbse_g1=percentrank_inc(par_tbse_g1, par_tbse_g1.mean()),
            par_tbse_g2=percentrank_inc(par_tbse_g2, par_tbse_g2.mean()),
        ),
        variance=GeneralRow(
            par_ibt_g1=par_ibt_g1.var(),
            par_ibt_g2=par_ibt_g2.var(),
            par_tbse_g1=par_tbse_g1.var(),
            par_tbse_g2=par_tbse_g2.var(),
        ),
        ecart_type=GeneralRow(
            par_ibt_g1=par_ibt_g1.std(),
            par_ibt_g2=par_ibt_g2.std(),
            par_tbse_g1=par_tbse_g1.std(),
            par_tbse_g2=par_tbse_g2.std(),
        ),
        MAPE=GeneralRow(
            par_ibt_g1=desvprom(par_ibt_g1),
            par_ibt_g2=desvprom(par_ibt_g2),
            par_tbse_g1=desvprom(par_tbse_g1),
            par_tbse_g2=desvprom(par_tbse_g2),
        ),
        coeff_variation=GeneralRow(
            par_ibt_g1=par_ibt_g1.std() / par_ibt_g1.mean() if par_ibt_g1.mean() != 0 else 0,
            par_ibt_g2=par_ibt_g2.std() / par_ibt_g2.mean() if par_ibt_g2.mean() != 0 else 0,
            par_tbse_g1=par_tbse_g1.std() / par_tbse_g1.mean() if par_tbse_g1.mean() != 0 else 0,
            par_tbse_g2=par_tbse_g2.std() / par_tbse_g2.mean() if par_tbse_g2.mean() != 0 else 0,
        ),
    )
