import numpy as np
from pydantic import BaseModel


class AffordabilityRow(BaseModel):
    ibt: float
    tbse: float


class AffordabilityGeneral(BaseModel):
    """
    Attributes:
        headcount_ratio: Represents the headcount ratio as an affordability metric.
        aparent_deficit: Represents the apparent deficit as an affordability metric.
        efective_deficit: Represents the effective deficit as an affordability metric.
        gini_index: Represents the Gini index as an affordability metric.
    """
    headcount_ratio: AffordabilityRow
    aparent_deficit: AffordabilityRow
    efective_deficit: AffordabilityRow
    gini_index: AffordabilityRow


def affordability_general(df) -> AffordabilityGeneral:
    aparent_ibt = df['VAR_PAR_Menages AX'].mean()
    cov_ibt = np.cov(df['VAR_PAR_Menages AX'].sort_values(), df['VAR_PAR_Menages BU'], bias=True)[0, 1]
    cov_tbse = np.cov(df['VAR_PAR_Menages AY'].sort_values(), df['VAR_PAR_Menages BD'], bias=True)[0, 1]
    aparent_tbse = df['VAR_PAR_Menages AY'].mean()
    return AffordabilityGeneral(
        headcount_ratio=AffordabilityRow(
            ibt=df['VAR_PAR_Menages AP'].sum() * 100 / len(df),
            tbse=df['VAR_PAR_Menages AQ'].sum() * 100 / len(df),
        ),
        # PROMEDIO('Var_PAR Ménages'!AX8:AX465)
        aparent_deficit=AffordabilityRow(
            ibt=aparent_ibt,
            tbse=aparent_tbse
        ),
        efective_deficit=AffordabilityRow(
            ibt=df.loc[df['VAR_PAR_Menages AX'] > 0, 'VAR_PAR_Menages AX'].mean(),
            tbse=df.loc[df['VAR_PAR_Menages AY'] > 0, 'VAR_PAR_Menages AY'].mean()
        ),
        gini_index=AffordabilityRow(
            ibt=2 * cov_ibt / aparent_ibt,
            tbse=2 * cov_tbse / aparent_tbse,
        ),
    )
