import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User
from src.initial.routers import get_simulation_payload_from_db
from src.results.schemas import EconomicEfficiencyDetailsTable, SurplusDeltaRow, \
    SurplusImpactRow
from src.small_assessment.new_calculator_service import get_or_create_simulation_from_payload

economic_efficiency_router = APIRouter(
    prefix="",
    tags=["economic_efficiency"],
    responses={404: {"description": "Not found"}},
)


@economic_efficiency_router.get("/{simulation_id}/economic_efficiency/details",
                                response_model=EconomicEfficiencyDetailsTable)
async def get_economic_efficiency_details(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                          db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    ibt_win = simulation_calculator.ibt_surplus_consumption > 0
    ibt_lose = simulation_calculator.ibt_surplus_consumption <= 0
    ibt_pp_win = simulation_calculator.ibt_pp_surplus_consumption > 0
    ibt_pp_lose = simulation_calculator.ibt_pp_surplus_consumption <= 0
    print((simulation_calculator.ibt_a_consumption_per_trim - simulation_calculator.ibt_pp_a_consumption_per_trim)[0])
    result = EconomicEfficiencyDetailsTable(ibt_a_delta=SurplusDeltaRow(total_percent=100.0,
                                                                        g_percent=(ibt_win).sum() * 100 / len(
                                                                            simulation_calculator.df),
                                                                        p_percent=(ibt_lose).sum() * 100 / len(
                                                                            simulation_calculator.df),
                                                                        total_value=np.mean(
                                                                            simulation_calculator.ibt_surplus_consumption),
                                                                        g_value=np.mean(
                                                                            simulation_calculator.ibt_surplus_consumption[
                                                                                ibt_win]), p_value=np.mean(
            simulation_calculator.ibt_surplus_consumption[ibt_lose])),
                                            ibt_a_pp_delta=SurplusDeltaRow(total_percent=100.0,
                                                                           g_percent=(ibt_pp_win).sum() * 100 / len(
                                                                               simulation_calculator.df),
                                                                           p_percent=(ibt_pp_lose).sum() * 100 / len(
                                                                               simulation_calculator.df),
                                                                           total_value=np.mean(
                                                                               simulation_calculator.ibt_pp_surplus_consumption),
                                                                           g_value=np.mean(
                                                                               simulation_calculator.ibt_pp_surplus_consumption[
                                                                                   ibt_win]), p_value=np.mean(
                                                    simulation_calculator.ibt_pp_surplus_consumption[ibt_lose])),
                                            impact_on_sur_co=SurplusImpactRow(
                                                total=np.mean(simulation_calculator.delta_ibt_surplus_consumption),
                                                overconsumers=np.mean(
                                                    simulation_calculator.delta_ibt_surplus_consumption[
                                                        simulation_calculator.overconsumption > 0]))
                                            )
    print(result)
    return result
