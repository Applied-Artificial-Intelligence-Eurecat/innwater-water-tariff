import io

import pandas as pd
from matplotlib import pyplot as plt

from src.core.models import Simulation


async def mock_data(title: str):
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 20, 30, 40, 50]
    # Create the plot
    fig, axs = plt.subplots(1, 1, figsize=(10, 6))
    axs.scatter(x_values, y_values)
    # Add titles and labels
    axs.set_title(title)
    axs.set_xlabel("Years")
    axs.set_ylabel("Population")
    # Add grid for better readability
    axs.grid(True, linestyle='--', alpha=0.7)
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


async def generate_tbse_par_affordability_plot(simulation: Simulation) -> io.BytesIO:
    import pandas as pd
    import matplotlib.pyplot as plt

    fichier_excel = "data/NIVEAUVIEPARTBSE.xls"
    df = pd.read_excel(fichier_excel)
    df.columns = df.columns.str.strip()  # Nettoyer les noms de colonnes

    if 'Niveau de Vie OCDE' not in df.columns or 'Par TBSE' not in df.columns:
        raise ValueError("Les colonnes 'Niveau de Vie OCDE' et 'Par TBSE' sont manquantes dans le fichier Excel.")

    df['Niveau de Vie OCDE'] = pd.to_numeric(df['Niveau de Vie OCDE'], errors='coerce')
    df['Par TBSE'] = pd.to_numeric(df['Par TBSE'], errors='coerce')
    df.fillna(0, inplace=True)

    x = df['Niveau de Vie OCDE'].tolist()
    y = df['Par TBSE'].tolist()

    fig = plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', alpha=0.7)
    plt.title('Scatter Plot : Niveau de Vie OCDE vs Par TBSE')
    plt.xlabel('Niveau de Vie OCDE')
    plt.ylabel('Par TBSE')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


async def generate_tbse_consumption_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("TBSE Consumption Plot")


async def generate_pens_parade_consumptions_plot(simulation: Simulation) -> io.BytesIO:
    FILE_PATH_BASE = 'data/CBASE_PEN_P.xls'
    FILE_PATH_CAPTIVE = 'data/CCaptive_PEN_P.xls'

    df_base = pd.read_excel(FILE_PATH_BASE, decimal=',')
    df_captive = pd.read_excel(FILE_PATH_CAPTIVE, decimal=',')

    # Vérifier la présence des colonnes requises
    required_columns_base = ['Ménage', 'C Base', 'Rang normalisé']
    required_columns_captive = ['Ménage', 'C Captive', 'Rang normalisé']

    if not all(col in df_base.columns for col in required_columns_base):
        raise ValueError(f"Colonnes manquantes dans {FILE_PATH_BASE}")

    if not all(col in df_captive.columns for col in required_columns_captive):
        raise ValueError(f"Colonnes manquantes dans {FILE_PATH_CAPTIVE}")

    # Préparer les données
    x_base = df_base['Rang normalisé']
    y_base = df_base['C Base']

    x_captive = df_captive['Rang normalisé']
    y_captive = df_captive['C Captive']

    # Afficher le graphique Pen’s Parade
    fig = plt.figure(figsize=(12, 6))
    plt.plot(x_base, y_base, label='Consommation Base', color='blue')
    plt.plot(x_captive, y_captive, label='Consommation Captive', color='red')
    plt.title("Pen's Parade : Consommation Base vs Captive")
    plt.xlabel('Rang normalisé')
    plt.ylabel('Consommation')
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


async def generate_consumption_deviation_losses_cost_recovery_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("Consumption Deviation Losses Cost Recovery Plot")
