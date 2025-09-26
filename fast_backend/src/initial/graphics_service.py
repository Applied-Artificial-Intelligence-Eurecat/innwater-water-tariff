import io
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.initial.schemas import SimulationPayload
from src.small_assessment.calculator_service import SimulationFinished


def generate_par_affordability_plot(simulation: SimulationPayload, df, par_col: Literal[
    'VAR_PAR_Menages AM', 'VAR_PAR_Menages AL'] = 'VAR_PAR_Menages AL', feat='TBSE') -> io.BytesIO:
    fig = par_affordability_figure(df, simulation, par_col=par_col, feat=feat)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def par_affordability_figure(df, simulation: SimulationPayload,
                             par_col: Literal['VAR_PAR_Menages AM', 'VAR_PAR_Menages AL'] = 'VAR_PAR_Menages AL',
                             feat='TBSE'):
    oecd = pd.to_numeric(df['Level OECD'], errors='coerce')
    par_tbse = pd.to_numeric(df[par_col], errors='coerce')
    df.fillna(0, inplace=True)
    x = oecd.tolist()
    y = par_tbse.tolist()
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', alpha=0.7)
    plt.title(f'Scatter Plot : Level of Life OECD vs Par {feat}')
    plt.xlabel('Level OECD')
    plt.ylabel(f'Par {feat}')
    plt.xlim(*plt.xlim())
    plt.ylim(*plt.ylim())
    plt.hlines(y=simulation.primitives.social_data.threshold_par, xmin=plt.xlim()[0], xmax=plt.xlim()[1],
               label=f'Par {feat} Threshold', color='green')
    plt.vlines(x=simulation.primitives.social_data.poverty, ymin=plt.ylim()[0], ymax=plt.ylim()[1],
               label="Poverty threshold", color='red')
    plt.legend()
    plt.grid(True)
    return fig


def generate_consumption_plot(df: pd.DataFrame, col: Literal['C_et_F_TBSE P', 'C_EP_BCP HM'],
                              feat: Literal['TBSE', 'IBT']) -> io.BytesIO:
    fig = plt.figure(figsize=(10, 6))
    model = LinearRegression()
    model.fit(df[['Level OECD']], df[col])
    y_pred = model.predict(df[['Level OECD']])
    score = r2_score(df[["Level OECD"]], df[[col]])

    plt.scatter(df['Level OECD'], df[col])
    plt.plot(df['Level OECD'], y_pred, color='blue', linestyle='dashed')
    plt.text(plt.xlim()[1] * 0.7, plt.ylim()[1] * 0.80,
             f"y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}\nR2 = {score:.2f}", )
    plt.xlabel('Level OECD')
    plt.ylabel(f'Consommation {feat} (m3/trim)')
    plt.title(f'Linear Regression : Level of Life OECD vs Consommation {feat}')
    plt.grid(True, alpha=0.75, linestyle='--')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_tbse_pens_parade_consumptions_plot(df: pd.DataFrame) -> io.BytesIO:
    fig = plt.figure(figsize=(12, 6))
    xs = np.array(list(range(len(df))))
    xs = xs / len(df)
    plt.plot(xs, df['Partie_Base_C_et_Fact Q'].sort_values(), label='Pen\'s Parade of Base Consumption', color='orange')
    plt.plot(xs, df['Partie Captive C et Fact R'].sort_values(), label='Pen\'s Parade of Captive Consumption',
             color='blue')
    plt.title("TBSE Pen's Parade : Consommation Base vs Captive")
    plt.xlabel('Normalized Rank')
    plt.ylabel('Consumption')
    plt.legend()
    plt.grid(True)
    plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_ibt_pens_parade_consumptions_plot(df: pd.DataFrame) -> io.BytesIO:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    xs = np.array(range(len(df)))
    xs = xs / len(df)

    # Left axis → Pen's Parade
    y1 = df['Partie_Base_C_et_Fact Q'].sort_values()
    ax1.plot(xs, y1, label="Pen's Parade of Base Consumption", color='orange')
    ax1.set_xlabel('Normalized Rank')
    ax1.set_ylabel('Consumption (Base)', color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')

    ax2 = ax1.twinx()
    cumsum_basic_consumption = y1.cumsum()
    cumsum_basic_consumption = cumsum_basic_consumption / cumsum_basic_consumption.max() * 100
    ax2.plot(xs, cumsum_basic_consumption, label='Function for the distribution of the mass of basic consumptions',
             color='blue')
    ax2.set_ylabel('Cumulative % of Consumption', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    ax1.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_tbse_consumption_deviation_losses_cost_recovery_plot(simulation: SimulationFinished,
                                                                  consumption: Literal['C_et_F_TBSE P', 'C_EP_BCP HM'],
                                                                  feat: Literal['TBSE', 'IBT']) -> io.BytesIO:
    df = simulation.df
    g1_consumption = df.loc[df[simulation.is_sanitation] == 0, consumption]
    g2_consumption = df.loc[df[simulation.is_sanitation] == 1, consumption]
    g1_poor_consumption = df.loc[(df['poor'] == 1) & (df[simulation.is_sanitation]), consumption].mean()
    g2_poor_consumption = df.loc[(df['poor'] == 1) & (~df[simulation.is_sanitation]), consumption].mean()
    g1_non_poor_consumption = df.loc[(df['poor'] == 0) & (df[simulation.is_sanitation]), consumption].mean()
    g2_non_poor_consumption = df.loc[(df['poor'] == 0) & (~df[simulation.is_sanitation]), consumption].mean()

    g1_uvc = max(
        simulation.simulation.primitives.environment.average_variable_cost - simulation.simulation.primitives.taxation.drinking_water.fees,
        0)
    g2_uvc = max(
        g1_uvc - simulation.simulation.primitives.taxation.sanitation.fees - simulation.simulation.primitives.sanitation.variable_costs,
        0)

    # --- Cost ambiental no recuperat per grup ---
    g1_ec_fixed = g1_consumption * g1_uvc
    g2_ec_fixed = g2_consumption * g2_uvc
    total_ec_fixed = (g1_ec_fixed.sum() + g2_ec_fixed.sum()) / len(df)

    poor_g1_ec = g1_poor_consumption * g1_uvc
    poor_g2_ec = (g2_poor_consumption ) * g2_uvc
    non_poor_g1_ec = (g1_non_poor_consumption ) * g1_uvc
    non_poor_g2_ec = (g2_non_poor_consumption ) * g2_uvc

    labels = ["Ensemble", "Non Poor G2", "Non Poor G1", "Poor G2", "Poor G1"]
    values = np.array([
        total_ec_fixed,
        non_poor_g2_ec,
        non_poor_g1_ec,
        poor_g2_ec,
        poor_g1_ec,
    ], dtype=float)

    values = np.nan_to_num(values, nan=0.0)
    colors = {
        "Ensemble": "#6aaed6",  # blau suau
        "Non Poor G2": "#f5c04a",  # groc
        "Non Poor G1": "#b0b0b0",  # gris
        "Poor G2": "#e58a4a",  # taronja
        "Poor G1": "#4a76c9",  # blau
    }
    bar_colors = [colors.get(lbl, "#4472C4") for lbl in labels]

    fig, ax = plt.subplots(figsize=(12, 6))
    y = np.arange(len(labels))

    ax.barh(y, values, color=bar_colors)
    ax.set_xlim(left=0)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_title(f"Environmental cost recovery using {feat} consumption")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Llegenda a dalt a l'esquerra, en una fila
    plt.show()
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf