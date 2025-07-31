import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier Excel
fichier_excel = "CAR.xls"
df = pd.read_excel(fichier_excel)
df.columns = df.columns.str.strip()  # Nettoyer les noms de colonnes

# Vérifier la présence des colonnes nécessaires
if 'CAR TBSE' not in df.columns or 'Rang N' not in df.columns:
    raise ValueError("Les colonnes 'CAR TBSE' et 'Rang N' sont manquantes dans le fichier Excel.")

# Convertir les colonnes en numériques
df['CAR TBSE'] = pd.to_numeric(df['CAR TBSE'], errors='coerce')
df['Rang N'] = pd.to_numeric(df['Rang N'], errors='coerce')
df.fillna(0, inplace=True)

# Extraire les valeurs
percentiles = df['Rang N'].tolist()
values = df['CAR TBSE'].tolist()

# Afficher le graphique
plt.figure(figsize=(10,6))
plt.plot(percentiles, values, marker='o')
plt.title('Données CAR TBSE')
plt.xlabel('Rang N')
plt.ylabel('CAR TBSE')
plt.grid(True)
plt.show()
