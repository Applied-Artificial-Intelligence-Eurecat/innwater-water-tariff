import io
from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import BaseModel


class PopulationPlotModel(BaseModel):
    total_subscribers: int
    sanitation_subscribers: int
    bd: str
    eps: int
    std: float
    random_seed: int = 42


DATA = {
    "Reunion 2010": "data/data.csv"
}


def generate_and_create_population_plot(total_subscribers: int, sanitation_subscribers: int, bd: str, eps: int,
                                        std: float, random_seed: int = 42) -> io.BytesIO:
    xls_path = DATA[bd]
    df = pd.read_csv(Path(xls_path))

    g1_augmented, g2_augmented = generate_population_sample_dfs(bd, total_subscribers, sanitation_subscribers,
                                                                eps,
                                                                std)

    buf = create_population_plot(df, g1_augmented, g2_augmented)
    return buf


def create_population_plot(df, g1_augmented, g2_augmented):
    fig, axs = plt.subplots(1, 2, figsize=(8, 4))
    axs[0].hist(g1_augmented['Revenu_Imputé_2'], bins=50, alpha=0.6, range=(0, df['Revenu_Imputé_2'].max()),
                label='Only Potable Water (G1)', )
    axs[1].hist(g2_augmented['Revenu_Imputé_2'], bins=50, alpha=0.6, range=(0, df['Revenu_Imputé_2'].max()),
                label='Sanitation and Potable Water (G2)', )
    axs[0].set_xlabel("Income")
    axs[1].set_xlabel("Income")
    axs[0].set_ylabel("Number of cases")
    plt.suptitle("Distribution Comparison of Income from households by different groups")
    axs[0].set_title("Only Potable Water (G1)")
    axs[1].set_title("Sanitation and Potable Water (G2)")
    axs[0].grid(True, alpha=0.75, linestyle='--')
    axs[1].grid(True, alpha=0.75, linestyle='--')
    max_ylim = max(axs[0].get_ylim()[1], axs[1].get_ylim()[1])
    axs[0].set_ylim(0, max_ylim)
    axs[1].set_ylim(0, max_ylim)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_original_df(bd: str):
    xls_path = DATA[bd]
    df = pd.read_csv(Path(xls_path))
    df['Garden * Wheather'] = df['jardin (1 = oui)'] * df["Freq Nombre de Jours sans pluie"]
    return df


def generate_population_sample_dfs(bd: str, total_subscribers: int, sanitation_subscribers: int, eps: int,
                                   std: float):
    xls_path = DATA[bd]
    df = pd.read_csv(Path(xls_path))
    g1_augmented, g2_augmented = process_population_sample_df(df, total_subscribers, sanitation_subscribers, eps,
                                                              std, )
    return g1_augmented, g2_augmented


def process_population_sample_df(df, total_subscribers, sanitation_subscribers, eps, std, ):
    np.random.seed(42)
    df['Garden * Wheather'] = df['jardin (1 = oui)'] * df["Freq Nombre de Jours sans pluie"]
    is_g1 = df['Assainissement Collectif (1 = oui)'] == 0
    g1_perc = sanitation_subscribers / total_subscribers
    g1_card = int(eps * g1_perc)
    g2_card = int(eps - g1_card)

    g1_augmented = pd.concat([df[is_g1]] * ceil(g1_card / len(df[is_g1]))).sample(g1_card)
    g2_augmented = pd.concat([df[~is_g1]] * ceil(g2_card / len(df[~is_g1]))).sample(g2_card)
    g1_augmented['Revenu_Imputé_2'] = g1_augmented[('Revenu_Imputé_2')] * (1 + np.random.normal(0, std, g1_card))
    g2_augmented['Revenu_Imputé_2'] = g2_augmented[('Revenu_Imputé_2')] * (1 + np.random.normal(0, std, g2_card))

    return g1_augmented, g2_augmented


async def save_population_data_given_simulation_info(bd: str, total_subscribers: int, sanitation_subscribers: int,
                                                     eps: int,
                                                     std: float, use_original_datasource: bool, simulation_id: int):
    Path(f'data/simulation_data/{simulation_id}').mkdir(parents=True, exist_ok=True)
    if not use_original_datasource:
        g1_df, g2_df = generate_population_sample_dfs(bd, total_subscribers, sanitation_subscribers, eps, std)
        concat_df = pd.concat([g1_df, g2_df])
    else:
        concat_df = generate_original_df(bd)

    concat_df.to_csv(f'data/simulation_data/{simulation_id}/sample.csv', index=False)
