import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import *
from ...core.auth import get_current_active_user
from ...core.database import get_db
from ...core.models import User
from ...initial.routers import get_simulation_payload_from_db
from ...small_assessment.effeco.gini_decomp import gini_decomp
from ...small_assessment.incentive_service import percentrank_inc, desvprom
from ...small_assessment.new_calculator_service import get_or_create_simulation_from_payload, NewSimulation

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


@affordability_router.post("/{simulation_id}/general/descriptive")
async def get_general_descriptive_affordability(
        simulation_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
) -> GeneralStatistic:
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    simulation_calculator = await get_or_create_simulation_from_payload(
        simulation_id, simulation, simulation_payload
    )

    par_ibt = simulation_calculator.par_ibt
    par_tbse = simulation_calculator.par_tbse
    delta_par = par_ibt - par_tbse

    return GeneralStatistic(
        mean=AugmentedGeneralRow(
            par_ibt=par_ibt.mean(),
            par_tbse=par_tbse.mean(),
            delta_par=delta_par.mean(),
        ),
        median=AugmentedGeneralRow(
            par_ibt=par_ibt.median(),
            par_tbse=par_tbse.median(),
            delta_par=delta_par.median(),
        ),
        min=GeneralRow(
            par_ibt=par_ibt.min(),
            par_tbse=par_tbse.min(),
        ),
        max=GeneralRow(
            par_ibt=par_ibt.max(),
            par_tbse=par_tbse.max(),
        ),
        q1=GeneralRow(
            par_ibt=par_ibt.quantile(0.25),
            par_tbse=par_tbse.quantile(0.25),
        ),
        q3=GeneralRow(
            par_ibt=par_ibt.quantile(0.75),
            par_tbse=par_tbse.quantile(0.75),
        ),
        d1=GeneralRow(
            par_ibt=par_ibt.quantile(0.1),
            par_tbse=par_tbse.quantile(0.1),
        ),
        d9=GeneralRow(
            par_ibt=par_ibt.quantile(0.9),
            par_tbse=par_tbse.quantile(0.9),
        ),
        f=GeneralRow(
            par_ibt=percentrank_inc(par_ibt, par_ibt.mean()) * 100,
            par_tbse=percentrank_inc(par_tbse, par_tbse.mean()) * 100,
        ),
        variance=GeneralRow(
            par_ibt=par_ibt.var(),
            par_tbse=par_tbse.var(),
        ),
        ecart_type=GeneralRow(
            par_ibt=par_ibt.std(),
            par_tbse=par_tbse.std(),
        ),
        MAPE=GeneralRow(
            par_ibt=desvprom(par_ibt),
            par_tbse=desvprom(par_tbse),
        ),
        coeff_variation=GeneralRow(
            par_ibt=par_ibt.std() / par_ibt.mean() if par_ibt.mean() != 0 else 0,
            par_tbse=par_tbse.std() / par_tbse.mean() if par_tbse.mean() != 0 else 0,
        ),
    )


@affordability_router.post("/{simulation_id}/general/incidence")
async def get_general_incidence_affordability(
        simulation_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    simulation_calculator: NewSimulation = await get_or_create_simulation_from_payload(
        simulation_id, simulation, simulation_payload
    )
    return GeneralHeadcountRatio(
        household=AugmentedGeneralRow(par_ibt=simulation_calculator.ibt_par_headcount.mean() * 100,
                                      par_tbse=simulation_calculator.tbse_par_headcount.mean() * 100,
                                      delta_par=simulation_calculator.ibt_par_headcount.mean() - simulation_calculator.tbse_par_headcount.mean() * 100),
        people=AugmentedGeneralRow(
            par_ibt=(simulation_calculator.ibt_par_headcount * simulation_calculator.df['nbpers']).sum() /
                    simulation_calculator.df['nbpers'].sum() * 100,
            par_tbse=(simulation_calculator.tbse_par_headcount * simulation_calculator.df['nbpers']).sum() /
                     simulation_calculator.df['nbpers'].sum() * 100,
            delta_par=(simulation_calculator.ibt_par_headcount * simulation_calculator.df['nbpers']).sum() /
                      simulation_calculator.df['nbpers'].sum() - (
                              simulation_calculator.tbse_par_headcount * simulation_calculator.df['nbpers']).sum() /
                      simulation_calculator.df['nbpers'].sum() * 100
        ),
        children=AugmentedGeneralRow(
                par_ibt=(simulation_calculator.ibt_par_headcount * simulation_calculator.df['nenf']).sum() /
                        simulation_calculator.df['nenf'].sum() * 100,
                par_tbse=(simulation_calculator.tbse_par_headcount * simulation_calculator.df['nenf']).sum() /
                         simulation_calculator.df['nenf'].sum() * 100,
                delta_par=(simulation_calculator.ibt_par_headcount * simulation_calculator.df['nenf']).sum() /
                          simulation_calculator.df['nenf'].sum() - (
                                  simulation_calculator.tbse_par_headcount * simulation_calculator.df['nenf']).sum() /
                          simulation_calculator.df['nenf'].sum() * 100,
        )
    )


@affordability_router.get("/{simulation_id}/general/deficits")
async def get_general_deficits_affordability(
        simulation_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    ibt_excess = simulation_calculator.ibt_par_excess
    tbse_excess = simulation_calculator.tbse_par_excess

    filtered_ibt_excess = ibt_excess[ibt_excess > 0]
    filtered_tbse_excess = tbse_excess[tbse_excess > 0]
    return {
        "apparent": create_deficit_table(ibt_excess, tbse_excess),
        "effective": create_deficit_table(filtered_ibt_excess, filtered_tbse_excess)
    }


@affordability_router.get("/{simulation_id}/general/inequality")
async def get_general_inequality_affordability(
        simulation_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)
    deficit_tables = await get_general_deficits_affordability(simulation_id, current_user, db)
    apparent_table: DeficitTable = deficit_tables['apparent']
    effective_table: DeficitTable = deficit_tables['effective']
    return {
        "all": InequalityTable(
            gini=GeneralRow(par_ibt=(1 - simulation_calculator.ibt_ginis.sum() / 10000) * 100,
                            par_tbse=(1 - simulation_calculator.tbse_ginis.sum() / 10000) * 100),
            schutz=GeneralRow(
                par_ibt=apparent_table.mape.par_ibt / (2 * apparent_table.mean.par_ibt) * 100,
                par_tbse=apparent_table.mape.par_tbse / (2 * apparent_table.mean.par_tbse) * 100,
            )
        ),
        "unafford": InequalityTable(
            gini=GeneralRow(par_ibt=(1 - simulation_calculator.ibt_unafford_ginis.sum() / 10000) * 100,
                            par_tbse=(1 - simulation_calculator.tbse_unafford_ginis.sum() / 10000) * 100),
            schutz=GeneralRow(
                par_ibt=effective_table.mape.par_ibt / (2 * effective_table.mean.par_ibt) * 100,
                par_tbse=effective_table.mape.par_tbse / (2 * effective_table.mean.par_tbse) * 100,
            )
        )
    }


def create_deficit_table(ibt_excess, tbse_excess):
    return DeficitTable(
        mean=AugmentedGeneralRow(
            par_ibt=ibt_excess.mean(),
            par_tbse=tbse_excess.mean(),
            delta_par=ibt_excess.mean() - tbse_excess.mean()
        ),
        median=GeneralRow(
            par_ibt=ibt_excess.median(),
            par_tbse=tbse_excess.median(),
        ),
        d1=GeneralRow(
            par_ibt=ibt_excess.quantile(0.1),
            par_tbse=tbse_excess.quantile(0.1),
        ),
        d9=GeneralRow(
            par_ibt=ibt_excess.quantile(0.9),
            par_tbse=tbse_excess.quantile(0.9),
        ),
        variance=GeneralRow(
            par_ibt=ibt_excess.var(),
            par_tbse=tbse_excess.var(),
        ),
        ecart_type=GeneralRow(
            par_ibt=ibt_excess.std(),
            par_tbse=tbse_excess.std(),
        ),
        cv=GeneralRow(
            par_ibt=ibt_excess.std() / ibt_excess.mean() if ibt_excess.mean() != 0 else 0,
            par_tbse=tbse_excess.std() / tbse_excess.mean() if tbse_excess.mean() != 0 else 0,
        ),
        mape=GeneralRow(
            par_ibt=desvprom(ibt_excess),
            par_tbse=desvprom(tbse_excess),
        )
    )


async def get_group_par_description(
    simulation_id: int, 
    current_user: User,
    db: Session,
    filter_func
) -> GeneralStatistic:
    simulation_payload, simulation = await get_simulation_payload_from_db(current_user, db, simulation_id,
                                                                          get_simulation_db=True)
    simulation_calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    filter_value = filter_func(simulation_calculator)
    not_filter_value = ~filter_value

    # Get PAR data for each group
    par_ibt_g1 = simulation_calculator.par_ibt[not_filter_value]
    par_ibt_g2 = simulation_calculator.par_ibt[filter_value]
    par_tbse_g1 = simulation_calculator.par_tbse[not_filter_value]
    par_tbse_g2 = simulation_calculator.par_tbse[filter_value]

    # Calculate delta values
    delta_par_g1 = par_ibt_g1 - par_tbse_g1
    delta_par_g2 = par_ibt_g2 - par_tbse_g2

    return GeneralStatistic(
        mean=AugmentedGroupRow(
            par_ibt_g1=par_ibt_g1.mean(),
            par_ibt_g2=par_ibt_g2.mean(),
            par_tbse_g1=par_tbse_g1.mean(),
            par_tbse_g2=par_tbse_g2.mean(),
            delta_par_g1=delta_par_g1.mean(),
            delta_par_g2=delta_par_g2.mean(),
        ),
        median=AugmentedGroupRow(
            par_ibt_g1=par_ibt_g1.median(),
            par_ibt_g2=par_ibt_g2.median(),
            par_tbse_g1=par_tbse_g1.median(),
            par_tbse_g2=par_tbse_g2.median(),
            delta_par_g1=delta_par_g1.median(),
            delta_par_g2=delta_par_g2.median(),
        ),
        min=GroupRow(
            par_ibt_g1=par_ibt_g1.min(),
            par_ibt_g2=par_ibt_g2.min(),
            par_tbse_g1=par_tbse_g1.min(),
            par_tbse_g2=par_tbse_g2.min(),
        ),
        max=GroupRow(
            par_ibt_g1=par_ibt_g1.max(),
            par_ibt_g2=par_ibt_g2.max(),
            par_tbse_g1=par_tbse_g1.max(),
            par_tbse_g2=par_tbse_g2.max(),
        ),
        q1=GroupRow(
            par_ibt_g1=par_ibt_g1.quantile(0.25),
            par_ibt_g2=par_ibt_g2.quantile(0.25),
            par_tbse_g1=par_tbse_g1.quantile(0.25),
            par_tbse_g2=par_tbse_g2.quantile(0.25),
        ),
        q3=GroupRow(
            par_ibt_g1=par_ibt_g1.quantile(0.75),
            par_ibt_g2=par_ibt_g2.quantile(0.75),
            par_tbse_g1=par_tbse_g1.quantile(0.75),
            par_tbse_g2=par_tbse_g2.quantile(0.75),
        ),
        d1=GroupRow(
            par_ibt_g1=par_ibt_g1.quantile(0.1),
            par_ibt_g2=par_ibt_g2.quantile(0.1),
            par_tbse_g1=par_tbse_g1.quantile(0.1),
            par_tbse_g2=par_tbse_g2.quantile(0.1),
        ),
        d9=GroupRow(
            par_ibt_g1=par_ibt_g1.quantile(0.9),
            par_ibt_g2=par_ibt_g2.quantile(0.9),
            par_tbse_g1=par_tbse_g1.quantile(0.9),
            par_tbse_g2=par_tbse_g2.quantile(0.9),
        ),
        f=GroupRow(
            par_ibt_g1=percentrank_inc(par_ibt_g1, par_ibt_g1.mean()) * 100,
            par_ibt_g2=percentrank_inc(par_ibt_g2, par_ibt_g2.mean()) * 100,
            par_tbse_g1=percentrank_inc(par_tbse_g1, par_tbse_g1.mean()) * 100,
            par_tbse_g2=percentrank_inc(par_tbse_g2, par_tbse_g2.mean()) * 100,
        ),
        variance=GroupRow(
            par_ibt_g1=par_ibt_g1.var(),
            par_ibt_g2=par_ibt_g2.var(),
            par_tbse_g1=par_tbse_g1.var(),
            par_tbse_g2=par_tbse_g2.var(),
        ),
        ecart_type=GroupRow(
            par_ibt_g1=par_ibt_g1.std(),
            par_ibt_g2=par_ibt_g2.std(),
            par_tbse_g1=par_tbse_g1.std(),
            par_tbse_g2=par_tbse_g2.std(),
        ),
        MAPE=GroupRow(
            par_ibt_g1=desvprom(par_ibt_g1),
            par_ibt_g2=desvprom(par_ibt_g2),
            par_tbse_g1=desvprom(par_tbse_g1),
            par_tbse_g2=desvprom(par_tbse_g2),
        ),
        coeff_variation=GroupRow(
            par_ibt_g1=par_ibt_g1.std() / par_ibt_g1.mean() if par_ibt_g1.mean() != 0 else 0,
            par_ibt_g2=par_ibt_g2.std() / par_ibt_g2.mean() if par_ibt_g2.mean() != 0 else 0,
            par_tbse_g1=par_tbse_g1.std() / par_tbse_g1.mean() if par_tbse_g1.mean() != 0 else 0,
            par_tbse_g2=par_tbse_g2.std() / par_tbse_g2.mean() if par_tbse_g2.mean() != 0 else 0,
        ),
    )

@affordability_router.get("/{simulation_id}/g1_g2_par_description")
async def general_par_description(
    simulation_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> GeneralStatistic:
    return await get_group_par_description(simulation_id, current_user, db, lambda calculator: calculator.is_sanitation())

@affordability_router.get("/{simulation_id}/poor/par_description")
async def poor_par_description(
    simulation_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> GeneralStatistic:
    return await get_group_par_description(simulation_id, current_user, db, lambda calculator: calculator.is_poor)


async def get_group_par_incidence(
    simulation_id: int, 
    current_user: User,
    db: Session,
    filter_func
):
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    filter_value = filter_func(calculator)
    not_filter_value = ~filter_value

    # For sanitation filter, we use specific logic for perc_household in g1 and g2
    if filter_func.__code__.co_consts and 'is_sanitation' in str(filter_func.__code__.co_consts):
        g1_perc_household = ((calculator.simulation.primitives.drinking_water.number_of_subscribers -
                             calculator.simulation.primitives.sanitation.number_of_subscribers) /
                            calculator.simulation.primitives.drinking_water.number_of_subscribers) * 100
        g2_perc_household = ((calculator.simulation.primitives.sanitation.number_of_subscribers) /
                            calculator.simulation.primitives.drinking_water.number_of_subscribers) * 100
    else:
        # For other filters, calculate percentage based on the filter
        g1_perc_household = not_filter_value.mean() * 100
        g2_perc_household = filter_value.mean() * 100

    return GroupIncidenceTable(
        g1=GroupIncidenceRow(
            perc_household=g1_perc_household,
            ibt_household=calculator.ibt_par_headcount[not_filter_value].sum() / (
                    not_filter_value).sum() * 100,
            perc_people=calculator.df["nbpers"][not_filter_value].sum() / (
                calculator.df["nbpers"].sum()
            ) * 100,
            ibt_people=(100 * (calculator.ibt_par_headcount * calculator.df["nbpers"])[
                not_filter_value].sum() /
                        calculator.df["nbpers"][not_filter_value].sum()
                        ),
            perc_children=(100 * calculator.df.loc[not_filter_value, "nenf"].sum()
                           / calculator.df["nenf"].sum()
                           ),
            ibt_children=(100 *
                          (calculator.ibt_par_headcount * calculator.df["nenf"])[
                              not_filter_value
                              ].sum() / calculator.df.loc[not_filter_value, "nenf"].sum()),
            tbse_household=calculator.tbse_par_headcount[not_filter_value].sum() / (
                    not_filter_value
            ).sum() * 100,
            tbse_people=(100 * (calculator.tbse_par_headcount * calculator.df["nbpers"])[
                not_filter_value].sum() / calculator.df["nbpers"][
                             not_filter_value].sum()),
            tbse_children=(100 * calculator.df.loc[not_filter_value, "nenf"].sum()
                           / calculator.df["nenf"].sum()
                           ),
        ),
        g2=GroupIncidenceRow(
            perc_household=g2_perc_household,
            ibt_household=calculator.ibt_par_headcount[filter_value].sum() / (
                    filter_value).sum() * 100,
            perc_people=calculator.df["nbpers"][filter_value].sum() / (
                calculator.df["nbpers"].sum()
            ) * 100,
            ibt_people=(100 * (calculator.ibt_par_headcount * calculator.df["nbpers"])[
                filter_value].sum() /
                        calculator.df["nbpers"][filter_value].sum()
                        ),
            perc_children=(100 * calculator.df.loc[filter_value, "nenf"].sum()
                           / calculator.df["nenf"].sum()
                           ),
            ibt_children=(100 *
                          (calculator.ibt_par_headcount * calculator.df["nenf"])[
                              filter_value
                              ].sum() / calculator.df.loc[filter_value, "nenf"].sum()),
            tbse_household=calculator.tbse_par_headcount[filter_value].sum() / (
                    filter_value
            ).sum() * 100,
            tbse_people=(100 * (calculator.tbse_par_headcount * calculator.df["nbpers"])[
                filter_value].sum() / calculator.df["nbpers"][
                             filter_value].sum()),
            tbse_children=(100 * calculator.df.loc[filter_value, "nenf"].sum()
                           / calculator.df["nenf"].sum()
                           ),
        ),
        total=GroupIncidenceRow(
            perc_household=100,
            ibt_household=calculator.ibt_par_headcount.mean() * 100,
            perc_people=100,
            ibt_people=(calculator.ibt_par_headcount * calculator.df['nbpers']).sum() /
                       calculator.df['nbpers'].sum() * 100,
            perc_children=100,
            ibt_children=(calculator.ibt_par_headcount * calculator.df['nenf']).sum() /
                         calculator.df['nenf'].sum() * 100,
            tbse_household=calculator.tbse_par_headcount.mean() * 100,
            tbse_people=(calculator.tbse_par_headcount * calculator.df['nbpers']).sum() /
                        calculator.df['nbpers'].sum() * 100,
            tbse_children=(calculator.tbse_par_headcount * calculator.df['nenf']).sum() /
                          calculator.df['nenf'].sum() * 100,
        )
    )

@affordability_router.get("/{simulation_id}/g1_g2/incidence")
async def general_par_incidence(
    simulation_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return await get_group_par_incidence(simulation_id, current_user, db, lambda calculator: calculator.is_sanitation())

@affordability_router.get("/{simulation_id}/poor/incidence")
async def poor_par_incidence(
    simulation_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return await get_group_par_incidence(simulation_id, current_user, db, lambda calculator: calculator.is_poor)


async def get_group_intensity(
        simulation_id: int,
        current_user: User,
        db: Session,
        filter_func
):
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    filter_value = filter_func(calculator)
    not_filter_value = ~filter_value

    ibt_apparent_group = GroupDeficit(
        g1=RowDeficit(
            perc=not_filter_value.mean() * 100,
            mean=calculator.ibt_par_excess[
                filter_value == False
                ].mean(),
            var=calculator.ibt_par_excess[
                filter_value == False
                ].var()
        ),
        g2=RowDeficit(
            perc=filter_value.mean() * 100,
            mean=calculator.ibt_par_excess[
                filter_value == True
                ].mean(),
            var=calculator.ibt_par_excess[
                filter_value == True
                ].var(), ),
        ensemble=RowDeficit(
            perc=100,
            mean=calculator.ibt_par_excess.mean(),
            var=calculator.ibt_par_excess.var()
        )
    )
    ibt_apparent_group = from_group_deficit_to_augmented(ibt_apparent_group)
    tbse_apparent_group = GroupDeficit(
        g1=RowDeficit(
            perc=not_filter_value.mean() * 100,
            mean=calculator.tbse_par_excess[
                filter_value == False
                ].mean(),
            var=calculator.tbse_par_excess[
                filter_value == False
                ].var()
        ),
        g2=RowDeficit(
            perc=filter_value.mean() * 100,
            mean=calculator.tbse_par_excess[
                filter_value == True
                ].mean(),
            var=calculator.tbse_par_excess[
                filter_value == True
                ].var(), ),
        ensemble=RowDeficit(
            perc=100,
            mean=calculator.tbse_par_excess.mean(),
            var=calculator.tbse_par_excess.var()
        )
    )
    tbse_apparent_group = from_group_deficit_to_augmented(tbse_apparent_group)

    ibt_effective_group = GroupDeficit(
        g1=RowDeficit(
            perc=(np.array((filter_value == False))[(calculator.ibt_par_excess > 0)]).mean() * 100,
            mean=calculator.ibt_par_excess[
                (filter_value == False) & (calculator.ibt_par_excess > 0)
                ].mean(),
            var=calculator.ibt_par_excess[
                (filter_value == False) & (calculator.ibt_par_excess > 0)
                ].var()
        ),
        g2=RowDeficit(
            perc=(np.array((filter_value))[(calculator.ibt_par_excess > 0)]).mean() * 100,
            mean=calculator.ibt_par_excess[
                (filter_value == True) & (calculator.ibt_par_excess > 0)
                ].mean(),
            var=calculator.ibt_par_excess[
                (filter_value == True) & (calculator.ibt_par_excess > 0)
                ].var(),
        ), ensemble=RowDeficit(
            perc=100,
            mean=calculator.ibt_par_excess[calculator.ibt_par_excess > 0].mean(),
            var=calculator.ibt_par_excess[calculator.ibt_par_excess > 0].var()
        )
    )
    ibt_effective_group = from_group_deficit_to_augmented(ibt_effective_group)
    tbse_effective_group = GroupDeficit(
        g1=RowDeficit(
            perc=(np.array((filter_value == False))[(calculator.tbse_par_excess > 0)]).mean() * 100,
            mean=calculator.tbse_par_excess[
                (filter_value == False) & (calculator.tbse_par_excess > 0)
                ].mean(),
            var=calculator.tbse_par_excess[
                (filter_value == False) & (calculator.tbse_par_excess > 0)
                ].var()
        ),
        g2=RowDeficit(
            perc=(np.array((filter_value == True))[(calculator.tbse_par_excess > 0)]).mean() * 100,
            mean=calculator.tbse_par_excess[
                (filter_value == True) & (calculator.tbse_par_excess > 0)
                ].mean(),
            var=calculator.tbse_par_excess[
                (filter_value == True) & (calculator.tbse_par_excess > 0)
                ].var()
        ),
        ensemble=RowDeficit(
            perc=100,
            mean=calculator.tbse_par_excess[calculator.tbse_par_excess > 0].mean(),
            var=calculator.tbse_par_excess[calculator.tbse_par_excess > 0].var()
        )
    )
    tbse_effective_group = from_group_deficit_to_augmented(tbse_effective_group)
    return {
        "apparent": DeficitAffordabilityTable(
            par_ibt=ibt_apparent_group,
            par_tbse=tbse_apparent_group,
        ),
        "effective": DeficitAffordabilityTable(
            par_ibt=ibt_effective_group,
            par_tbse=tbse_effective_group,
        )
    }

@affordability_router.get("/{simulation_id}/g1_g2/intensity")
async def get_group_g1_g2_intensity(
        simulation_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return await get_group_intensity(simulation_id, current_user, db, lambda calculator: calculator.is_sanitation())

@affordability_router.get("/{simulation_id}/poor/intensity")
async def get_group_poor_intensity(
        simulation_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return await get_group_intensity(simulation_id, current_user, db, lambda calculator: calculator.is_poor)


async def get_group_par_inequality(
        simulation_id: int,
        current_user: User,
        db: Session,
        filter_func
) -> OutputGiniDecomp:
    simulation_payload, simulation = await get_simulation_payload_from_db(
        current_user, db, simulation_id, get_simulation_db=True
    )
    calculator = await get_or_create_simulation_from_payload(simulation_id, simulation, simulation_payload)

    filter_value = filter_func(calculator)

    # Process PAR IBT values
    par_ibt_gini_data = gini_decomp(calculator.par_ibt, filter_value)['gini_decomp']
    par_ibt_table = _create_gini_decomp_table(par_ibt_gini_data)

    # Process PAR TBSE values
    par_tbse_gini_data = gini_decomp(calculator.par_tbse, filter_value)['gini_decomp']
    par_tbse_table = _create_gini_decomp_table(par_tbse_gini_data)

    # Process excess PAR IBT values
    excess_par_ibt_gini_data = gini_decomp(
        calculator.par_ibt[calculator.ibt_par_excess > 0],
        filter_value[calculator.ibt_par_excess > 0]
    )['gini_decomp']
    excess_par_ibt_table = _create_gini_decomp_table(excess_par_ibt_gini_data)

    # Process excess PAR TBSE values
    excess_par_tbse_gini_data = gini_decomp(
        calculator.par_tbse[calculator.tbse_par_excess > 0],
        filter_value[calculator.tbse_par_excess > 0]
    )['gini_decomp']
    excess_par_tbse_table = _create_gini_decomp_table(excess_par_tbse_gini_data)

    return OutputGiniDecomp(
        par_ibt=par_ibt_table,
        par_tbse=par_tbse_table,
        excess_par_ibt=excess_par_ibt_table,
        excess_par_tbse=excess_par_tbse_table
    )

@affordability_router.get("/{simulation_id}/g1_g2_par_inequality")
async def gini_index_comparison(
        simulation_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
) -> OutputGiniDecomp:
    return await get_group_par_inequality(simulation_id, current_user, db, lambda calculator: calculator.is_sanitation())

@affordability_router.get("/{simulation_id}/poor/par_inequality")
async def poor_gini_index_comparison(
        simulation_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
) -> OutputGiniDecomp:
    return await get_group_par_inequality(simulation_id, current_user, db, lambda calculator: calculator.is_poor)
