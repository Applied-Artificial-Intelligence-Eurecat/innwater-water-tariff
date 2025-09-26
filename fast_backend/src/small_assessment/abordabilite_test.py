import pandas as pd

from src.initial.graphics_service import generate_ibt_pens_parade_consumptions_plot, \
    generate_tbse_consumption_deviation_losses_cost_recovery_plot, generate_tbse_pens_parade_consumptions_plot
from src.initial.schemas import *
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.calculator_service import SimulationCalculator, SimulationFinished
from src.small_assessment.rex_service import create_mock_simulation

if __name__ == '__main__':
    simulation_payload: SimulationPayload = create_mock_simulation()
    df = pd.read_csv('/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/fast_backend/data/data.csv',
                     index_col=0)
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    simulation_calculator = SimulationCalculator(simulation_payload, g1_df, g2_df)
    # print(par_affordability_figure(simulation_calculator.df, simulation_calculator.simulation))
    # generate_consumption_plot(simulation_calculator.df, 'C_et_F_TBSE P', 'TBSE')
    simulation_calculator.save_simulation_data(4)
    finished = SimulationFinished(4, simulation_payload)
    print(affordability_general(finished.df))
    #generate_ibt_pens_parade_consumptions_plot(finished.df)
    #generate_tbse_pens_parade_consumptions_plot(finished.df)
    #generate_tbse_consumption_deviation_losses_cost_recovery_plot(finished, 'C_et_F_TBSE P', 'TBSE')
    #generate_tbse_consumption_deviation_losses_cost_recovery_plot(finished, 'C_EP_BCP HM', 'IBT')
