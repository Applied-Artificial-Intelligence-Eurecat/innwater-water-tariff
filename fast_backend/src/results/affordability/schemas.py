from pydantic import BaseModel


class GeneralRow(BaseModel):
    par_ibt_g1: float | None
    par_ibt_g2: float | None
    par_tbse_g1: float | None
    par_tbse_g2: float | None


class AugmentedGeneralRow(GeneralRow):
    delta_par_g1: float | None
    delta_par_g2: float | None


class GeneralStatistic(BaseModel):
    mean: AugmentedGeneralRow
    median: AugmentedGeneralRow
    min: GeneralRow
    max: GeneralRow
    q1: GeneralRow
    q3: GeneralRow
    d1: GeneralRow
    d9: GeneralRow
    f: GeneralRow
    variance: GeneralRow
    ecart_type: GeneralRow
    MAPE: GeneralRow
    coeff_variation: GeneralRow


class GiniDecompRow(BaseModel):
    value: float | None
    perc: float | None


class GiniDecompTable(BaseModel):
    between: GiniDecompRow
    within: GiniDecompRow
    transvariation: GiniDecompRow
    ensemble: GiniDecompRow


class OutputGiniDecomp(BaseModel):
    par_ibt: GiniDecompTable
    par_tbse: GiniDecompTable
    excess_par_ibt: GiniDecompTable
    excess_par_tbse: GiniDecompTable
