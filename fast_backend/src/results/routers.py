from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User
from src.initial.routers import get_simulation_payload_from_db
from src.initial.schemas import GetSimulationPayload
from src.results.affordability.routers import affordability_router
from src.results.incentive.routers import incentive_effect_router
from src.results.schemas import *
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.calculator_service import SimulationFinished
from src.small_assessment.incentive_service import incentive_effect_consumption
from src.small_assessment.rex_service import calculate_net_cost_service

results_router = APIRouter(
    prefix="/results",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)

results_router.include_router(incentive_effect_router, tags=["incentive_effect"])


@results_router.get("/{simulation_id}/affordability", response_model=AffordabilityTable)
async def get_affordability_indicators(simulation_id, current_user: User = Depends(get_current_active_user),
                                       db: Session = Depends(get_db)):
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = SimulationFinished(simulation_id, simulation_payload)

    result = affordability_general(simulation_finished.df)

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
    simulation_payload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = SimulationFinished(simulation_id, simulation_payload)

    incentive_effect_consumption_result = incentive_effect_consumption(simulation_finished.df)
    print(list(simulation_finished.df.columns))
    consumption_table = IncentiveConsumptionTable(
        ibt=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.ibt,
                              average_bill_eur_trim=simulation_finished.ibt_c_bcp_co(simulation_finished.df).mean()),
        ibt_pp=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.ibt_pp,
                                 average_bill_eur_trim=simulation_finished.df['Facture IBT C PP CO'].mean()),
        ibt_tbse=ConsumptionValues(average_consumption_m3_trim=incentive_effect_consumption_result.mean.tbse,
                                   average_bill_eur_trim=simulation_finished.bill_bl_tbse().mean()),
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


@results_router.get("/{simulation_id}/economic_efficiency", response_model=EconomicEfficiencyTable)
async def get_economic_efficiency(simulation_id, current_user: User = Depends(get_current_active_user),
                                  db: Session = Depends(get_db)):
    efficiency_table = EconomicEfficiencyTable(
        first_best=EconomicEfficiencyRow(conso=None, delta_w=None),  # '***' → None
        delta_ibt_pp=EconomicEfficiencyRow(conso=None, delta_w=None),
        impact_sur_co=EconomicEfficiencyRow(conso=None, delta_w=None),
        delta_tbse=EconomicEfficiencyRow(conso=None, delta_w=None),
        delta_surplus_m=EconomicEfficiencyRow(conso=None, delta_w=None)
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
    return BasicConsumptionEquityTable(
        net_sub_basic_c=BasicConsumptionEquityRow(dae=None, dai=None),
        omega_ratio_1=BasicConsumptionEquityRow(dae=None, dai=None),
        net_taxes_basic_c=BasicConsumptionEquityRow(dae=None, dai=None),
        omega_ratio_2=BasicConsumptionEquityRow(dae=None, dai=None),
    )


@results_router.get("/{simulation_id}/equity/full_consumption", response_model=FullConsumptionEquityTable)
async def get_full_consumption_equity(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                      db: Session = Depends(get_db)):
    return FullConsumptionEquityTable(
        net_sub_c=FullConsumptionEquityRow(afe=None, afi=None),
        omega_ratio_1=FullConsumptionEquityRow(afe=None, afi=None),
        net_taxation=FullConsumptionEquityRow(afe=None, afi=None),
        omega_ratio_2=FullConsumptionEquityRow(afe=None, afi=None),
    )


@results_router.get("/{simulation_id}/funding/rex_op")
async def get_rex_op_funding(simulation_id: int, current_user: User = Depends(get_current_active_user),
                             db: Session = Depends(get_db)):
    simulation_payload: GetSimulationPayload = await get_simulation_payload_from_db(current_user, db, simulation_id)
    simulation_finished = SimulationFinished(simulation_id, simulation_payload)

    return await calculate_rex(simulation_finished, simulation_payload)


async def calculate_rex(simulation_finished, simulation_payload):
    df = simulation_finished.df
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    social_sampling_rate = len(g2_df)
    total_subscription_yearly_fee = (
            df['Assainissement Collectif (1 = oui)'] * simulation_payload.tariff.sanitation.subscription).sum()
    result = affordability_general(df)
    print("SANITATION")
    net_sanitation, sanitation_total_charges = calculate_net_cost_service(
        simulation_payload.primitives.sanitation.number_of_subscribers,
        simulation_payload.tariff.sanitation.subscription,
        social_sampling_rate,
        df['Facture_IBT_C_BCP AT'].sum(),
        simulation_finished.total_tariff_sanitation_subscription_fee(),
        simulation_finished.only_subscription_tariff_sanitation_subscription_fee(),
        simulation_payload.primitives.sanitation.variable_costs,
        simulation_payload.primitives.sanitation.fixed_costs)
    print(net_sanitation, sanitation_total_charges)
    print("POOTABLE WATER")
    net_potable_water, net_potable_total_charges = calculate_net_cost_service(
        simulation_payload.primitives.drinking_water.number_of_subscribers,
        simulation_payload.tariff.drinking_water.subscription,
        len(df),
        simulation_finished.total_tariff_potable_water_subscription_fee(),
        simulation_finished.only_subscription_tariff_potable_water_subscription_fee(),
        simulation_finished.only_tariff_drinking_water_subscription_fee(),
        simulation_payload.primitives.drinking_water.variable_costs,
        simulation_payload.primitives.drinking_water.fixed_costs)
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
        net_contributors_percent=None,
        net_beneficiaries_percent=None,
        subsidized_basic_c_percent=None,
        subsidized_non_basic_c_percent=None,
        margined_c_percent=None,
        bad_sub_percent=None,
        bad_tax_percent=None
    )


@results_router.get("/{simulation_id}/environmental_cost")
async def get_environmental_cost(simulation_id: int, current_user: User = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):
    return EnvironmentalCostTable(
        tbse_conso_rang_1=None,
        effective_tbse=None,
        ibt=None,
        ibt_pp=None
    )


@results_router.get("/{simulation_id}/water_agency")
async def get_water_agency(simulation_id: int, current_user: User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    return WaterAgencyTable(
        exercise_duty=None,
    )


@results_router.get("/{simulation_id}/state")
async def get_state_table(simulation_id: int, current_user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    return StateTable(
        vat=None
    )


results_router.include_router(affordability_router)
