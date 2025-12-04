import time

import pandas as pd

from src.results.routers import calculate_rex
from src.small_assessment.effeco.gini_decomp import gini_decomp
from src.small_assessment.mock_simulation import PAYLOAD
from src.small_assessment.new_calculator_service import NewSimulation


def main():
    df = pd.read_csv(
        '/Users/oriol.alas/PROJECTS/INNWATER/innwater-water-tariff/fast_backend/data/data.csv',
        index_col=0
    )
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_df = df[is_g1]
    g2_df = df[~is_g1]
    start = time.time()
    simulation = NewSimulation(PAYLOAD, g1_df, g2_df)

    res = calculate_rex(simulation)
    print(res)

    print(gini_decomp(simulation.par_ibt, simulation.is_sanitation())['gini_decomp'])


if __name__ == '__main__':
    main()
