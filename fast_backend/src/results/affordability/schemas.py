from pydantic import BaseModel


class GroupRow(BaseModel):
    par_ibt_g1: float | None
    par_ibt_g2: float | None
    par_tbse_g1: float | None
    par_tbse_g2: float | None


class AugmentedGroupRow(GroupRow):
    delta_par_g1: float | None
    delta_par_g2: float | None


class GeneralRow(BaseModel):
    par_ibt: float | None
    par_tbse: float | None


class AugmentedGeneralRow(GeneralRow):
    delta_par: float | None


class DeficitTable(BaseModel):
    mean: AugmentedGeneralRow
    median: GeneralRow
    d1: GeneralRow
    d9: GeneralRow
    variance: GeneralRow
    ecart_type: GeneralRow
    cv: GeneralRow
    mape: GeneralRow


class GeneralStatistic(BaseModel):
    mean: AugmentedGroupRow | AugmentedGeneralRow
    median: AugmentedGroupRow | AugmentedGeneralRow
    min: GroupRow | GeneralRow
    max: GroupRow | GeneralRow
    q1: GroupRow | GeneralRow
    q3: GroupRow | GeneralRow
    d1: GroupRow | GeneralRow
    d9: GroupRow | GeneralRow
    f: GroupRow | GeneralRow
    variance: GroupRow | GeneralRow
    ecart_type: GroupRow | GeneralRow
    MAPE: GroupRow | GeneralRow
    coeff_variation: GroupRow | GeneralRow


class GeneralHeadcountRatio(BaseModel):
    household: AugmentedGeneralRow
    people: AugmentedGeneralRow
    children: AugmentedGeneralRow


class GroupIncidenceRow(BaseModel):
    perc_household: float
    ibt_household: float
    perc_people: float
    ibt_people: float
    perc_children: float
    ibt_children: float
    tbse_household: float
    tbse_people: float
    tbse_children: float


class GroupIncidenceTable(BaseModel):
    g1: GroupIncidenceRow
    g2: GroupIncidenceRow
    total: GroupIncidenceRow


class InequalityTable(BaseModel):
    gini: GeneralRow
    schutz: GeneralRow


class RowDeficit(BaseModel):
    perc: float
    mean: float
    var: float


class GroupDeficit(BaseModel):
    g1: RowDeficit
    g2: RowDeficit
    ensemble: RowDeficit


class AugmentedGroupDeficit(GroupDeficit):
    var_inter: float
    var_intra: float
    rap_corr: float


def from_group_deficit_to_augmented(group_deficit: GroupDeficit) -> AugmentedGroupDeficit:
    var_inter = (group_deficit.g1.perc * (
            group_deficit.g1.mean - group_deficit.ensemble.mean) ** 2 + group_deficit.g2.perc * (
                        group_deficit.g2.mean - group_deficit.ensemble.mean) ** 2) / 100
    return AugmentedGroupDeficit(g1=group_deficit.g1, g2=group_deficit.g2, ensemble=group_deficit.ensemble,
                                 var_inter=var_inter,
                                 var_intra=(
                                                       group_deficit.g1.perc * group_deficit.g1.var + group_deficit.g2.perc * group_deficit.g2.var) / 100,
                                 rap_corr=var_inter / group_deficit.ensemble.var * 100)


class DeficitAffordabilityTable(BaseModel):
    par_ibt: AugmentedGroupDeficit
    par_tbse: AugmentedGroupDeficit


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
