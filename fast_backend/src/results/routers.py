from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_active_user
from src.core.database import get_db
from src.core.models import User
from src.results.schemas import *

results_router = APIRouter(
    prefix="/results",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)


@results_router.get("/{simulation_id}/affordability", response_model=AffordabilityTable)
async def get_affordability_indicators(simulation_id, current_user: User = Depends(get_current_active_user),
                                       db: Session = Depends(get_db)):
    return AffordabilityTable(
        headcount_ratio=AffordabilityColumnValues(ibt=15.9, tbse=32.1),
        apparent_affordability_deficit=AffordabilityColumnValues(ibt=3.37, tbse=16.87),
        effective_affordability_deficit=AffordabilityColumnValues(ibt=17.69, tbse=53.33),
        gini_app=AffordabilityColumnValues(ibt=0.956, tbse=0.793),
        gini_eff=AffordabilityColumnValues(ibt=0.725, tbse=0.355)
    )


@results_router.get("/{simulation_id}/incentive/consumption", response_model=IncentiveConsumptionTable)
async def get_incentive_consumption(simulation_id, current_user: User = Depends(get_current_active_user),
                                    db: Session = Depends(get_db)):
    consumption_table = IncentiveConsumptionTable(
        ibt=ConsumptionValues(average_consumption_m3_trim=None, average_bill_eur_trim=None),
        ibt_pp=ConsumptionValues(average_consumption_m3_trim=None, average_bill_eur_trim=None),
        ibt_tbse=ConsumptionValues(average_consumption_m3_trim=None, average_bill_eur_trim=None),
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
    return {
        "general": -32322,
        "total_cost": -0.9
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
