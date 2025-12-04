from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User
from src.initial.routers import get_simulation_payload_from_db
from src.small_assessment.calculator_service import SimulationFinished
from src.small_assessment.incentive_service import delta_incentive_effect_consumption, incentive_effect_consumption, \
    overconsumption_decomposition, overconsumption_decomposition_variance, composition_of_households_that_overconsume, \
    breakdown_of_overconsumption, decomposition_table, increase_contingency_table_household_percentage, \
    decrease_contingency_table_household_percentage, increase_contingency_table_consumption
from src.small_assessment.new_calculator_service import get_or_create_simulation_from_payload

incentive_effect_router = APIRouter(
    prefix="/incentive",
    tags=["incentive"],
    responses={404: {"description": "Not found"}},
)




@incentive_effect_router.get("/{simulation_id}/general_description")
async def incentive_effec_general_description(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                              db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return incentive_effect_consumption(new_simulation)


@incentive_effect_router.get("/{simulation_id}/delta_general_description")
async def delta_incentive_effect_description(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                             db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return delta_incentive_effect_consumption(new_simulation)


# Volet decomposition

@incentive_effect_router.get("/{simulation_id}/decomposition_tables")
async def get_decomposition_tables(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                   db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    result = decomposition_table(new_simulation)
    return result


# Contingency tables

@incentive_effect_router.get("/{simulation_id}/contingency_table_percentages")
async def get_contingency_table_percentages(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                            db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return {
        "increase": increase_contingency_table_household_percentage(new_simulation),
        "decrease": decrease_contingency_table_household_percentage(new_simulation)
    }


@incentive_effect_router.get("/{simulation_id}/contingency_table_consumption")
async def get_contingency_table_consumption(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                            db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return {
        "increase": increase_contingency_table_consumption(new_simulation),
        "decrease": decrease_contingency_table_household_percentage(new_simulation)
    }


# Surconso decompositivon


@incentive_effect_router.get("/{simulation_id}/overconsumption_decomposition")
async def get_overconsumption_decomposition(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                            db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    decomposed = overconsumption_decomposition(new_simulation)
    vintra_groups = overconsumption_decomposition_variance(decomposed.households_percentage, decomposed.g1,
                                                           decomposed.g2)
    vintra_poors = overconsumption_decomposition_variance(decomposed.households_percentage, decomposed.poor,
                                                          decomposed.nonpoor)
    return {
        "decomposed": decomposed,
        "groups_variance": vintra_groups,
        "poor_variance": vintra_poors,
    }


# Composition des menages qui surconso

@incentive_effect_router.get("/{simulation_id}/households_that_overconsume_composition")
async def get_composition_of_households_that_overconsume(simulation_id: int,
                                                         current_user: User = Depends(get_current_active_user),
                                                         db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return composition_of_households_that_overconsume(new_simulation)


@incentive_effect_router.get("/{simulation_id}/breakdown_of_overconsumption_composition")
async def get_breakdown_of_overconsumption(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                           db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    new_simulation = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    return breakdown_of_overconsumption(new_simulation)
