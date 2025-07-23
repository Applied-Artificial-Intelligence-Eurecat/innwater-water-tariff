from flask import Flask, jsonify, abort
import pandas as pd
from typing import Dict, Any
import sqlite3

class AFS_IncidenceCalc:
    def __init__(self, project_id: int = 1):
        self.project_id = project_id
        self.database_name = "database.db"
        self.table_name = "afs_incidence_calc"

    def build_dataframe(self) -> pd.DataFrame:
        """Génère le DataFrame avec la structure demandée"""
        data = {
            "headcount_ratio": [7.9, 7.9, 9.9],
            "par_ibt": [32.8, 31.6, 35.1],
            "par_tbse": [7.9, 7.9, 9.9],
            "delta_par": [-24.9, -23.8, -25.2]
        }

        index = ["Ménages", "Individus", "Enfants"]

        df = pd.DataFrame(data, index=index)
        df.index.name = "category"
        df.reset_index(inplace=True)

        # Ajout de la colonne ID_Projet
        df["id_projet"] = self.project_id

        # Réorganiser les colonnes
        df = df[["id_projet", "category", "headcount_ratio", "par_ibt", "par_tbse", "delta_par"]]

        return df

    def create_sqlite_table(self):
        """Crée la table SQLite si elle n'existe pas"""
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projet INTEGER,
                category TEXT,
                headcount_ratio REAL,
                par_ibt REAL,
                par_tbse REAL,
                delta_par REAL
            )
        """)

        conn.commit()
        conn.close()

    def insert_data(self):
        """Insère le DataFrame dans la table SQLite"""
        df = self.build_dataframe()

        conn = sqlite3.connect(self.database_name)
        df.to_sql(self.table_name, conn, if_exists='append', index=False)
        conn.close()
from AFS_IncidenceCalc import AFS_IncidenceCalc

if __name__ == "__main__":
    # Crée une instance avec project_id=1
    incidence_calc = AFS_IncidenceCalc(project_id=1)

    print("🔧 Initialisation de AFS_IncidenceCalc\n")

    # 1. Construire le DataFrame
    print("▶️ build_dataframe()")
    df = incidence_calc.build_dataframe()
    print(df)
    print("✅ DataFrame construit.\n")

    # 2. Créer la table SQLite
    print("▶️ create_sqlite_table()")
    incidence_calc.create_sqlite_table()
    print("✅ Table SQLite créée.\n")

    # 3. Insérer les données dans la table SQLite
    print("▶️ insert_data()")
    incidence_calc.insert_data()
    print("✅ Données insérées dans la base SQLite.\n")

    print("🎯 Exécution complète de AFS_IncidenceCalc terminée.")
    print(f"📂 Base SQLite : {incidence_calc.database_name}")
