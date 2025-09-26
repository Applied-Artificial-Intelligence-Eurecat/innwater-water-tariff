import numpy as np
import pandas as pd
from pydantic import BaseModel

from src.small_assessment.calculator_service import AbstractSimulation


class IncentiveConsumptionRow(BaseModel):
    ibt: float
    ibt_pp: float
    tbse: float
    actual_overconsumption: float
    overconsumption_per_capita: float


class DeltaIncentiveConsumptionRow(BaseModel):
    delta_ibt_plus: float
    delta_ibt_minus: float
    delta_ibt_pp_plus: float
    delta_ibt_pp_minus: float


class IncentiveConsumption(BaseModel):
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
    frequency: float
    delta_c_moyen: float | str
    variance: float | str


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


def delta_incentive_effect_consumption(df) -> IncentiveConsumption:
    delta_ibt = df['C_EP_BCP HM'] - df['C_et_F_TBSE P']
    delta_ibt_pp = df['C_PP BM'] - df['C_et_F_TBSE P']
    delta_ibt_plus = delta_ibt[delta_ibt >= 0]
    delta_ibt_minus = delta_ibt[delta_ibt < 0]
    delta_ibt_pp_plus = delta_ibt_pp[delta_ibt_pp >= 0]
    delta_ibt_pp_minus = delta_ibt_pp[delta_ibt_pp < 0]

    q1_row = DeltaIncentiveConsumptionRow(
        delta_ibt_plus=df['C_EP_BCP HM'].quantile(0.25),
        delta_ibt_minus=df['C_EP_BCP HM'].quantile(0.25),
        delta_ibt_pp_plus=df['C_PP BM'].quantile(0.25),
        delta_ibt_pp_minus=df['C_PP BM'].quantile(0.25)
    )
    q3_row = DeltaIncentiveConsumptionRow(
        delta_ibt_plus=df['C_EP_BCP HM'].quantile(0.75),
        delta_ibt_minus=df['C_EP_BCP HM'].quantile(0.75),
        delta_ibt_pp_plus=df['C_PP BM'].quantile(0.75),
        delta_ibt_pp_minus=df['C_PP BM'].quantile(0.75)
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
            delta_ibt_plus=df['C_EP_BCP HM'].quantile(0.1) - df['C_EP_BCP HM'].quantile(0.1),
            delta_ibt_minus=df['C_EP_BCP HM'].quantile(0.1) - df['C_EP_BCP HM'].quantile(0.1),
            delta_ibt_pp_plus=df['C_PP BM'].quantile(0.1) - df['C_PP BM'].quantile(0.1),
            delta_ibt_pp_minus=df['C_PP BM'].quantile(0.1) - df['C_PP BM'].quantile(0.1)
        ),
        d9=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=df['C_EP_BCP HM'].quantile(0.9),
            delta_ibt_minus=df['C_EP_BCP HM'].quantile(0.9),
            delta_ibt_pp_plus=df['C_PP BM'].quantile(0.9),
            delta_ibt_pp_minus=df['C_PP BM'].quantile(0.9)
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
            delta_ibt_plus=delta_ibt_plus.quantile(0.9) / delta_ibt_plus.quantile(0.1),
            delta_ibt_minus=delta_ibt_minus.quantile(0.9) / delta_ibt_minus.quantile(0.1),
            delta_ibt_pp_plus=delta_ibt_pp_plus.quantile(0.9) / delta_ibt_pp_plus.quantile(0.1),
            delta_ibt_pp_minus=delta_ibt_pp_minus.quantile(0.9) / delta_ibt_pp_minus.quantile(0.1),
        ),
        yule_coeff=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=((q3_row.delta_ibt_plus - median_row.delta_ibt_plus) - (
                    median_row.delta_ibt_plus - q1_row.delta_ibt_plus)) / (
                                   q3_row.delta_ibt_plus - q1_row.delta_ibt_plus),
            delta_ibt_minus=((q3_row.delta_ibt_minus - median_row.delta_ibt_minus) - (
                    median_row.delta_ibt_minus - q1_row.delta_ibt_minus)) / (
                                    q3_row.delta_ibt_minus - q1_row.delta_ibt_minus),
            delta_ibt_pp_plus=((q3_row.delta_ibt_pp_plus - median_row.delta_ibt_pp_plus) - (
                    median_row.delta_ibt_pp_plus - q1_row.delta_ibt_pp_plus)) / (
                                      q3_row.delta_ibt_pp_plus - q1_row.delta_ibt_pp_plus),
            delta_ibt_pp_minus=((q3_row.delta_ibt_pp_minus - median_row.delta_ibt_pp_minus) - (
                    median_row.delta_ibt_pp_minus - q1_row.delta_ibt_pp_minus)) / (
                                       q3_row.delta_ibt_pp_minus - q1_row.delta_ibt_pp_minus),
        ),
        gini_schutz=DeltaIncentiveConsumptionRow(
            delta_ibt_plus=1 - (mape_row.delta_ibt_plus / 100),
            delta_ibt_minus=1 - (mape_row.delta_ibt_minus / 100),
            delta_ibt_pp_plus=1 - (mape_row.delta_ibt_pp_plus / 100),
            delta_ibt_pp_minus=1 - (mape_row.delta_ibt_pp_minus / 100),
        )
    )


def incentive_effect_consumption(df) -> IncentiveConsumption:
    actual_overconsumption = (df['C_EP_BCP HM'] - df['C_PP BM']).replace(0, pd.NA)
    consumption_per_capita = actual_overconsumption / df['nbpers']
    mean_row = IncentiveConsumptionRow(ibt=df['C_EP_BCP HM'].mean(), ibt_pp=df['C_PP BM'].mean(),
                                       tbse=df['C_et_F_TBSE P'].mean(),
                                       actual_overconsumption=actual_overconsumption.mean(),
                                       overconsumption_per_capita=(consumption_per_capita).mean())
    median_row = IncentiveConsumptionRow(ibt=df['C_EP_BCP HM'].median(), ibt_pp=df['C_PP BM'].median(),
                                         tbse=df['C_et_F_TBSE P'].median(),
                                         actual_overconsumption=actual_overconsumption.median(),
                                         overconsumption_per_capita=(consumption_per_capita).median())
    q1_row = IncentiveConsumptionRow(ibt=df['C_EP_BCP HM'].quantile(0.25), ibt_pp=df['C_PP BM'].quantile(0.25),
                                     tbse=df['C_et_F_TBSE P'].quantile(0.25),
                                     actual_overconsumption=actual_overconsumption.quantile(0.25),
                                     overconsumption_per_capita=(consumption_per_capita).quantile(0.25))
    q3_row = IncentiveConsumptionRow(ibt=df['C_EP_BCP HM'].quantile(0.75), ibt_pp=df['C_PP BM'].quantile(0.75),
                                     tbse=df['C_et_F_TBSE P'].quantile(0.75),
                                     actual_overconsumption=actual_overconsumption.quantile(0.75),
                                     overconsumption_per_capita=(consumption_per_capita).quantile(0.75))
    mape_row = IncentiveConsumptionRow(ibt=desvprom(df['C_EP_BCP HM']), ibt_pp=desvprom(df['C_PP BM']),
                                       tbse=desvprom(df['C_et_F_TBSE P']),
                                       actual_overconsumption=desvprom(actual_overconsumption),
                                       overconsumption_per_capita=desvprom(consumption_per_capita))
    return IncentiveConsumption(
        mean=mean_row,
        median=median_row,
        min=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].min(),
            ibt_pp=df['C_PP BM'].min(),
            tbse=df['C_et_F_TBSE P'].min(),
            actual_overconsumption=actual_overconsumption.min(),
            overconsumption_per_capita=(consumption_per_capita).min()
        ),
        max=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].max(),
            ibt_pp=df['C_PP BM'].max(),
            tbse=df['C_et_F_TBSE P'].max(),
            actual_overconsumption=actual_overconsumption.max(),
            overconsumption_per_capita=(consumption_per_capita).max()
        ),
        q1=q1_row,
        q3=q3_row,
        d1=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].quantile(0.1) - df['C_EP_BCP HM'].quantile(0.1),
            ibt_pp=df['C_PP BM'].quantile(0.1) - df['C_PP BM'].quantile(0.1),
            tbse=df['C_et_F_TBSE P'].quantile(0.1) - df['C_et_F_TBSE P'].quantile(0.1),
            actual_overconsumption=actual_overconsumption.quantile(0.1),
            overconsumption_per_capita=(consumption_per_capita).quantile(0.1)
        ),
        d9=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].quantile(0.9),
            ibt_pp=df['C_PP BM'].quantile(0.9),
            tbse=df['C_et_F_TBSE P'].quantile(0.9),
            actual_overconsumption=actual_overconsumption.quantile(0.9),
            overconsumption_per_capita=(consumption_per_capita).quantile(0.9)
        ),
        percentile_rank=IncentiveConsumptionRow(
            ibt=percentrank_inc(df['C_EP_BCP HM'], df['C_EP_BCP HM'].mean()),
            ibt_pp=percentrank_inc(df['C_PP BM'], df['C_PP BM'].mean()),
            tbse=percentrank_inc(df['C_et_F_TBSE P'], df['C_et_F_TBSE P'].mean()),
            actual_overconsumption=percentrank_inc(actual_overconsumption, actual_overconsumption.mean()),
            overconsumption_per_capita=percentrank_inc(consumption_per_capita,
                                                       consumption_per_capita.mean())
        ),
        variance=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].var(),
            ibt_pp=df['C_PP BM'].var(),
            tbse=df['C_et_F_TBSE P'].var(),
            actual_overconsumption=actual_overconsumption.var(),
            overconsumption_per_capita=(consumption_per_capita).var()
        ),
        ecart_type=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].std(),
            ibt_pp=df['C_PP BM'].std(),
            tbse=df['C_et_F_TBSE P'].std(),
            actual_overconsumption=actual_overconsumption.std(),
            overconsumption_per_capita=(consumption_per_capita).std()
        ),
        mape=mape_row,
        variation_coeff=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].std() / df['C_EP_BCP HM'].mean(),
            ibt_pp=df['C_PP BM'].std() / df['C_PP BM'].mean(),
            tbse=df['C_et_F_TBSE P'].std() / df['C_et_F_TBSE P'].mean(),
            actual_overconsumption=df['C_EP_BCP HM'].std() / df['C_EP_BCP HM'].mean(),
            overconsumption_per_capita=df['C_EP_BCP HM'].std() / df['C_EP_BCP HM'].mean(),
        ),
        iqr=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].quantile(0.75) - df['C_EP_BCP HM'].quantile(0.25),
            ibt_pp=df['C_PP BM'].quantile(0.75) - df['C_PP BM'].quantile(0.25),
            tbse=df['C_et_F_TBSE P'].quantile(0.75) - df['C_et_F_TBSE P'].quantile(0.25),
            actual_overconsumption=df['C_EP_BCP HM'].quantile(0.75) - df['C_EP_BCP HM'].quantile(0.25),
            overconsumption_per_capita=df['C_EP_BCP HM'].quantile(0.75) - df['C_EP_BCP HM'].quantile(0.25),
        ),
        idr=IncentiveConsumptionRow(
            ibt=df['C_EP_BCP HM'].quantile(0.9) / df['C_EP_BCP HM'].quantile(0.1),
            ibt_pp=df['C_PP BM'].quantile(0.9) / df['C_PP BM'].quantile(0.1),
            tbse=df['C_et_F_TBSE P'].quantile(0.9) / df['C_et_F_TBSE P'].quantile(0.1),
            actual_overconsumption=df['C_EP_BCP HM'].quantile(0.9) / df['C_EP_BCP HM'].quantile(0.1),
            overconsumption_per_capita=df['C_EP_BCP HM'].quantile(0.9) / df['C_EP_BCP HM'].quantile(0.1),
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


def overconsumption_decomposition(simulation_calculator: AbstractSimulation) -> OverconsumptionDecomposition:
    df = simulation_calculator.df
    households_percentage_delta_c_moyen = (df['C_EP_BCP HM'] - df['C_PP BM']).replace(0, pd.NA).mean()
    g1_frequency = df.loc[(df['Donnees K'] > 0) & (df[simulation_calculator.is_sanitation] == 0), 'Donnees K'].sum() / \
                   df.loc[
                       df['Donnees K'] > 0, 'Donnees K'].sum() * 100
    g1_delta_c_moyen = df.loc[
        (df['Donnees J'] > 0) & (df[simulation_calculator.is_sanitation] == 0), 'C_EP_BCP J'].mean()
    g2_frequency = df.loc[(df['Donnees K'] > 0) & (df[simulation_calculator.is_sanitation] == 1), 'Donnees K'].sum() / \
                   df.loc[
                       (df['Donnees K'] > 0), 'Donnees K'].sum()
    g2_delta_c_moyen = df.loc[
        (df['Donnees J'] > 0) & (df[simulation_calculator.is_sanitation] == 1), 'C_EP_BCP J'].mean()

    g1_var = df.loc[(df['Donnees J'] != 0) & df[simulation_calculator.is_sanitation] == 0, 'Donnees J'].var(ddof=1)
    g2_var = df.loc[(df['Donnees J'] != 0) & df[simulation_calculator.is_sanitation] == 1, 'Donnees J'].var(ddof=1)
    households_var = (df['C_EP_BCP HM'] - df['C_PP BM']).replace(0, pd.NA).var()
    return OverconsumptionDecomposition(
        households_percentage=OverconsumptionDecompositionRow(
            frequency=(df['Donnees K']).astype(float).sum() / len(df) * 100,
            delta_c_moyen=households_percentage_delta_c_moyen,
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
            frequency=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 1), 'Donnees K'].sum() / df.loc[
                (df['Donnees K'] > 0), 'Donnees K'].sum() * 100,
            delta_c_moyen=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 1), 'C_EP_BCP J'].mean(),
            variance=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 1), 'Donnees J'].var(ddof=1),
            # percentage=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 1), 'Donnees J'].mean() / df.loc[   (df['Donnees K'] > 0) & (df['poor'] == 1), 'Donnees J'].var(ddof=1)
        ),
        nonpoor=OverconsumptionDecompositionRow(
            frequency=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 0), 'Donnees K'].sum() / df.loc[
                (df['Donnees K'] > 0), 'Donnees K'].sum() * 100,
            delta_c_moyen=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 0), 'C_EP_BCP J'].mean(),
            variance=df.loc[(df['Donnees K'] > 0) & (df['poor'] == 0), 'Donnees J'].var(ddof=1),
        )
    )


def composition_of_households_that_overconsume(simulation_calculator: AbstractSimulation):
    df = simulation_calculator.df

    den = df['Donnees K'].sum()

    g1_row = SquareRow(
        poor=df.loc[(df[simulation_calculator.is_sanitation] == 0) & (df['poor'] == 1), 'Donnees K'].sum() / den * 100,
        nonpoor=df.loc[
                    (df[simulation_calculator.is_sanitation] == 0) & (df['poor'] == 0), 'Donnees K'].sum() / den * 100,
        ensemble=df.loc[(df[simulation_calculator.is_sanitation] == 0), 'Donnees K'].sum() / den * 100,
    )
    g2_row = SquareRow(
        poor=df.loc[(df[simulation_calculator.is_sanitation] == 1) & (df['poor'] == 1), 'Donnees K'].sum() / den * 100,
        nonpoor=df.loc[
                    (df[simulation_calculator.is_sanitation] == 1) & (df['poor'] == 0), 'Donnees K'].sum() / den * 100,
        ensemble=df.loc[(df[simulation_calculator.is_sanitation] == 1), 'Donnees K'].sum() / den * 100,
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


def breakdown_of_overconsumption(simulation_calculator: AbstractSimulation):
    df = simulation_calculator.df
    den = df.loc[df['Donnees J'] > 0, 'Donnees J'].sum()
    col = 'Donnees J'
    g1 = SquareRow(
        poor=df.loc[(df[col] > 0) & (df[simulation_calculator.is_sanitation] == 0) & (
                df['poor'] == 1), col].sum() / den * 100,
        nonpoor=df.loc[(df[col] > 0) & (df[simulation_calculator.is_sanitation] == 0) & (
                df['poor'] == 0), col].sum() / den * 100,
        ensemble=df.loc[(df[col] > 0) & (
                df[simulation_calculator.is_sanitation] == 0), col].sum() / den * 100,
    )
    g2 = SquareRow(
        poor=df.loc[(df[col] > 0) & (df[simulation_calculator.is_sanitation] == 1) & (
                df['poor'] == 1), col].sum() / den * 100,
        nonpoor=df.loc[(df[col] > 0) & (df[simulation_calculator.is_sanitation] == 1) & (
                df['poor'] == 0), col].sum() / den * 100,
        ensemble=df.loc[(df[col] > 0) & (
                df[simulation_calculator.is_sanitation] == 1), col].sum() / den * 100,
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


def decomposition_table(simulation_calculator: AbstractSimulation) -> GroupDecomposition:
    df = simulation_calculator.df
    col = 'Donnees U'
    delta_ibt_plus = df.loc[df[col] >= 0, col]
    delta_ibt_minus = df.loc[df[col] < 0, col]
    g1_delta_ibt_plus = df.loc[(df[col] >= 0) & (df[simulation_calculator.is_sanitation] == 0), col]
    g1_delta_ibt_minus = df.loc[(df[col] < 0) & (df[simulation_calculator.is_sanitation] == 0), col]
    g2_delta_ibt_plus = df.loc[(df[col] >= 0) & (df[simulation_calculator.is_sanitation] == 1), col]
    g2_delta_ibt_minus = df.loc[(df[col] < 0) & (df[simulation_calculator.is_sanitation] == 1), col]
    poor_delta_ibt_plus = df.loc[(df[col] >= 0) & (df['poor'] == 1), col]
    poor_delta_ibt_minus = df.loc[(df[col] < 0) & (df['poor'] == 1), col]
    nonpoor_delta_ibt_plus = df.loc[(df[col] >= 0) & (df['poor'] == 0), col]
    nonpoor_delta_ibt_minus = df.loc[(df[col] < 0) & (df['poor'] == 0), col]
    return GroupDecomposition(
        ensemble=OverconsumptionDecompositionRow(
            frequency=100,
            delta_c_moyen=df['Donnees U'].mean(),
            variance=df['Donnees U'].var(ddof=1),
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
            delta_c_moyen=str(g1_delta_ibt_minus.mean()),
            variance=str(g1_delta_ibt_minus.var(ddof=1)),
        ),
        g2_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(g2_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=str(g2_delta_ibt_plus.mean()) ,
            variance=str(g2_delta_ibt_plus.var(ddof=1)),
        ),
        g2_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(g2_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=str(g2_delta_ibt_minus.mean()),
            variance=str(g2_delta_ibt_minus.var(ddof=1)),
        ),
        poor_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(poor_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=str(poor_delta_ibt_plus.mean()),
            variance=str(poor_delta_ibt_plus.var(ddof=1)),
        ),
        poor_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(poor_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=str(poor_delta_ibt_minus.mean()),
            variance=str(poor_delta_ibt_minus.var(ddof=1)),
        ),
        nonpoor_delta_plus=OverconsumptionDecompositionRow(
            frequency=len(nonpoor_delta_ibt_plus) / len(df) * 100,
            delta_c_moyen=str(nonpoor_delta_ibt_plus.mean()),
            variance=str(nonpoor_delta_ibt_plus.var(ddof=1)),
        ),
        nonpoor_delta_minus=OverconsumptionDecompositionRow(
            frequency=len(nonpoor_delta_ibt_minus) / len(df) * 100,
            delta_c_moyen=str(nonpoor_delta_ibt_minus.mean()),
            variance=str(nonpoor_delta_ibt_minus.var(ddof=1)),
        )
    )


def increase_contingency_table_household_percentage(simulation_calculator: AbstractSimulation) -> SquareTable:
    df = simulation_calculator.df
    increase_df = df.loc[df['Donnees U'] >= 0]
    variable = 'Donnees X'
    return contingence_table(increase_df, df, simulation_calculator, variable)


def decrease_contingency_table_household_percentage(simulation_calculator: AbstractSimulation) -> SquareTable:
    df = simulation_calculator.df
    decrease_df = df.loc[df['Donnees U'] < 0]
    variable = 'Donnees X'
    return contingence_table(decrease_df, df, simulation_calculator, variable)


def increase_contingency_table_consumption(simulation_calculator: AbstractSimulation) -> SquareTable:
    df = simulation_calculator.df
    increase_df = df.loc[df['Donnees U'] >= 0]
    variable = 'Donnees U'
    return contingence_table(increase_df, df, simulation_calculator, variable)


def decrease_contingency_table_consumption(simulation_calculator: AbstractSimulation) -> SquareTable:
    df = simulation_calculator.df
    decrease_df = df.loc[df['Donnees U'] < 0]
    variable = 'Donnees U'
    return contingence_table(decrease_df, df, simulation_calculator, variable)


def contingence_table(variable_df, df, simulation_calculator, column_feature):
    return SquareTable(
        g1=SquareRow(
            poor=variable_df.loc[(variable_df[simulation_calculator.is_sanitation] == 0) & (
                    variable_df['poor'] == 1), column_feature].sum() / len(
                df) * 100,
            nonpoor=variable_df.loc[(variable_df[simulation_calculator.is_sanitation] == 0) & (
                    variable_df['poor'] == 0), column_feature].sum() / len(
                df) * 100,
            ensemble=variable_df.loc[
                         (variable_df[simulation_calculator.is_sanitation] == 0), column_feature].sum() / len(
                df) * 100,
        ),
        g2=SquareRow(
            poor=variable_df.loc[(variable_df[simulation_calculator.is_sanitation] == 1) & (
                    variable_df['poor'] == 1), column_feature].sum() / len(
                df) * 100,
            nonpoor=variable_df.loc[(variable_df[simulation_calculator.is_sanitation] == 1) & (
                    variable_df['poor'] == 0), column_feature].sum() / len(df) * 100,
            ensemble=variable_df.loc[
                         (variable_df[simulation_calculator.is_sanitation] == 1), column_feature].sum() / len(
                df) * 100,
        ),
        total_population=SquareRow(
            poor=variable_df.loc[variable_df['poor'] == 1, column_feature].sum() / len(df) * 100,
            nonpoor=variable_df.loc[variable_df['poor'] == 0, column_feature].sum() / len(df) * 100,
            ensemble=variable_df[column_feature].sum() / len(df) * 100,
        )
    )
