import pandas as pd
import sqlite3
from typing import Dict, Any

class AFSIntensityCalc:
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.df = None

    def build_dataframe(self) -> pd.DataFrame:
        """Génère le DataFrame avec la structure demandée"""
        data = {
            'par_ibt': [1.39, 0.00, 38.5366, 6.21, 4.47, 2.57],
            'par_tbse': [17.47, 0.00, 1013.2596, 31.83, 1.82, 24.49],
            'delta_par': [-16.08, 0.00, None, None, None, None],
            'de_moy': [17.69, 16.15, 2.08, 37.01, 202.0810, 14.22],
            'de_med': [53.33, 43.78, 11.03, 102.79, 1181.3969, 34.37],
            'de_d1': [None, None, None, None, None, None],
            'de_d9': [None, None, None, None, None, None],
            'de_var': [-35.64, None, None, None, None, None],
            'de_std': [0.804, None, None, None, None, None],
            'de_cv': [0.645, None, None, None, None, None],
            'de_mape': [11.25, 30.19, None, None, None, None]
        }

        index = ['da_moy', 'da_med', 'da_var', 'da_std', 'da_cv', 'da_mape']

        self.df = pd.DataFrame(data, index=index)
        
        # Ajout de la colonne project_id (English instead of id_projet)
        self.df['project_id'] = self.project_id
        
        # Réorganiser les colonnes pour mettre project_id en premier
        cols = ['project_id'] + [col for col in self.df.columns if col != 'project_id']
        self.df = self.df[cols]
        
        return self.df

    def create_sqlite_table(self, db_name: str = 'database.db') -> None:
        """Crée ou écrase la table SQLite"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS afs_intensitycalc (
            project_id INTEGER,
            metric_name TEXT,
            par_ibt REAL,
            par_tbse REAL,
            delta_par REAL,
            de_moy REAL,
            de_med REAL,
            de_d1 REAL,
            de_d9 REAL,
            de_var REAL,
            de_std REAL,
            de_cv REAL,
            de_mape REAL
        )
        """
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS afs_intensitycalc")
            cursor.execute(create_table_query)
            conn.commit()

    def insert_data(self, db_name: str = 'database.db') -> None:
        """Insère les données du DataFrame dans SQLite"""
        if self.df is None:
            self.build_dataframe()
        
        insert_query = """
        INSERT INTO afs_intensitycalc (
            project_id, metric_name, par_ibt, par_tbse, delta_par, 
            de_moy, de_med, de_d1, de_d9, de_var, de_std, de_cv, de_mape
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            # Préparer les données pour l'insertion
            data_to_insert = []
            for index, row in self.df.iterrows():
                data_to_insert.append((
                    int(row['project_id']),
                    str(index),
                    float(row['par_ibt']),
                    float(row['par_tbse']),
                    float(row['delta_par']) if pd.notna(row['delta_par']) else None,
                    float(row['de_moy']) if pd.notna(row['de_moy']) else None,
                    float(row['de_med']) if pd.notna(row['de_med']) else None,
                    float(row['de_d1']) if 'de_d1' in row and pd.notna(row['de_d1']) else None,
                    float(row['de_d9']) if 'de_d9' in row and pd.notna(row['de_d9']) else None,
                    float(row['de_var']) if 'de_var' in row and pd.notna(row['de_var']) else None,
                    float(row['de_std']) if pd.notna(row['de_std']) else None,
                    float(row['de_cv']) if 'de_cv' in row and pd.notna(row['de_cv']) else None,
                    float(row['de_mape']) if pd.notna(row['de_mape']) else None
                ))
            
            # Exécuter l'insertion
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()


# Exemple d'utilisation
if __name__ == "__main__":
    # Création de l'instance avec un ID de projet
    afs_calc = AFSIntensityCalc(project_id=1)
    
    # Génération du DataFrame
    df = afs_calc.build_dataframe()
    print("DataFrame généré :")
    print(df)
    print("\nNom du fichier SQLite : database.db")
    
    # Création de la table SQLite
    afs_calc.create_sqlite_table()
    
    # Insertion des données
    afs_calc.insert_data()