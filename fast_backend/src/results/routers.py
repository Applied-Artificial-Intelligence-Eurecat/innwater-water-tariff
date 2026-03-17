from io import StringIO

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User
from src.initial.routers import get_simulation_payload_from_db
from src.results.affordability.routers import affordability_router
from src.results.economic_efficiency.routers import economic_efficiency_router
from src.results.incentive.routers import incentive_effect_router
from src.results.schemas import *
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.economic_efficiency import economic_efficiency_dashboard
from src.small_assessment.incentive_service import incentive_effect_consumption
from src.small_assessment.new_calculator_service import get_or_create_simulation_from_payload, NewSimulation
from src.small_assessment.rex_service import calculate_net_cost_service
from src.results.equity.equity_indicators import calculate_full_equity_indicators

from src.results.schemas import EconomicEfficiencyTable

results_router = APIRouter(
    prefix="/results",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)

results_router.include_router(incentive_effect_router, tags=["incentive_effect"])
results_router.include_router(economic_efficiency_router, tags=["economic_efficiency"])


@results_router.get("/{simulation_id}/affordability", response_model=AffordabilityTable)
async def get_affordability_indicators(simulation_id, current_user: User = Depends(get_current_active_user),
                                       db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    result = affordability_general(simulation_finished)

    return AffordabilityTable(
        headcount_ratio=AffordabilityColumnValues(
            ibt=round(result.headcount_ratio.ibt, 2),
            tbse=round(result.headcount_ratio.tbse, 2),
        ),
        apparent_affordability_deficit=AffordabilityColumnValues(
            ibt=round(result.aparent_deficit.ibt, 2),
            tbse=round(result.aparent_deficit.tbse, 2),
        ),
        effective_affordability_deficit=AffordabilityColumnValues(
            ibt=round(result.efective_deficit.ibt, 2),
            tbse=round(result.efective_deficit.tbse, 2),
        ),
        gini_app=AffordabilityColumnValues(
            ibt=round(result.gini_index.ibt, 2),
            tbse=round(result.gini_index.tbse, 2),
        ),
        gini_eff=AffordabilityColumnValues(
            ibt=round(0.725, 2),
            tbse=round(0.355, 2),
        )
    )


@results_router.get("/{simulation_id}/incentive/consumption", response_model=IncentiveConsumptionTable)
async def get_incentive_consumption(simulation_id, current_user: User = Depends(get_current_active_user),
                                    db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    incentive_effect_consumption_result = incentive_effect_consumption(simulation_finished)
    consumption_table = IncentiveConsumptionTable(
        ibt=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.ibt,
                              average_bill_eur_trim=simulation_finished.ibt_bcp_receipt.mean()),
        ibt_pp=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.ibt_pp,
                                 average_bill_eur_trim=simulation_finished.ibt_pp_receipt.mean()),
        ibt_tbse=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.tbse,
                                   average_bill_eur_trim=simulation_finished.tbse_tbse_consumption_receipt.mean()),
    )
    return consumption_table


@results_router.get("/{simulation_id}/incentive/efficiency", response_model=IncentiveEfficiencyTable)
async def get_incentive_efficiency(simulation_id, current_user: User = Depends(get_current_active_user),
                                   db: Session = Depends(get_db)):
    efficiency_table = IncentiveEfficiencyTable(
        per_h=EfficiencyMetrics(eff_overconsumption=None, eff_mismanagement_cost=None),
        per_ind=EfficiencyMetrics(eff_overconsumption=None, eff_mismanagement_cost=None),
    )
    return efficiency_table




@results_router.get("/{simulation_id}/equity/gini", response_model=EquityGiniIndexTable)
async def get_equity_gini_index(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)):
    return EquityGiniIndexTable(
        ibt=None,
        ibt_ae=None,
        tbse=None
    )


@results_router.get("/{simulation_id}/equity/basic_consumption", response_model=BasicConsumptionEquityTable)
async def get_basic_consumption_equity(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                       db: Session = Depends(get_db)):
    from src.results.equity.calculation_service import calculate_equity_from_simulation

    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    equity_indicators = calculate_equity_from_simulation(simulation_calculator)
    basic_indicators = equity_indicators['basic']

    return BasicConsumptionEquityTable(
        net_sub_basic_c=BasicConsumptionEquityRow(
            dae=round(basic_indicators['net_subsidy_consumption_mean'], 2),
            dai=round(basic_indicators['net_subsidy_service_mean'], 2)
        ),
        omega_ratio_1=BasicConsumptionEquityRow(
            dae=round(basic_indicators['omega_net_subsidy_consumption'], 2),
            dai=round(basic_indicators['omega_net_subsidy_service'], 2)
        ),
        net_taxes_basic_c=BasicConsumptionEquityRow(
            dae=round(basic_indicators['net_margin_consumption_mean'], 2),
            dai=round(basic_indicators['net_margin_service_mean'], 2)
        ),
        omega_ratio_2=BasicConsumptionEquityRow(
            dae=round(basic_indicators['omega_net_margin_consumption'], 2),
            dai=round(basic_indicators['omega_net_margin_service'], 2)
        ),
    )


@results_router.get("/{simulation_id}/equity/full_consumption", response_model=FullConsumptionEquityTable)
async def get_full_consumption_equity(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                      db: Session = Depends(get_db)):
    from src.results.equity.calculation_service import calculate_equity_from_simulation

    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    equity_indicators = calculate_equity_from_simulation(simulation_calculator)
    general_indicators = equity_indicators['general']

    return FullConsumptionEquityTable(
        net_sub_c=FullConsumptionEquityRow(
            afe=round(general_indicators['net_subsidy_consumption_mean'], 2),
            afi=round(general_indicators['net_subsidy_service_mean'], 2)
        ),
        omega_ratio_1=FullConsumptionEquityRow(
            afe=round(general_indicators['omega_net_subsidy_consumption'], 2),
            afi=round(general_indicators['omega_net_subsidy_service'], 2)
        ),
        net_taxation=FullConsumptionEquityRow(
            afe=round(general_indicators['net_margin_consumption_mean'], 2),
            afi=round(general_indicators['net_margin_service_mean'], 2)
        ),
        omega_ratio_2=FullConsumptionEquityRow(
            afe=round(general_indicators['omega_net_margin_consumption'], 2),
            afi=round(general_indicators['omega_net_margin_service'], 2)
        ),
    )


@results_router.get("/{simulation_id}/funding/rex_op")
async def get_rex_op_funding(simulation_id: int, current_user: User = Depends(get_current_active_user),
                             db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calcuator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    return calculate_rex(simulation_calcuator)


def calculate_rex(simulation_calculator: NewSimulation):
    simulation_payload = simulation_calculator.simulation

    print("SANITATION")
    net_sanitation, sanitation_total_charges = calculate_net_cost_service(
        num_subscribers=simulation_payload.primitives.sanitation.number_of_subscribers,
        charge_fix=simulation_payload.tariff.sanitation.subscription,
        social_sampling_rate=simulation_calculator.is_sanitation().sum(),
        total_group_subscription_fee=simulation_calculator.sanitation_ibt_bcp_consumption_receipt.sum(),
        only_subscription_fee=simulation_calculator.is_sanitation().sum() * simulation_payload.tariff.sanitation.subscription,
        potential_consumption_base=(simulation_calculator.bcp_consumptions[
                                        simulation_payload.launch.periods] * simulation_calculator.is_sanitation()).sum(),
        taxation_group_fees=simulation_payload.primitives.sanitation.variable_costs,
        fixed_costs=simulation_payload.primitives.sanitation.fixed_costs)
    print(net_sanitation, sanitation_total_charges)
    print("POOTABLE WATER")
    net_potable_water, net_potable_total_charges = calculate_net_cost_service(
        num_subscribers=simulation_payload.primitives.drinking_water.number_of_subscribers,
        charge_fix=simulation_payload.tariff.drinking_water.subscription,
        social_sampling_rate=len(simulation_calculator.df),
        total_group_subscription_fee=simulation_calculator.potable_water_ibt_bcp_consumption_receipt.sum(),
        only_subscription_fee=len(simulation_calculator.df) * simulation_payload.tariff.drinking_water.subscription,
        potential_consumption_base=(simulation_calculator.bcp_consumptions[simulation_payload.launch.periods]).sum(),
        taxation_group_fees=simulation_payload.primitives.drinking_water.variable_costs,
        fixed_costs=simulation_payload.primitives.drinking_water.fixed_costs)
    print(net_potable_water, net_potable_total_charges)
    return {
        "general": net_sanitation + net_potable_water,
        "total_cost": (net_sanitation + net_potable_water) / (
                sanitation_total_charges + net_potable_total_charges) * 100,
    }


@results_router.get("/{simulation_id}/funding/other")
async def get_other_funding(simulation_id: int, current_user: User = Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    return FundingTable(
        net_contributors_percent=42.1,
        net_beneficiaries_percent=57.9,
        subsidized_basic_c_percent=47.3,
        subsidized_non_basic_c_percent=4.2,
        margined_c_percent=77.6,
        bad_sub_percent=FundingMetricRow(dae=10.7, dai=0.0),
        bad_tax_percent=FundingMetricRow(dae=17.9, dai=17.9)
    )


@results_router.get("/{simulation_id}/environmental_cost")
async def get_environmental_cost(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):

    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    return EnvironmentalCostTable(
        tbse_conso_rang_1=np.mean(simulation_calculator.first_tier_env_cost),
        effective_tbse=np.mean(simulation_calculator.tbse_env_cost),
        ibt=np.mean(simulation_calculator.ibt_env_cost),
        ibt_pp=np.mean(simulation_calculator.ibt_pp_env_cost),
    )


@results_router.get("/{simulation_id}/water_agency")
async def get_water_agency(simulation_id: int, current_user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    return WaterAgencyTable(
        exercise_duty=simulation_calculator.water_agency_exercise_duty,
    )


@results_router.get("/{simulation_id}/state")
async def get_state_table(simulation_id: int, current_user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)
    return StateTable(
        vat=simulation_calculator.state_avt_total
    )


@results_router.get("/{simulation_id}/csv")
async def get_csv_results(simulation_id: int, current_user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id, get_simulation_db=True)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, payload)
    csv_buffer = StringIO()

    # Escribir el CSV al buffer
    df = simulation_finished.get_df()
    df.to_csv(csv_buffer, index=False)

    # Mover el cursor al inicio del buffer
    csv_buffer.seek(0)
    from fastapi.responses import StreamingResponse

    # Retornar como StreamingResponse
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=simulation_{simulation_id}_results.csv"}
    )


@results_router.get("/{simulation_id}/economic_efficiency", response_model=EconomicEfficiencyTable)
async def get_economic_efficiency(simulation_id: int, current_user: User = Depends(get_current_active_user),
                              db: Session = Depends(get_db)):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                      get_simulation_db=True)
    simulation_finished = await get_or_create_simulation_from_payload(simulation.id, simulation, simulation_payload)

    return economic_efficiency_dashboard(simulation_finished)

results_router.include_router(affordability_router)
