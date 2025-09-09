from typing import Optional, Literal, List

from pydantic import BaseModel


class GeneralRow(BaseModel):
    metric: str
    par_ibt: Optional[float]
    par_tbse: Optional[float]
    delta_par: Optional[float]
    car_ibt: Optional[float]
    car_tbse: Optional[float]
    delta_car: Optional[float]


class GeneralGroupRow(BaseModel):
    metric: str
    par_ibt_g1: Optional[float] = None
    par_ibt_g2: Optional[float] = None
    par_tbse_g1: Optional[float] = None
    par_tbse_g2: Optional[float] = None
    car_ibt_g1: Optional[float] = None
    car_ibt_g2: Optional[float] = None
    car_tbse_g1: Optional[float] = None
    car_tbse_g2: Optional[float] = None


class HeadcountBreakdownRow(BaseModel):
    group: Literal["EP", "EPA", "Total"]
    f_i: float
    par_ibt_households: float
    par_ibt_individuals: float
    par_ibt_children: float
    par_tbse_households: float
    par_tbse_individuals: float
    par_tbse_children: float
    delta_households: float
    delta_individuals: float
    delta_children: float


class ApparentDeficitRow(BaseModel):
    group: Literal["EP", "EPA", "Total"]
    f_i_menages: Optional[float] = None

    mean_par_ibt: Optional[float] = None
    variance_par_ibt: Optional[float] = None

    corr_coef_group_1: Optional[str] = None
    corr_coef_value_1: Optional[float] = None

    # PAR TBSE
    f_i_par_tbse: Optional[float] = None
    mean_par_tbse: Optional[float] = None
    variance_par_tbse: Optional[float] = None

    corr_coef_group_2: Optional[str] = None
    corr_coef_value_2: Optional[float] = None



class GiniComponent(BaseModel):
    name: str
    value: float
    percentage: float

class GiniPARResult(BaseModel):
    components: List[GiniComponent]


class WeightMatrixRow(BaseModel):
    group: Literal["G1", "G2", "Total"]  # G1, G2, Total
    fj: float
    aj: float
    wij: float | None
    final_weight: float | None

class WeightMatrix(BaseModel):
    rows: List[WeightMatrixRow]