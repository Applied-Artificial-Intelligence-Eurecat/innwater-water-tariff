import pandas as pd
import matplotlib.pyplot as plt

# Chemins des fichiers
FILE_PATH_BASE = 'CBASE_PEN_P.xls'
FILE_PATH_CAPTIVE = 'CCaptive_PEN_P.xls'

# Lire les fichiers Excel
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
plt.figure(figsize=(12,6))
plt.plot(x_base, y_base, label='Consommation Base', color='blue')
plt.plot(x_captive, y_captive, label='Consommation Captive', color='red')
plt.title("Pen's Parade : Consommation Base vs Captive")
plt.xlabel('Rang normalisé')
plt.ylabel('Consommation')
plt.legend()
plt.grid(True)
plt.show()
