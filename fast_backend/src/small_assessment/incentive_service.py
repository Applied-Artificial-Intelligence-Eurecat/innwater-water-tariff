import numpy as np
import pandas as pd
from pydantic import BaseModel, field_validator

from src.small_assessment.new_calculator_service import NewSimulation


def check_zero_devision(func, args=[]):
    try:
        result = func(*args)
    except ZeroDivisionError:
        return None
    if np.isnan(result).any():
        return None
    return result


class IncentiveConsumptionRow(BaseModel):
    ibt: float
    ibt_pp: float
    tbse: float
    actual_overconsumption: float
    overconsumption_per_capita: float


class DeltaIncentiveConsumptionRow(BaseModel):
    delta_ibt_plus: float | None
    delta_ibt_minus: float | None
    delta_ibt_pp_plus: float | None
    delta_ibt_pp_minus: float | None

    @field_validator('delta_ibt_plus', 'delta_ibt_minus', 'delta_ibt_pp_plus', 'delta_ibt_pp_minus')
    @classmethod
    def convert_nan_to_none(cls, v):
        if v is not None and np.isnan(v).any():
            return None
        return v


class IncentiveConsumption(BaseModel):
    perc_households: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow | None = None
    mean: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    median: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    min: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    max: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    q1: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    q3: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    d1: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    d9: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    percentile_rank: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    variance: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    ecart_type: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    mape: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    variation_coeff: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    iqr: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    idr: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    yule_coeff: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow
    gini_schutz: IncentiveConsumptionRow | DeltaIncentiveConsumptionRow


class OverconsumptionDecompositionRow(BaseModel):
    frequency: float | None
    delta_c_moyen: float  | None
    variance: float  | None

    @field_validator('frequency', 'delta_c_moyen', 'variance')
    @classmethod
    def convert_nan_to_none(cls, v):
        if v is not None and np.isnan(v).any():
            return None
        return v

class GroupDecomposition(BaseModel):
    ensemble: OverconsumptionDecompositionRow
    delta_plus: OverconsumptionDecompositionRow
    delta_minus: OverconsumptionDecompositionRow
    g1_delta_plus: OverconsumptionDecompositionRow
    g2_delta_plus: OverconsumptionDecompositionRow
    g1_delta_minus: OverconsumptionDecompositionRow
    g2_delta_minus: OverconsumptionDecompositionRow
    poor_delta_plus: OverconsumptionDecompositionRow
    poor_delta_minus: OverconsumptionDecompositionRow
    nonpoor_delta_plus: OverconsumptionDecompositionRow
    nonpoor_delta_minus: OverconsumptionDecompositionRow


class OverconsumptionDecomposition(BaseModel):
    households_percentage: OverconsumptionDecompositionRow
    g1: OverconsumptionDecompositionRow
    g2: OverconsumptionDecompositionRow
    poor: OverconsumptionDecompositionRow
    nonpoor: OverconsumptionDecompositionRow


class OverconsumptionDecompositionVariance(BaseModel):
    v_inter: float
    v_intra: float
    correlation_ratio: float


class SquareRow(BaseModel):
    poor: float
    nonpoor: float
    ensemble: float


class SquareTable(BaseModel):
    g1: SquareRow
    g2: SquareRow
    total_population: SquareRow


def percentrank_inc(data, x):
    data = np.sort(data)
    N = len(data)

    if x <= data[0]:
        return 0.0
    if x >= data[-1]:
        return 1.0

    # Find lower and upper bounds
    for i in range(1, N):
        if data[i] >= x:
            L, U = data[i - 1], data[i]
            pos = (i - 1) + (x - L) / (U - L)
            return pos / (N - 1)


def desvprom(series: pd.Series) -> float:
    m = series.mean()
    return np.abs(series - m).mean()


def delta_incentive_effect_consumption(calculator: NewSimulation) -> IncentiveConsumption:
    # Consumption BCP (t) - TBSE consumption

    delta = calculator.bcp_consumptions[calculator.simulation.launch.periods] - calculator.tbse_consumption_per_trim
    delta_pp = calculator.ibt_pp_consumption - calculator.tbse_consumption_per_trim

    delta_ibt_plus = delta[delta > 0]
    delta_ibt_minus = delta[delta < 0]

    delta_ibt_pp_plus = delta_pp[delta_pp > 0]
    delta_ibt_pp_minus = delta_pp[delta_pp < 0]

    q1_row = DeltaIncentiveConsumptionRow(
        delta_ibt_plus=check_zero_devision(lambda: delta_ibt_plus.quantile(0.25)),
        delta_ibt_minus=check_zero_devision(lambda: delta_ibt_minus.quantile(0.25)),
        delta_ibt_pp_plus=check_zero_devision(lambda: delta_ibt_pp_plus.quantile(0.25)),
        delta_ibt_pp_minus=check_zero_devision(lambda: delta_ibt_pp_minus.quantile(0.25))
    )
    q3_row = DeltaIncentiveConsumptionRow(
        delta_ibt_plus=check_zero_devision(lambda: delta_ibt_plus.quantile(0.75)),
        delta_ibt_minus=check_zero_devision(lambda: delta_ibt_minus.quantile(0.75)),
        delta_ibt_pp_plus=check_zero_devision(lambda: delta_ibt_pp_plus.quantile(0.75)),
        delta_ibt_pp_minus=check_zero_devision(lambda: delta_ibt_pp_minus.quantile(0.75))
    )
    mape_row = DeltaIncentiveConsumptionRow(
        delta_ibt_plus=desvprom(delta_ibt_plus),
        delta_ibt_minus=desvprom(delta_ibt_minus),
        delta_ibt_pp_plus=desvprom(delta_ibt_pp_plus),
        delta_ibt_pp_minus=desvprom(delta_ibt_pp_minus)
    )
    median_row = DeltaIncentiveConsumptionRow(delta_ibt_plus=delta_ibt_plus.median(),
                                              delta_ibt_minus=delta_ibt_minus.median(),
                                              delta_ibt_pp_plus=delta_ibt_pp_plus.median(),
                                              delta_ibt_pp_minus=delta_ibt_pp_minus.median())
    return IncentiveConsumption(
        perc_households=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=len(delta_ibt_plus) / len(delta) * 100,
            delta_ibt_minus=len(delta_ibt_minus) / len(delta) * 100,
            delta_ibt_pp_plus=len(delta_ibt_pp_plus) / len(delta_pp) * 100,
            delta_ibt_pp_minus=len(delta_ibt_pp_minus) / len(delta_pp) * 100
        ),
        mean=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.mean(),
            delta_ibt_minus=delta_ibt_minus.mean(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.mean(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.mean()
        ),
        median=median_row,
        min=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.min(),
            delta_ibt_minus=delta_ibt_minus.min(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.min(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.min()
        ),
        max=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.max(),
            delta_ibt_minus=delta_ibt_minus.max(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.max(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.max()
        ),
        q1=q1_row,
        q3=q3_row,
        d1=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.quantile(0.1),
            delta_ibt_minus=delta_ibt_minus.quantile(0.1),
            delta_ibt_pp_plus=delta_ibt_pp_plus.quantile(0.1),
            delta_ibt_pp_minus=delta_ibt_pp_minus.quantile(0.1)
        ),
        d9=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.quantile(0.9),
            delta_ibt_minus=delta_ibt_minus.quantile(0.9),
            delta_ibt_pp_plus=delta_ibt_pp_plus.quantile(0.9),
            delta_ibt_pp_minus=delta_ibt_pp_minus.quantile(0.9)
        ),
        percentile_rank=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=percentrank_inc(delta_ibt_plus, delta_ibt_plus.mean()),
            delta_ibt_minus=percentrank_inc(delta_ibt_minus, delta_ibt_minus.mean()),
            delta_ibt_pp_plus=percentrank_inc(delta_ibt_pp_plus, delta_ibt_pp_plus.mean()),
            delta_ibt_pp_minus=percentrank_inc(delta_ibt_pp_minus, delta_ibt_pp_minus.mean())
        ),
        variance=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.var(),
            delta_ibt_minus=delta_ibt_minus.var(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.var(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.var()
        ),
        ecart_type=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.std(),
            delta_ibt_minus=delta_ibt_minus.std(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.std(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.std()
        ),
        mape=mape_row,
        variation_coeff=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.std() / delta_ibt_plus.mean(),
            delta_ibt_minus=delta_ibt_minus.std() / delta_ibt_minus.mean(),
            delta_ibt_pp_plus=delta_ibt_pp_plus.std() / delta_ibt_pp_plus.mean(),
            delta_ibt_pp_minus=delta_ibt_pp_minus.std() / delta_ibt_pp_minus.mean(),
        ),
        iqr=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.quantile(0.75) - delta_ibt_plus.quantile(0.25),
            delta_ibt_minus=delta_ibt_minus.quantile(0.75) - delta_ibt_minus.quantile(0.25),
            delta_ibt_pp_plus=delta_ibt_pp_plus.quantile(0.75) - delta_ibt_pp_plus.quantile(0.25),
            delta_ibt_pp_minus=delta_ibt_pp_minus.quantile(0.75) - delta_ibt_pp_minus.quantile(0.25),
        ),
        idr=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=delta_ibt_plus.quantile(0.9) - delta_ibt_plus.quantile(0.1),
            delta_ibt_minus=delta_ibt_minus.quantile(0.9) - delta_ibt_minus.quantile(0.1),
            delta_ibt_pp_plus=delta_ibt_pp_plus.quantile(0.9) - delta_ibt_pp_plus.quantile(0.1),
            delta_ibt_pp_minus=delta_ibt_pp_minus.quantile(0.9) - delta_ibt_pp_minus.quantile(0.1),
        ),
        yule_coeff=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=check_zero_devision(lambda: ((q3_row.delta_ibt_plus - median_row.delta_ibt_plus) - (
                    median_row.delta_ibt_plus - q1_row.delta_ibt_plus)) / (
                                                               q3_row.delta_ibt_plus - q1_row.delta_ibt_plus)),
            delta_ibt_minus=check_zero_devision(lambda: ((q3_row.delta_ibt_minus - median_row.delta_ibt_minus) - (
                    median_row.delta_ibt_minus - q1_row.delta_ibt_minus)) / (
                                                                q3_row.delta_ibt_minus - q1_row.delta_ibt_minus)),
            delta_ibt_pp_plus=check_zero_devision(lambda: ((q3_row.delta_ibt_pp_plus - median_row.delta_ibt_pp_plus) - (
                    median_row.delta_ibt_pp_plus - q1_row.delta_ibt_pp_plus)) / (
                                                                  q3_row.delta_ibt_pp_plus - q1_row.delta_ibt_pp_plus)),
            delta_ibt_pp_minus=check_zero_devision(
                lambda: (q3_row.delta_ibt_pp_minus - median_row.delta_ibt_pp_minus) - (
                        median_row.delta_ibt_pp_minus - q1_row.delta_ibt_pp_minus)) / (
                                       q3_row.delta_ibt_pp_minus - q1_row.delta_ibt_pp_minus),
        ),
        gini_schutz=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=(mape_row.delta_ibt_plus / (2 * delta_ibt_plus.mean())) * 100,
            delta_ibt_minus=(mape_row.delta_ibt_minus / (2 * delta_ibt_minus.mean())) * 100,
            delta_ibt_pp_plus=(mape_row.delta_ibt_pp_plus / (2 * delta_ibt_pp_plus.mean())) * 100,
            delta_ibt_pp_minus=(mape_row.delta_ibt_pp_minus / (2 * delta_ibt_pp_minus.mean())) * 100,
        )
    )


def incentive_effect_consumption(calculator: NewSimulation) -> IncentiveConsumption:
    # (Consumption BCP (EPA) - Consumptiopn IBT PP)

    ibt = calculator.bcp_consumptions[calculator.simulation.launch.periods]
    ibt_pp = calculator.ibt_pp_consumption
    tbse = calculator.tbse_consumption_per_trim
    actual_overconsumption = calculator.bcp_consumptions[
                                 calculator.simulation.launch.periods] - calculator.ibt_pp_consumption
    consumption_per_capita = actual_overconsumption / calculator.df['nbpers']

    mean_row = IncentiveConsumptionRow(ibt=ibt.mean(),
                                       ibt_pp=ibt_pp.mean(),
                                       tbse=tbse.mean(),
                                       actual_overconsumption=actual_overconsumption.mean(),
                                       overconsumption_per_capita=(consumption_per_capita).mean())
    median_row = IncentiveConsumptionRow(ibt=ibt.median(), ibt_pp=ibt_pp.median(),
                                         tbse=tbse.median(),
                                         actual_overconsumption=actual_overconsumption.median(),
                                         overconsumption_per_capita=(consumption_per_capita).median())
    q1_row = IncentiveConsumptionRow(ibt=ibt.quantile(0.25), ibt_pp=ibt_pp.quantile(0.25),
                                     tbse=tbse.quantile(0.25),
                                     actual_overconsumption=actual_overconsumption.quantile(0.25),
                                     overconsumption_per_capita=(consumption_per_capita).quantile(0.25))
    q3_row = IncentiveConsumptionRow(ibt=ibt.quantile(0.75), ibt_pp=ibt_pp.quantile(0.75),
                                     tbse=tbse.quantile(0.75),
                                     actual_overconsumption=actual_overconsumption.quantile(0.75),
                                     overconsumption_per_capita=(consumption_per_capita).quantile(0.75))
    mape_row = IncentiveConsumptionRow(ibt=desvprom(ibt), ibt_pp=desvprom(ibt_pp),
                                       tbse=desvprom(tbse),
                                       actual_overconsumption=desvprom(actual_overconsumption),
                                       overconsumption_per_capita=desvprom(consumption_per_capita))
    return IncentiveConsumption(
        mean=mean_row,
        median=median_row,
        min=IncentiveConsumptionRow(
            ibt=ibt.min(),
            ibt_pp=ibt_pp.min(),
            tbse=tbse.min(),
            actual_overconsumption=actual_overconsumption.min(),
            overconsumption_per_capita=(consumption_per_capita).min()
        ),
        max=IncentiveConsumptionRow(
            ibt=ibt.max(),
            ibt_pp=ibt_pp.max(),
            tbse=tbse.max(),
            actual_overconsumption=actual_overconsumption.max(),
            overconsumption_per_capita=(consumption_per_capita).max()
        ),
        q1=q1_row,
        q3=q3_row,
        d1=IncentiveConsumptionRow(
            ibt=ibt.quantile(0.1),
            ibt_pp=ibt_pp.quantile(0.1),
            tbse=tbse.quantile(0.1),
            actual_overconsumption=actual_overconsumption.quantile(0.1),
            overconsumption_per_capita=(consumption_per_capita).quantile(0.1)
        ),
        d9=IncentiveConsumptionRow(
            ibt=ibt.quantile(0.9),
            ibt_pp=ibt_pp.quantile(0.9),
            tbse=tbse.quantile(0.9),
            actual_overconsumption=actual_overconsumption.quantile(0.9),
            overconsumption_per_capita=(consumption_per_capita).quantile(0.9)
        ),
        percentile_rank=IncentiveConsumptionRow(
            ibt=percentrank_inc(ibt, ibt.mean()),
            ibt_pp=percentrank_inc(ibt_pp, ibt_pp.mean()),
            tbse=percentrank_inc(tbse, tbse.mean()),
            actual_overconsumption=percentrank_inc(actual_overconsumption, actual_overconsumption.mean()),
            overconsumption_per_capita=percentrank_inc(consumption_per_capita,
                                                       consumption_per_capita.mean())
        ),
        variance=IncentiveConsumptionRow(
            ibt=ibt.var(),
            ibt_pp=ibt_pp.var(),
            tbse=tbse.var(),
            actual_overconsumption=actual_overconsumption.var(),
            overconsumption_per_capita=(consumption_per_capita).var()
        ),
        ecart_type=IncentiveConsumptionRow(
            ibt=ibt.std(),
            ibt_pp=ibt_pp.std(),
            tbse=tbse.std(),
            actual_overconsumption=actual_overconsumption.std(),
            overconsumption_per_capita=(consumption_per_capita).std()
        ),
        mape=mape_row,
        variation_coeff=IncentiveConsumptionRow(
            ibt=ibt.std() / ibt.mean(),
            ibt_pp=ibt_pp.std() / ibt_pp.mean(),
            tbse=tbse.std() / tbse.mean(),
            actual_overconsumption=ibt.std() / ibt.mean(),
            overconsumption_per_capita=ibt.std() / ibt.mean(),
        ),
        iqr=IncentiveConsumptionRow(
            ibt=ibt.quantile(0.75) - ibt.quantile(0.25),
            ibt_pp=ibt_pp.quantile(0.75) - ibt_pp.quantile(0.25),
            tbse=tbse.quantile(0.75) - tbse.quantile(0.25),
            actual_overconsumption=ibt.quantile(0.75) - ibt.quantile(0.25),
            overconsumption_per_capita=ibt.quantile(0.75) - ibt.quantile(0.25),
        ),
        idr=IncentiveConsumptionRow(
            ibt=ibt.quantile(0.9) / ibt.quantile(0.1),
            ibt_pp=ibt_pp.quantile(0.9) / ibt_pp.quantile(0.1),
            tbse=tbse.quantile(0.9) / tbse.quantile(0.1),
            actual_overconsumption=ibt.quantile(0.9) / ibt.quantile(0.1),
            overconsumption_per_capita=ibt.quantile(0.9) / ibt.quantile(0.1),
        ),
        yule_coeff=IncentiveConsumptionRow(
            ibt=((q3_row.ibt - median_row.ibt) - (median_row.ibt - q1_row.ibt)) / (q3_row.ibt - q1_row.ibt),
            ibt_pp=((q3_row.ibt_pp - median_row.ibt_pp) - (median_row.ibt_pp - q1_row.ibt_pp)) / (
                    q3_row.ibt_pp - q1_row.ibt_pp),
            tbse=((q3_row.tbse - median_row.tbse) - (median_row.tbse - q1_row.tbse)) / (q3_row.tbse - q1_row.tbse),
            actual_overconsumption=((q3_row.actual_overconsumption - median_row.actual_overconsumption) - (
                    median_row.actual_overconsumption - q1_row.actual_overconsumption)) / (
                                           q3_row.actual_overconsumption - q1_row.actual_overconsumption),
            overconsumption_per_capita=((q3_row.overconsumption_per_capita - median_row.overconsumption_per_capita) - (
                    median_row.overconsumption_per_capita - q1_row.overconsumption_per_capita)) / (
                                               q3_row.overconsumption_per_capita - q1_row.overconsumption_per_capita),
        ),
        gini_schutz=IncentiveConsumptionRow(
            ibt=1 - (mape_row.ibt / 100),
            ibt_pp=1 - (mape_row.ibt_pp / 100),
            tbse=1 - (mape_row.tbse / 100),
            actual_overconsumption=1 - (mape_row.actual_overconsumption / 100),
            overconsumption_per_capita=1 - (mape_row.overconsumption_per_capita / 100),
        )

    )


def overconsumption_decomposition_variance(all_groups: OverconsumptionDecompositionRow,
                                           g1: OverconsumptionDecompositionRow,
                                           g2: OverconsumptionDecompositionRow) -> OverconsumptionDecompositionVariance:
    households_percentage = g1.frequency / 100 * (
            g1.delta_c_moyen - all_groups.delta_c_moyen) ** 2 + g2.frequency / 100 * (
                                    g2.delta_c_moyen - all_groups.delta_c_moyen) ** 2

    v_intra = (g1.frequency * g1.variance + g2.frequency * g2.variance) / 100
    return OverconsumptionDecompositionVariance(
        v_inter=households_percentage,
        v_intra=v_intra,
        correlation_ratio=households_percentage / v_intra * 100
    )


def overconsumption_decomposition(simulation_calculator: NewSimulation) -> OverconsumptionDecomposition:
    df = simulation_calculator.df
    bcp_consumption = simulation_calculator.bcp_consumptions[simulation_calculator.simulation.launch.periods]
    ibt_pp_consumption = simulation_calculator.ibt_pp_consumption
    overconsumption = bcp_consumption - ibt_pp_consumption
    is_overconsumption = (overconsumption > 0)

    captive_ln = np.log(simulation_calculator.captive_consumption_per_day)
    g1_delta_c_moyen = captive_ln[is_overconsumption & (
            simulation_calculator.is_sanitation() == False)].mean()
    g1_frequency = overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == False)].sum() / \
                   overconsumption[is_overconsumption].sum()

    g2_frequency = overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == True)].sum() / \
                   overconsumption[is_overconsumption].sum()
    g2_delta_c_moyen = captive_ln[is_overconsumption & (
            simulation_calculator.is_sanitation() == True)].mean()

    g1_var = overconsumption[(overconsumption != 0) & (
            simulation_calculator.is_sanitation() == False)].var(ddof=1)
    g2_var = overconsumption[(overconsumption != 0) & (
            simulation_calculator.is_sanitation() == True)].var(ddof=1)
    households_var = (overconsumption).replace(0, pd.NA).var()

    return OverconsumptionDecomposition(
        households_percentage=OverconsumptionDecompositionRow(
            frequency=(is_overconsumption).astype(float).sum() / len(df) * 100,
            delta_c_moyen=overconsumption.mean(),
            variance=households_var,
        ),
        g1=OverconsumptionDecompositionRow(
            frequency=g1_frequency,
            delta_c_moyen=g1_delta_c_moyen,
            variance=g1_var,
        ),
        g2=OverconsumptionDecompositionRow(
            frequency=g2_frequency,
            delta_c_moyen=g2_delta_c_moyen,
            variance=g2_var,
        ),
        poor=OverconsumptionDecompositionRow(
            frequency=is_overconsumption[
                          is_overconsumption & simulation_calculator.is_poor].sum() / is_overconsumption.sum() * 100,
            delta_c_moyen=captive_ln[is_overconsumption & simulation_calculator.is_poor].mean(),
            variance=overconsumption[is_overconsumption & simulation_calculator.is_poor].var(ddof=1),
        ),
        nonpoor=OverconsumptionDecompositionRow(
            frequency=is_overconsumption[is_overconsumption & (
                ~simulation_calculator.is_poor)].sum() / is_overconsumption.sum() * 100,
            delta_c_moyen=captive_ln[is_overconsumption & (~simulation_calculator.is_poor)].mean(),
            variance=overconsumption[is_overconsumption & (~simulation_calculator.is_poor)].var(ddof=1),
        )
    )


def composition_of_households_that_overconsume(simulation_calculator: NewSimulation):
    bcp_consumption = simulation_calculator.bcp_consumptions[simulation_calculator.simulation.launch.periods]
    ibt_pp_consumption = simulation_calculator.ibt_pp_consumption
    overconsumption = bcp_consumption - ibt_pp_consumption
    is_overconsumption = (overconsumption > 0)

    den = is_overconsumption.sum()

    g1_row = SquareRow(
        poor=is_overconsumption[
                 (simulation_calculator.is_sanitation() == 0) & (simulation_calculator.is_poor)].sum() / den * 100,
        nonpoor=is_overconsumption[(simulation_calculator.is_sanitation() == 0) & (
            ~ simulation_calculator.is_poor)].sum() / den * 100,
        ensemble=is_overconsumption[simulation_calculator.is_sanitation() == 0].sum() / den * 100,
    )
    g2_row = SquareRow(
        poor=is_overconsumption[
                 (simulation_calculator.is_sanitation() == 1) & (simulation_calculator.is_poor)].sum() / den * 100,
        nonpoor=is_overconsumption[(simulation_calculator.is_sanitation() == 1) & (
            ~ simulation_calculator.is_poor)].sum() / den * 100,
        ensemble=is_overconsumption[simulation_calculator.is_sanitation() == 1].sum() / den * 100,
    )
    return SquareTable(
        g1=g1_row,
        g2=g2_row,
        total_population=SquareRow(
            poor=g1_row.poor + g2_row.poor,
            nonpoor=g1_row.nonpoor + g2_row.nonpoor,
            ensemble=g1_row.ensemble + g2_row.ensemble,
        )
    )


def breakdown_of_overconsumption(simulation_calculator: NewSimulation):
    bcp_consumption = simulation_calculator.bcp_consumptions[simulation_calculator.simulation.launch.periods]
    ibt_pp_consumption = simulation_calculator.ibt_pp_consumption
    overconsumption = bcp_consumption - ibt_pp_consumption
    is_overconsumption = (overconsumption > 0)

    den = overconsumption[is_overconsumption].sum()
    col = 'Donnees J'
    g1 = SquareRow(
        poor=overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == 0) & (
            simulation_calculator.is_poor)].sum() / den * 100,
        nonpoor=overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == 0) & (
                simulation_calculator.is_poor == False
        )].sum() / den * 100,
        ensemble=overconsumption[is_overconsumption & simulation_calculator.is_sanitation() == 0].sum() / den * 100,
    )
    g2 = SquareRow(
        poor=overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == 1) & (
            simulation_calculator.is_poor)].sum() / den * 100,
        nonpoor=overconsumption[is_overconsumption & (simulation_calculator.is_sanitation() == 1) & (
                simulation_calculator.is_poor == False
        )].sum() / den * 100,
        ensemble=overconsumption[is_overconsumption & simulation_calculator.is_sanitation() == 1].sum() / den * 100,
    )
    return SquareTable(
        g1=g1,
        g2=g2,
        total_population=SquareRow(
            poor=g1.poor + g2.poor,
            nonpoor=g1.nonpoor + g2.nonpoor,
            ensemble=g1.ensemble + g2.ensemble,
        )
    )


def decomposition_table(simulation_calculator: NewSimulation) -> GroupDecomposition:
    df = simulation_calculator.df

    diff_consumption = simulation_calculator.bcp_consumptions[
                           simulation_calculator.simulation.launch.periods] - simulation_calculator.tbse_consumption_per_trim
    delta_ibt_plus = diff_consumption[diff_consumption >= 0]
    delta_ibt_minus = diff_consumption[diff_consumption < 0]
    g1_delta_ibt_plus = diff_consumption[(diff_consumption >= 0) & (simulation_calculator.is_sanitation() == 0)]
    g1_delta_ibt_minus = diff_consumption[(diff_consumption < 0) & (simulation_calculator.is_sanitation() == 0)]
    g2_delta_ibt_plus = diff_consumption[(diff_consumption >= 0) & (simulation_calculator.is_sanitation() == 1)]
    g2_delta_ibt_minus = diff_consumption[(diff_consumption < 0) & (simulation_calculator.is_sanitation() == 1)]
    poor_delta_ibt_plus = diff_consumption[(diff_consumption >= 0) & (simulation_calculator.is_poor == True)]
    poor_delta_ibt_minus = diff_consumption[(diff_consumption < 0) & (simulation_calculator.is_poor == True)]
    nonpoor_delta_ibt_plus = diff_consumption[(diff_consumption >= 0) & (simulation_calculator.is_poor == False)]
    nonpoor_delta_ibt_minus = diff_consumption[(diff_consumption < 0) & (simulation_calculator.is_poor == False)]

    return GroupDecomposition(
        ensemble=OverconsumptionDecompositionRow(
            frequency=100,
            delta_c_moyen=diff_consumption.mean(),
            variance=diff_consumption.var(ddof=1),
        ),
        delta_plus=OverconsumptionDecompositionRow(
            frequency=len(delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=delta_ibt_plus.mean(),
            variance=delta_ibt_plus.var(ddof=1),
        ),
        delta_minus=OverconsumptionDecompositionRow(
            frequency=len(delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=delta_ibt_minus.mean(),
            variance=delta_ibt_minus.var(ddof=1),
        ),
        g1_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(g1_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=g1_delta_ibt_plus.mean(),
            variance=g1_delta_ibt_plus.var(ddof=1),
        ),
        g1_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(g1_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=g1_delta_ibt_minus.mean(),
            variance=g1_delta_ibt_minus.var(ddof=1),
        ),
        g2_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(g2_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=(g2_delta_ibt_plus.mean()),
            variance=(g2_delta_ibt_plus.var(ddof=1)),
        ),
        g2_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(g2_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=(g2_delta_ibt_minus.mean()),
            variance=(g2_delta_ibt_minus.var(ddof=1)),
        ),
        poor_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(poor_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=(poor_delta_ibt_plus.mean()),
            variance=(poor_delta_ibt_plus.var(ddof=1)),
        ),
        poor_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(poor_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=(poor_delta_ibt_minus.mean()),
            variance=(poor_delta_ibt_minus.var(ddof=1)),
        ),
        nonpoor_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(nonpoor_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=(nonpoor_delta_ibt_plus.mean()),
            variance=(nonpoor_delta_ibt_plus.var(ddof=1)),
        ),
        nonpoor_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(nonpoor_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=(nonpoor_delta_ibt_minus.mean()),
            variance=(nonpoor_delta_ibt_minus.var(ddof=1)),
        )
    )


def increase_contingency_table_household_percentage(simulation_calculator: NewSimulation) -> SquareTable:
    diff_consumption = simulation_calculator.bcp_consumptions[
                           simulation_calculator.simulation.launch.periods] - simulation_calculator.tbse_consumption_per_trim
    return contingence_table(simulation_calculator, diff_consumption >= 0, (diff_consumption >= 0).astype(float))


def decrease_contingency_table_household_percentage(simulation_calculator: NewSimulation) -> SquareTable:
    diff_consumption = simulation_calculator.bcp_consumptions[
                           simulation_calculator.simulation.launch.periods] - simulation_calculator.tbse_consumption_per_trim
    return contingence_table(simulation_calculator, diff_consumption < 0, (diff_consumption < 0).astype(float))


def increase_contingency_table_consumption(simulation_calculator: NewSimulation) -> SquareTable:
    diff_consumption = simulation_calculator.bcp_consumptions[
                           simulation_calculator.simulation.launch.periods] - simulation_calculator.tbse_consumption_per_trim
    return contingence_table(simulation_calculator, diff_consumption >= 0, diff_consumption)


def decrease_contingency_table_consumption(simulation_calculator: NewSimulation) -> SquareTable:
    diff_consumption = simulation_calculator.bcp_consumptions[
                           simulation_calculator.simulation.launch.periods] - simulation_calculator.tbse_consumption_per_trim
    return contingence_table(simulation_calculator, diff_consumption < 0, diff_consumption)


def contingence_table(simulation_calculator: NewSimulation, condition, column_feature):
    total_length = len(simulation_calculator.df)

    return SquareTable(
        g1=SquareRow(
            poor=column_feature[condition & (simulation_calculator.is_sanitation() == False) & (
                    simulation_calculator.is_poor == True)].sum() / total_length * 100,
            nonpoor=column_feature[condition & (simulation_calculator.is_sanitation() == False) & (
                    simulation_calculator.is_poor == False)].sum() / total_length * 100,
            ensemble=column_feature[
                         condition & (simulation_calculator.is_sanitation() == False)].sum() / total_length * 100,
        ),
        g2=SquareRow(
            poor=column_feature[condition & (simulation_calculator.is_sanitation() == True) & (
                    simulation_calculator.is_poor == True)].sum() / total_length * 100,
            nonpoor=column_feature[condition & (simulation_calculator.is_sanitation() == True) & (
                    simulation_calculator.is_poor == False)].sum() / total_length * 100,
            ensemble=column_feature[
                         condition & (simulation_calculator.is_sanitation() == True)].sum() / total_length * 100,
        ),
        total_population=SquareRow(
            poor=column_feature[condition & (simulation_calculator.is_poor == True)].sum() / total_length * 100,
            nonpoor=column_feature[condition & (simulation_calculator.is_poor == False)].sum() / total_length * 100,
            ensemble=column_feature[condition].sum() / total_length * 100,
        )
    )
