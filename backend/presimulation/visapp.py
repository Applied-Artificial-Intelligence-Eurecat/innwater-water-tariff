import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier Excel
fichier_excel = "NIVEAUVIEPARTBSE.xls"
df = pd.read_excel(fichier_excel)
df.columns = df.columns.str.strip()  # Nettoyer les noms de colonnes

# Vérifier la présence des colonnes nécessaires
if 'Niveau de Vie OCDE' not in df.columns or 'Par TBSE' not in df.columns:
    raise ValueError("Les colonnes 'Niveau de Vie OCDE' et 'Par TBSE' sont manquantes dans le fichier Excel.")

# Convertir les colonnes en numériques
df['Niveau de Vie OCDE'] = pd.to_numeric(df['Niveau de Vie OCDE'], errors='coerce')
df['Par TBSE'] = pd.to_numeric(df['Par TBSE'], errors='coerce')
df.fillna(0, inplace=True)

# Extraire les valeurs
x = df['Niveau de Vie OCDE'].tolist()
y = df['Par TBSE'].tolist()

# Afficher le scatter plot
plt.figure(figsize=(10,6))
plt.scatter(x, y, color='blue', alpha=0.7)
plt.title('Scatter Plot : Niveau de Vie OCDE vs Par TBSE')
plt.xlabel('Niveau de Vie OCDE')
plt.ylabel('Par TBSE')
plt.grid(True)
plt.show()
