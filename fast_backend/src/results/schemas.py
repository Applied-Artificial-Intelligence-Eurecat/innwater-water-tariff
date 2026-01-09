from typing import Optional

from pydantic import BaseModel, Field


class AffordabilityColumnValues(BaseModel):
    ibt: float | None
    tbse: float | None


class AffordabilityTable(BaseModel):
    headcount_ratio: AffordabilityColumnValues = Field(..., description="Headcount ratio (%)")
    apparent_affordability_deficit: AffordabilityColumnValues = Field(..., description="App. Afford. Deficit (€)")
    effective_affordability_deficit: AffordabilityColumnValues = Field(..., description="Effec. Afford. Deficit (€)")
    gini_app: AffordabilityColumnValues = Field(..., description="Gini coefficient (apparent)")
    gini_eff: AffordabilityColumnValues = Field(..., description="Gini coefficient (effective)")


class ConsumptionValues(BaseModel):
    average_consumption_m3_trim: float | None = Field(..., description="Average water consumption (m³ / trimester)")
    average_bill_eur_trim: float | None = Field(..., description="Average bill (€ / trimester)")


class IncentiveConsumptionTable(BaseModel):
    ibt: ConsumptionValues
    ibt_pp: ConsumptionValues
    ibt_tbse: ConsumptionValues


class EfficiencyMetrics(BaseModel):
    eff_overconsumption: float | None = Field(..., description="Effective overconsumption")
    eff_mismanagement_cost: float | None = Field(..., description="Effective mismanagement cost (€)")


class IncentiveEfficiencyTable(BaseModel):
    per_h: EfficiencyMetrics
    per_ind: EfficiencyMetrics




class EconomicEfficiencyRow(BaseModel):
    conso: Optional[float] = Field(None, description="Consumption (m³ / trimester)")
    delta_w: Optional[float] = Field(None, description="Delta in welfare (€ / trimester)")


class EconomicEfficiencyTable(BaseModel):
    first_best: EconomicEfficiencyRow
    delta_tbse_a: EconomicEfficiencyRow
    delta_ibt_a: EconomicEfficiencyRow
    delta_ibt_pp_a: EconomicEfficiencyRow
    impact_overconsumption: EconomicEfficiencyRow


class EquityGiniIndexTable(BaseModel):
    ibt: Optional[float] = Field(None, description="Net Income Gini Index for IBT")
    ibt_ae: Optional[float] = Field(None, description="Net Income Gini Index for IBT-AE")
    tbse: Optional[float] = Field(None, description="Net Income Gini Index for TBSE")

class BasicConsumptionEquityRow(BaseModel):
    dae: Optional[float]
    dai: Optional[float]


class BasicConsumptionEquityTable(BaseModel):
    net_sub_basic_c: BasicConsumptionEquityRow
    omega_ratio_1: BasicConsumptionEquityRow
    net_taxes_basic_c: BasicConsumptionEquityRow
    omega_ratio_2: BasicConsumptionEquityRow


class FullConsumptionEquityRow(BaseModel):
    afe: Optional[float]
    afi: Optional[float]


class FullConsumptionEquityTable(BaseModel):
    net_sub_c: FullConsumptionEquityRow
    omega_ratio_1: FullConsumptionEquityRow
    net_taxation: FullConsumptionEquityRow
    omega_ratio_2: FullConsumptionEquityRow

from typing import Optional
from pydantic import BaseModel, Field


class FundingMetricRow(BaseModel):
    dae: Optional[float] = None
    dai: Optional[float] = None


class FundingTable(BaseModel):
    net_contributors_percent: Optional[float] = Field(None, description="% Households that are net contributors")
    net_beneficiaries_percent: Optional[float] = Field(None, description="% Households that are net beneficiaries")
    subsidized_basic_c_percent: Optional[float] = Field(None, description="Subsidized basic consumption (%)")
    subsidized_non_basic_c_percent: Optional[float] = Field(None, description="Subsidized non-basic consumption (%)")
    margined_c_percent: Optional[float] = Field(None, description="Margined consumption (%)")
    bad_sub_percent: FundingMetricRow = Field(FundingMetricRow(), description='"Bad" Subsidy (%)')
    bad_tax_percent: FundingMetricRow = Field(FundingMetricRow(), description='"Bad" Taxation (%)')


class EnvironmentalCostTable(BaseModel):
    tbse_conso_rang_1: Optional[float] = Field(None, description="Environmental cost for TBSE Conso Rang 1 (€/trim)")
    effective_tbse: Optional[float] = Field(None, description="Environmental cost for Effective TBSE (€/trim)")
    ibt: Optional[float] = Field(None, description="Environmental cost for IBT (€/trim)")
    ibt_pp: Optional[float] = Field(None, description="Environmental cost for IBT_PP (€/trim)")

class WaterAgencyTable(BaseModel):
    exercise_duty: float | None

class StateTable(BaseModel):
    vat: float | None
