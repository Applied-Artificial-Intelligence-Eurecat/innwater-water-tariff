import pandas as pd

from src.initial.schemas import *
from src.small_assessment.rex_service import create_mock_simulation, SimulationCalculator

if __name__ == '__main__':
    simulation_payload: SimulationPayload = create_mock_simulation()
    df = pd.read_csv('/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/data.csv', index_col=0)
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    simulation_calculator = SimulationCalculator(simulation_payload, g1_df, g2_df)
    simulation_calculator.partie_base_c_et_fact()
    simulation_calculator.var_par_menages()
    print(simulation_calculator.tariff_sanitation_subscription_fee())