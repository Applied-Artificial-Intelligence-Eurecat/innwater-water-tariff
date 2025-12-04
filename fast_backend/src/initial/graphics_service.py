import io
from typing import Literal, Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.initial.schemas import SimulationPayload
from src.small_assessment.calculator_service import SimulationFinished
from src.small_assessment.new_calculator_service import NewSimulation


def generate_par_affordability_plot(simulation: SimulationPayload, level_oecd, par_col: Iterable[float],
                                    feat='TBSE') -> io.BytesIO:
    fig = par_affordability_figure(level_oecd, simulation, par_col=par_col, feat=feat)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def par_affordability_figure(level_oecd, simulation: SimulationPayload,
                             par_col: Iterable[float],
                             feat='TBSE'):
    oecd = pd.to_numeric(level_oecd, errors='coerce')
    par_tbse = pd.to_numeric(par_col, errors='coerce')
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


def generate_consumption_plot(level_oecd, consumption,
                              feat: Literal['TBSE', 'IBT']) -> io.BytesIO:
    fig = plt.figure(figsize=(10, 6))
    model = LinearRegression()

    # Pasar a numpy y aplanar
    consumption = np.asarray(consumption, dtype=float).ravel()  # (N,)
    level_oecd = np.asarray(level_oecd, dtype=float).ravel()  # (N,)

    # Máscara de NaNs (si quieres, puedes usar isfinite para quitar inf también)
    mask = ~np.isnan(consumption)
    consumption = consumption[mask]  # (K,)
    level_oecd = level_oecd[mask]  # (K,)

    # Asegurar shapes correctas para sklearn
    X = level_oecd.reshape(-1, 1)  # (K, 1)
    y = consumption  # (K,)

    print("SHAPE", mask.shape, y.shape, X.shape)

    # Fit del modelo
    model.fit(X, y)
    y_pred = model.predict(X)
    score = r2_score(y, y_pred)

    # Plot
    plt.scatter(level_oecd, consumption)
    plt.plot(level_oecd, y_pred, linestyle='dashed')

    # model.coef_ es (1,1); lo aplanamos
    coef = float(model.coef_.ravel()[0])
    intercept = float(model.intercept_)

    plt.text(plt.xlim()[1] * 0.7, plt.ylim()[1] * 0.80,
             f"y = {coef:.2f}x + {intercept:.2f}\nR2 = {score:.2f}")

    plt.xlabel('Level OECD')
    plt.ylabel(f'Consommation {feat} (m3/trim)')
    plt.title(f'Linear Regression : Level of Life OECD vs Consommation {feat}')
    plt.grid(True, alpha=0.75, linestyle='--')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_tbse_pens_parade_consumptions_plot(calculator: NewSimulation) -> io.BytesIO:
    fig = plt.figure(figsize=(12, 6))
    df = calculator.df
    xs = np.array(list(range(len(df))))
    xs = xs / len(df)

    df['Base Consumption'] = calculator.base_consumption_per_trim
    df['Captive Consumption'] = calculator.captive_consumption_per_trim

    plt.plot(xs, df['Base Consumption'].sort_values(), label='Pen\'s Parade of Base Consumption', color='orange')
    plt.plot(xs, df['Captive Consumption'].sort_values(), label='Pen\'s Parade of Captive Consumption',
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


def generate_ibt_pens_parade_consumptions_plot(calculator: NewSimulation) -> io.BytesIO:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    df = calculator.df
    xs = np.array(range(len(df)))
    xs = xs / len(df)

    df['Base Consumption'] = calculator.base_consumption_per_trim

    # Left axis → Pen's Parade
    y1 = df['Base Consumption'].sort_values()
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


def generate_tbse_consumption_deviation_losses_cost_recovery_plot(calculator: NewSimulation,
                                                                  consumption,
                                                                  feat: Literal['TBSE', 'IBT']) -> io.BytesIO:
    g1_consumption = consumption[calculator.is_sanitation() == False]
    g2_consumption = consumption[calculator.is_sanitation()]
    g1_poor_consumption = consumption[(calculator.is_poor) & (calculator.is_sanitation() == False)].mean()
    g2_poor_consumption = consumption[(calculator.is_poor) & (calculator.is_sanitation())].mean()
    g1_non_poor_consumption = consumption[(~calculator.is_poor) & (calculator.is_sanitation() == False)].mean()
    g2_non_poor_consumption = consumption[(~calculator.is_poor) & (calculator.is_sanitation())].mean()

    g1_uvc = max(
        calculator.simulation.primitives.environment.average_variable_cost - calculator.simulation.primitives.taxation.drinking_water.fees,
        0)
    g2_uvc = max(
        g1_uvc - calculator.simulation.primitives.taxation.sanitation.fees - calculator.simulation.primitives.sanitation.variable_costs,
        0)

    # --- Cost ambiental no recuperat per grup ---
    g1_ec_fixed = g1_consumption * g1_uvc
    g2_ec_fixed = g2_consumption * g2_uvc
    total_ec_fixed = (g1_ec_fixed.sum() + g2_ec_fixed.sum()) / len(consumption)

    poor_g1_ec = g1_poor_consumption * g1_uvc
    poor_g2_ec = (g2_poor_consumption) * g2_uvc
    non_poor_g1_ec = (g1_non_poor_consumption) * g1_uvc
    non_poor_g2_ec = (g2_non_poor_consumption) * g2_uvc

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
    plt.grid(alpha=0.2)
    # Llegenda a dalt a l'esquerra, en una fila
    plt.show()
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf
