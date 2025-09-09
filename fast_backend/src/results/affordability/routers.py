from typing import Dict

from fastapi import APIRouter

from .schemas import *

affordability_router = APIRouter(prefix="/affordability",
                                 tags=["affordability"],
                                 responses={404: {"description": "Not found"}},

                                 )


@affordability_router.get("/{simulation_id}/general", response_model=List[GeneralRow])
async def get_general_affordability_indicators(simulation_id):
    return [
        GeneralRow(metric="Mean", par_ibt=1.1, par_tbse=3.2, delta_par=-2.0, car_ibt=2.5, car_tbse=4.1,
                   delta_car=-1.57),
        GeneralRow(metric="Median", par_ibt=0.7, par_tbse=2.0, delta_par=-1.3, car_ibt=1.9, car_tbse=2.9,
                   delta_car=-0.99),

        GeneralRow(metric="Min", par_ibt=0.0, par_tbse=0.1, delta_par=None, car_ibt=0.3, car_tbse=0.3, delta_car=None),
        GeneralRow(metric="Max", par_ibt=10.9, par_tbse=21.9, delta_par=None, car_ibt=12.6, car_tbse=23.6,
                   delta_car=None),
        GeneralRow(metric="Q1", par_ibt=0.3, par_tbse=0.9, delta_par=None, car_ibt=1.0, car_tbse=1.4, delta_car=None),
        GeneralRow(metric="Q3", par_ibt=1.4, par_tbse=3.9, delta_par=None, car_ibt=3.3, car_tbse=5.0, delta_car=None),
        GeneralRow(metric="D1", par_ibt=0.1, par_tbse=0.5, delta_par=None, car_ibt=0.6, car_tbse=0.8, delta_car=None),
        GeneralRow(metric="D9", par_ibt=2.6, par_tbse=8.0, delta_par=None, car_ibt=5.4, car_tbse=9.6, delta_car=None),
        GeneralRow(metric="F (Mean)", par_ibt=68.5, par_tbse=69.3, delta_par=None, car_ibt=63.0, car_tbse=68.1,
                   delta_car=None),

        GeneralRow(metric="Variance", par_ibt=1.89, par_tbse=12.64, delta_par=None, car_ibt=4.24, car_tbse=15.73,
                   delta_car=None),
        GeneralRow(metric="Standard dev.", par_ibt=1.4, par_tbse=3.6, delta_par=None, car_ibt=2.06, car_tbse=3.97,
                   delta_car=None),
        GeneralRow(metric="MAPE", par_ibt=0.9, par_tbse=2.5, delta_par=None, car_ibt=1.5, car_tbse=2.9, delta_car=None),
        GeneralRow(metric="Coeff of Variation", par_ibt=1.216, par_tbse=1.119, delta_par=None, car_ibt=0.822,
                   car_tbse=0.972, delta_car=None),

        GeneralRow(metric="Interquartile range", par_ibt=1.1, par_tbse=3.0, delta_par=None, car_ibt=2.3, car_tbse=3.6,
                   delta_car=None),
        GeneralRow(metric="Interdecile range", par_ibt=2.5, par_tbse=7.5, delta_par=None, car_ibt=4.8, car_tbse=8.8,
                   delta_car=None),
        GeneralRow(metric="Yule coefficient", par_ibt=0.29, par_tbse=0.30, delta_par=None, car_ibt=0.23, car_tbse=0.18,
                   delta_car=None),

    ]


@affordability_router.get("/{simulation_id}/headcount_ratio", response_model=List[GeneralRow])
async def get_headcount_ratio(simulation_id):
    return [
        GeneralRow(metric="Household", par_ibt=7.9, par_tbse=32.8, delta_par=-24.9, car_ibt=28.8, car_tbse=48.3,
                   delta_car=-19.4),
        GeneralRow(metric="Individuals", par_ibt=7.9, par_tbse=31.6, delta_par=-23.8, car_ibt=32.6, car_tbse=48.9,
                   delta_car=-16.3),
        GeneralRow(metric="Children", par_ibt=9.9, par_tbse=35.1, delta_par=-25.2, car_ibt=38.0, car_tbse=52.3,
                   delta_car=-14.3),
    ]


@affordability_router.get("/{simulation_id}/apparent_affordability_deficit", response_model=List[GeneralRow])
async def get_apparent_affordability_deficit(simulation_id):
    return [
        GeneralRow(metric="Mean", par_ibt=1.39, par_tbse=17.47, delta_par=-16.08, car_ibt=9.51, car_tbse=29.03,
                   delta_car=-19.52),
        GeneralRow(metric="Median", par_ibt=0.00, par_tbse=0.00, delta_par=0.00, car_ibt=0.00, car_tbse=0.00,
                   delta_car=None),
        GeneralRow(metric="Variance", par_ibt=38.5366, par_tbse=1013.2596, delta_par=None, car_ibt=389.6407,
                   car_tbse=1718.7326, delta_car=None),
        GeneralRow(metric="Standard dev.", par_ibt=6.21, par_tbse=31.83, delta_par=None, car_ibt=19.74, car_tbse=41.46,
                   delta_car=None),
        GeneralRow(metric="Coeff of Variation", par_ibt=4.47, par_tbse=1.82, delta_par=None, car_ibt=2.076,
                   car_tbse=1.428, delta_car=None),
        GeneralRow(metric="MAPE", par_ibt=2.57, par_tbse=24.49, delta_par=None, car_ibt=13.97, car_tbse=34.32,
                   delta_car=None),
    ]


@affordability_router.get("/{simulation_id}/effective_affordability_deficit", response_model=List[GeneralRow])
async def get_effective_affordability_deficit(simulation_id):
    return [
        GeneralRow(metric="Mean", par_ibt=17.69, par_tbse=53.33, delta_par=-35.64, car_ibt=33.00, car_tbse=60.17,
                   delta_car=-27.17),
        GeneralRow(metric="Median", par_ibt=16.15, par_tbse=43.78, delta_par=None, car_ibt=27.85, car_tbse=52.73,
                   delta_car=None),
        GeneralRow(metric="D1", par_ibt=2.08, par_tbse=11.03, delta_par=None, car_ibt=6.07, car_tbse=9.73,
                   delta_car=None),
        GeneralRow(metric="D9", par_ibt=37.01, par_tbse=102.79, delta_par=None, car_ibt=64.50, car_tbse=119.81,
                   delta_car=None),
        GeneralRow(metric="Variance", par_ibt=202.0810, par_tbse=1181.3969, delta_par=None, car_ibt=576.8663,
                   car_tbse=1688.4959, delta_car=None),
        GeneralRow(metric="Standard dev.", par_ibt=14.22, par_tbse=34.37, delta_par=None, car_ibt=24.02, car_tbse=41.09,
                   delta_car=None),
        GeneralRow(metric="Coeff of Variation", par_ibt=0.804, par_tbse=0.645, delta_par=None, car_ibt=0.728,
                   car_tbse=0.683, delta_car=None),
        GeneralRow(metric="MAPE", par_ibt=11.25, par_tbse=30.19, delta_par=None, car_ibt=19.26, car_tbse=35.64,
                   delta_car=None),
    ]


@affordability_router.get("/{simulation_id}/groups/general", response_model=List[GeneralGroupRow])
async def get_groups_general(simulation_id):
    general_group_data = [
        GeneralGroupRow(metric="Mean", par_ibt_g1=0.6, par_ibt_g2=1.7, par_tbse_g1=2.0, par_tbse_g2=4.6,
                        car_ibt_g1=1.8, car_ibt_g2=3.3, car_tbse_g1=2.8, car_tbse_g2=5.59),
        GeneralGroupRow(metric="Median", par_ibt_g1=0.4, par_ibt_g2=1.2, par_tbse_g1=1.2, par_tbse_g2=3.0,
                        car_ibt_g1=1.4, car_ibt_g2=2.6, car_tbse_g1=1.9, car_tbse_g2=3.82),
        GeneralGroupRow(metric="Min", par_ibt_g1=0.0, par_ibt_g2=0.1, par_tbse_g1=0.1, par_tbse_g2=0.2,
                        car_ibt_g1=0.3, car_ibt_g2=0.3, car_tbse_g1=0.3, car_tbse_g2=0.3),
        GeneralGroupRow(metric="Max", par_ibt_g1=3.8, par_ibt_g2=10.9, par_tbse_g1=9.9, par_tbse_g2=21.9,
                        car_ibt_g1=8.6, car_ibt_g2=12.6, car_tbse_g1=12.8, car_tbse_g2=23.6),
        GeneralGroupRow(metric="Q1", par_ibt_g1=0.2, par_ibt_g2=0.6, par_tbse_g1=0.6, par_tbse_g2=1.7,
                        car_ibt_g1=0.7, car_ibt_g2=1.5, car_tbse_g1=1.0, car_tbse_g2=2.4),
        GeneralGroupRow(metric="Q3", par_ibt_g1=0.8, par_ibt_g2=2.3, par_tbse_g1=2.3, par_tbse_g2=6.3,
                        car_ibt_g1=2.5, car_ibt_g2=4.5, car_tbse_g1=3.5, car_tbse_g2=7.6),
        GeneralGroupRow(metric="D1", par_ibt_g1=0.1, par_ibt_g2=0.3, par_tbse_g1=0.4, par_tbse_g2=0.9,
                        car_ibt_g1=0.5, car_ibt_g2=1.0, car_tbse_g1=0.7, car_tbse_g2=1.3),
        GeneralGroupRow(metric="D9", par_ibt_g1=1.5, par_ibt_g2=4.2, par_tbse_g1=4.7, par_tbse_g2=10.8,
                        car_ibt_g1=3.9, car_ibt_g2=6.3, car_tbse_g1=6.3, car_tbse_g2=12.3),
        GeneralGroupRow(metric="F (Moyenne)", par_ibt_g1=65.5, par_ibt_g2=65.4, par_tbse_g1=65.9, par_tbse_g2=67.7,
                        car_ibt_g1=62.0, car_ibt_g2=61.0, car_tbse_g1=48.3, car_tbse_g2=65.0),
        GeneralGroupRow(metric="Variance", par_ibt_g1=0.47, par_ibt_g2=2.92, par_tbse_g1=4.16, par_tbse_g2=18.86,
                        car_ibt_g1=2.18, car_ibt_g2=5.52, car_tbse_g1=6.43, car_tbse_g2=22.50),
        GeneralGroupRow(metric="Standard deviation", par_ibt_g1=0.7, par_ibt_g2=1.7, par_tbse_g1=2.0, par_tbse_g2=4.3,
                        car_ibt_g1=1.48, car_ibt_g2=2.35, car_tbse_g1=2.54, car_tbse_g2=4.7),
        GeneralGroupRow(metric="MAPE", par_ibt_g1=0.5, par_ibt_g2=1.2, par_tbse_g1=1.5, par_tbse_g2=3.2,
                        car_ibt_g1=1.1, car_ibt_g2=1.8, car_tbse_g1=1.9, car_tbse_g2=3.6),
        GeneralGroupRow(metric="Coeff of Variation", par_ibt_g1=1.091, par_ibt_g2=0.991, par_tbse_g1=0.991,
                        par_tbse_g2=1.038,
                        car_ibt_g1=0.804, car_ibt_g2=0.714, car_tbse_g1=0.906, car_tbse_g2=0.849),
        GeneralGroupRow(metric="Interquartile range", par_ibt_g1=0.6, par_ibt_g2=1.8, par_tbse_g1=1.7, par_tbse_g2=4.6,
                        car_ibt_g1=1.7, car_ibt_g2=3.0, car_tbse_g1=2.5, car_tbse_g2=5.2),
        GeneralGroupRow(metric="Interdecile range", par_ibt_g1=1.3, par_ibt_g2=3.9, par_tbse_g1=4.3, par_tbse_g2=9.9,
                        car_ibt_g1=3.4, car_ibt_g2=5.3, car_tbse_g1=5.7, car_tbse_g2=11.0),
        GeneralGroupRow(metric="Yule coefficient", par_ibt_g1=0.38, par_ibt_g2=0.32, par_tbse_g1=0.29, par_tbse_g2=0.42,
                        car_ibt_g1=0.20, car_ibt_g2=0.26, car_tbse_g1=0.31, car_tbse_g2=0.44)
    ]
    return general_group_data


@affordability_router.get("/{simulation_id}/groups/headcount_ratio", response_model=List[HeadcountBreakdownRow])
async def get_groups_headcount_ratio(simulation_id):
    data: list[HeadcountBreakdownRow] = [
        HeadcountBreakdownRow(
            group="EP",
            f_i=54.1,
            par_ibt_households=1.2,
            par_ibt_individuals=1.8,
            par_ibt_children=1.8,
            par_tbse_households=18.1,
            par_tbse_individuals=19.0,
            par_tbse_children=20.9,
            delta_households=-16.9,
            delta_individuals=-17.2,
            delta_children=-19.1,
        ),
        HeadcountBreakdownRow(
            group="EPA",
            f_i=45.9,
            par_ibt_households=15.7,
            par_ibt_individuals=15.8,
            par_ibt_children=19.2,
            par_tbse_households=50.0,
            par_tbse_individuals=46.6,
            par_tbse_children=51.3,
            delta_households=-34.3,
            delta_individuals=-30.8,
            delta_children=-32.1,
        ),
        HeadcountBreakdownRow(
            group="Total",
            f_i=100.0,
            par_ibt_households=7.9,
            par_ibt_individuals=7.9,
            par_ibt_children=9.9,
            par_tbse_households=32.8,
            par_tbse_individuals=31.6,
            par_tbse_children=35.1,
            delta_households=-24.9,
            delta_individuals=-23.8,
            delta_children=-25.2,
        )
    ]
    return data


@affordability_router.get("/{simulation_id}/groups/apparent_deficit", response_model=List[
    ApparentDeficitRow])
async def get_groups_apparent_affordability_deficit(simulation_id):
    rows = [
        ApparentDeficitRow(
            group="EP",
            f_i_menages=54.1,
            mean_par_ibt=0.06,
            variance_par_ibt=0.3437,
            corr_coef_group_1="Between",
            corr_coef_value_1=2.0827,
            f_i_par_tbse=54.1,
            mean_par_tbse=4.50,
            variance_par_tbse=126.2414,
            corr_coef_group_2="Between",
            corr_coef_value_2=198.3668
        ),
        ApparentDeficitRow(
            group="EPA",
            f_i_menages=45.9,
            mean_par_ibt=2.96,
            variance_par_ibt=79.0985,
            corr_coef_group_1="Within",
            corr_coef_value_1=36.4540,
            f_i_par_tbse=45.9,
            mean_par_tbse=32.77,
            variance_par_tbse=1628.1573,
            corr_coef_group_2="Within",
            corr_coef_value_2=814.8928
        ),
        ApparentDeficitRow(
            group="Total",
            f_i_menages=100.0,
            mean_par_ibt=1.39,
            variance_par_ibt=38.5366,
            corr_coef_group_1="Corr. Coeff",
            corr_coef_value_1=5.4,
            f_i_par_tbse=100.0,
            mean_par_tbse=17.47,
            variance_par_tbse=1013.2596,
            corr_coef_group_2="Corr. Coeff",
            corr_coef_value_2=19.6
        )
    ]
    return rows


@affordability_router.get("/{simulation_id}/groups/effective_deficit", response_model=List[
    ApparentDeficitRow])
async def get_groups_effective_affordability_deficit(simulation_id):
    rows = [
        ApparentDeficitRow(
            group="EP",
            f_i_menages=8.3,
            mean_par_ibt=5.14,
            variance_par_ibt=2.3430,
            corr_coef_group_1="Between",
            corr_coef_value_1=14.3157,
            f_i_par_tbse=30.0,
            mean_par_tbse=24.83,
            variance_par_tbse=191.2013,
            corr_coef_group_2="Between",
            corr_coef_value_2=348.1182
        ),
        ApparentDeficitRow(
            group="EPA",
            f_i_menages=91.7,
            mean_par_ibt=18.83,
            variance_par_ibt=204.6219,
            corr_coef_group_1="Within",
            corr_coef_value_1=187.7653,
            f_i_par_tbse=70.0,
            mean_par_tbse=65.54,
            variance_par_tbse=1108.4547,
            corr_coef_group_2="Within",
            corr_coef_value_2=833.2787
        ),
        ApparentDeficitRow(
            group="Total",
            f_i_menages=100.0,
            mean_par_ibt=17.69,
            variance_par_ibt=202.0810,
            corr_coef_group_1="Corr. Coeff",
            corr_coef_value_1=7.1,
            f_i_par_tbse=100.0,
            mean_par_tbse=53.33,
            variance_par_tbse=1181.3969,
            corr_coef_group_2="Corr. Coeff",
            corr_coef_value_2=29.5
        )
    ]
    return rows


@affordability_router.get("/{simulation_id}/groups/gini_par", response_model=Dict[str, GiniPARResult])
async def get_gini_par(simulation_id):
    return {
        "ibt": GiniPARResult(components=[
            GiniComponent(name="Between", value=51.7, percentage=54.1),
            GiniComponent(name="Within", value=42.0, percentage=43.9),
            GiniComponent(name="Transvariat.", value=1.9, percentage=2.0),
            GiniComponent(name="Total Population", value=95.6, percentage=100.0),
        ]),
        "tbse":
            GiniPARResult(components=[
                GiniComponent(name="Between", value=40.2, percentage=50.7),
                GiniComponent(name="Within", value=32.1, percentage=40.5),
                GiniComponent(name="Transvariat.", value=7.0, percentage=8.8),
                GiniComponent(name="Total Pop", value=79.3, percentage=100.0),
            ])
    }


@affordability_router.get("/{simulation_id}/groups/gini_index_matrix",
                          response_model=Dict[
                              Literal["ibt", "tbse"], Dict[Literal["g1", "g2"], Dict[Literal["g1", "g2"], float]]])
async def get_gini_index(simulation_id):
    return {"ibt": {
        "g1": {
            "g1": 0.0,
            "g2": 0.0,
        },
        "g2": {
            "g1": 0.0,
            "g2": 0.0,
        }
    },
        "tbse": {
            "g1": {
                "g1": 0.0,
                "g2": 0.0,
            },
            "g2": {
                "g1": 0.0,
                "g2": 0.0,
            }
        }

    }


@affordability_router.get("/{simulation_id}/groups/weight_matrix",
                          response_model=Dict[Literal["ibt", "tbse"], WeightMatrix])
async def get_gini_index_by_group(simulation_id):
    return {"ibt": WeightMatrix(rows=[
        WeightMatrixRow(group="G1", fj=54.1, aj=2.4, wij=0.013, final_weight=0.539),
        WeightMatrixRow(group="G2", fj=45.9, aj=97.6, wij=0.539, final_weight=0.447),
        WeightMatrixRow(group="Total", fj=100.0, aj=100.0, wij=None, final_weight=None)
    ]), "tbse": WeightMatrix(rows=[
        WeightMatrixRow(group="G1", fj=54.1, aj=2.4, wij=0.013, final_weight=0.539),
        WeightMatrixRow(group="G2", fj=45.9, aj=97.6, wij=0.539, final_weight=0.447),
        WeightMatrixRow(group="Total", fj=100.0, aj=100.0, wij=None, final_weight=None)
    ])
    }


@affordability_router.get("/{simulation_id}/groups/contribution_matrix",
                          response_model=Dict[Literal["g1", "g2"], Dict[Literal["g1", "g2"], float]])
async def get_contribution_matrix(simulation_id):
    return {"ibt": {
        "g1": {
            "g1": 0.0,
            "g2": 0.0,
        },
        "g2": {
            "g1": 0.0,
            "g2": 0.0,
        }
    },
        "tbse": {
            "g1": {
                "g1": 0.0,
                "g2": 0.0,
            },
            "g2": {
                "g1": 0.0,
                "g2": 0.0,
            }
        }

    }
