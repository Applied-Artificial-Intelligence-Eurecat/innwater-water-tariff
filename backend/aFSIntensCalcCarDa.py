# aFSIntensCalcCarDa.py

import pandas as pd
import sqlite3

class aFSIntensCalcCarDa:
    def __init__(self, id_projet=1, db_path='database.db'):
        self.id_projet = id_projet
        self.db_path = db_path  # Nom de ta base de données SQLite

        # Valeurs initiales avec préfixe da_
        self.car_ibt_values = {
            'da_Moyenne': 33.00,
            'da_Médiane': 27.85,
            'da_D1': 6.07,
            'da_D9': 64.50,
            'da_Variance': 576.8663,
            'da_Ecart-type': 24.02,
            'da_cv': 0.728,
            'da_MAPE': 19.26
        }

        self.car_tbse_values = {
            'da_Moyenne': 60.17,
            'da_Médiane': 52.73,
            'da_D1': 9.73,
            'da_D9': 119.81,
            'da_Variance': 1688.4959,
            'da_Ecart-type': 41.09,
            'da_cv': 0.683,
            'da_MAPE': 35.64
        }

    def create_dataframe(self):
        # Création du DataFrame à partir des dictionnaires avec noms conformes à la table SQLite
        df = pd.DataFrame({
            'CAR_IBT': pd.Series(self.car_ibt_values),
            'CAR_TBSE': pd.Series(self.car_tbse_values)
        })

        # Calcul de Delta CAR (IBT - TBSE)
        df['Delta_CAR'] = df['CAR_IBT'] - df['CAR_TBSE']

        # Conversion en entiers
        df['CAR_IBT'] = df['CAR_IBT'].astype(int)
        df['CAR_TBSE'] = df['CAR_TBSE'].astype(int)
        df['Delta_CAR'] = df['Delta_CAR'].fillna(0).astype(int)

        # Ajout de la colonne id_projet
        df['id_projet'] = self.id_projet

        # Réorganisation des colonnes pour mettre id_projet en premier
        df = df.reset_index().rename(columns={'index': 'Metric'})
        df = df[['id_projet', 'Metric', 'CAR_IBT', 'CAR_TBSE', 'Delta_CAR']]

        return df

    def create_table(self, table_name='aFSIntensCalcCarDa'):
        # Connexion à la base SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Suppression de la table si elle existe déjà
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()

            # Création de la table vide avec les bonnes colonnes
            cursor.execute(f"""
                CREATE TABLE {table_name} (
                    id_projet INTEGER,
                    Metric TEXT,
                    CAR_IBT INTEGER,
                    CAR_TBSE INTEGER,
                    Delta_CAR INTEGER
                )
            """)
            conn.commit()

            print(f"✅ Table '{table_name}' recréée avec succès.")

    def insert_data(self, table_name='aFSIntensCalcCarDa'):
        # Récupération du DataFrame
        df = self.create_dataframe()

        # Connexion à la base SQLite
        with sqlite3.connect(self.db_path) as conn:
            # Insertion des données du DataFrame dans la table existante
            df.to_sql(table_name, conn, if_exists='append', index=False)

            print(f"✅ Données insérées avec succès dans la table '{table_name}'.")

# Exemple d’utilisation
if __name__ == "__main__":
    calc = aFSIntensCalcCarDa(id_projet=101, db_path='database.db')
    calc.create_table(table_name='aFSIntensCalcCarDa')  # Crée ou recrée la table
    calc.insert_data(table_name='aFSIntensCalcCarDa')   # Insère les données
