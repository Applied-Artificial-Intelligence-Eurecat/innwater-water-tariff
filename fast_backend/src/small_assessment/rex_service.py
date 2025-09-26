import pandas as pd

from src.small_assessment.calculator_service import SimulationCalculator
from src.initial.schemas import *

def calculate_net_cost_service(num_subscribers: int, charge_fix: float, social_sampling_rate: float,
                               total_group_subscription_fee: float,
                               only_subscription_fee: float, potential_consumption_base: float,
                               taxation_group_fees: float, fixed_costs: float):
    produit_per_abonne = 4 * (total_group_subscription_fee - only_subscription_fee) / social_sampling_rate
    r_variable = num_subscribers * produit_per_abonne
    r_fixes = num_subscribers * charge_fix * 4
    total_produit = r_fixes + r_variable
    social_sampling_rate_coef = num_subscribers / social_sampling_rate
    level_of_service = 4 * (social_sampling_rate_coef * potential_consumption_base)
    variable_costs = level_of_service * taxation_group_fees
    total_charges = variable_costs + fixed_costs
    net_sanitation = total_produit - total_charges
    return net_sanitation, total_charges


def create_mock_simulation():
    return SimulationPayload(
        primitives=PrimitivesModel(
            ep=WaterServiceCostModel(
                couts_fixes=9000000,
                couts_variables=0.9,
                nombre_abonnes=47847,
            ),
            assainissement=WaterServiceCostModel(
                couts_fixes=6000000,
                couts_variables=0.40,
                nombre_abonnes=25300,
            ),
            environnement=EnvironmentalModel(
                couts_fixes_par_an=0,
                couts_variable_moyen=1.3,
            ),
            fiscalite=TaxSectionModel(
                eau_potable=TaxModel(
                    tva=2.1,
                    redevances=0.12,
                ),
                assainissement=TaxModel(
                    tva=10,
                    redevances=0.04,
                )
            ),
            donnees_sociales=SocialDataModel(
                seuil_par=3,
                seuil_car=3,
                pauvrete=800,
            )
        ),
        population=PopulationModel(
            bd="BD",
            eps=458,
            std=0.05,
        ),
        tarification=TariffModel(
            ep=TariffSectionModel(
                abonnement=18.69,
                usage_tiers=[
                    ConsumptionThresholds(
                        seuil=0,
                        prix=0.878
                    ),
                    ConsumptionThresholds(
                        seuil=15,
                        prix=1.839
                    ),
                    ConsumptionThresholds(
                        seuil=30,
                        prix=2.768
                    ),
                    ConsumptionThresholds(
                        seuil=60,
                        prix=4.38
                    )
                ]
            ),
            assainissement=TariffSectionModel(
                abonnement=15.545,
                usage_tiers=[
                    ConsumptionThresholds(
                        seuil=0,
                        prix=1.3,
                    ),
                    ConsumptionThresholds(
                        seuil=15,
                        prix=2.12,
                    ),
                    ConsumptionThresholds(
                        seuil=30,
                        prix=2.21,
                    ),
                    ConsumptionThresholds(
                        seuil=60,
                        prix=2.5,
                    )
                ]
            )
        ),
        demande=DemandModel(
            coefficients=CoefficientModel(
                a0=-2.56,
                a1=0.48,
                a2=0.44,
                a3=0.12,
                a4=0.37,
                a5=-0.31,
                a6=0.25
            ),
            k=0.4,
            piscine=False,
            jardin=False
        ),
        launch=LaunchModel(
            periodes=4,
            nom_simulation="MockSimulation"
        )
    )


if __name__ == '__main__':
    from src.initial.schemas import *

    # PPrimitives

    simulation_payload: SimulationPayload = create_mock_simulation()

    unit_variable_cost = 0.40

    # Tariff module
    sanitation_charge_fix = 15.545

    # Generation dataset

    df = pd.read_csv('/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/fast_backend/data/data.csv', index_col=0)
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    simulation_calculator = SimulationCalculator(simulation_payload, g1_df, g2_df)
    # Social Data J17 J18
    print(len(g1_df) + len(g2_df))

    all_df = pd.concat([g1_df, g2_df])
    print(all_df.columns)
    total_subscription_yearly_fee = (
            all_df['Assainissement Collectif (1 = oui)'] * simulation_payload.tariff.sanitation.subscription).sum()
    print("total_sanitation_subscription_fee", total_subscription_yearly_fee)
    print("total_sanitation_subscription_fee", simulation_calculator.base_sanitation_subscription_fee)
    social_sampling_rate = len(g2_df)

    facture_ibt_c_bcp = simulation_calculator.total_tariff_sanitation_subscription_fee()

    c_ep_bcp_hy_481 = 6780
    print("HY", simulation_calculator.df['C_EP_BCP HY'].sum())

    net_sanitation, _  = calculate_net_cost_service(simulation_payload.primitives.sanitation.number_of_subscribers,
                                                simulation_payload.tariff.sanitation.subscription,
                                                    social_sampling_rate,
                                                total_subscription_yearly_fee,
                                                simulation_calculator.total_tariff_sanitation_subscription_fee(),
                                                simulation_calculator.only_subscription_tariff_sanitation_subscription_fee(),
                                                simulation_payload.primitives.sanitation.variable_costs,
                                                simulation_payload.primitives.sanitation.fixed_costs)
    from math import isclose

    assert isclose(net_sanitation, -9271037.519950997)

    net_potable_water, _ = calculate_net_cost_service(simulation_payload.primitives.drinking_water.number_of_subscribers,
                                                   simulation_payload.tariff.drinking_water.subscription,
                                                   len(simulation_calculator.df),
                                                   simulation_calculator.total_tariff_potable_water_subscription_fee(),
                                                   simulation_calculator.only_subscription_tariff_potable_water_subscription_fee(),
                                                   simulation_calculator.only_tariff_drinking_water_subscription_fee(),
                                                   simulation_payload.primitives.drinking_water.variable_costs,
                                                   simulation_payload.primitives.drinking_water.fixed_costs)
    assert isclose(net_potable_water, 2493994.6051737517)
