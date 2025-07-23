import pandas as pd
import sqlite3
from typing import Dict, List

class AFS_AffordabilityIndicatorDW:
    def __init__(self, project_id: int = 1):
        self.project_id = project_id
        self.database_name = "database.db"
        self.table_name = "AFS_AffordabilityIndicatorDW"
        
    def build_dataframe(self) -> pd.DataFrame:
        """Génère le DataFrame avec la structure demandée"""
        data: Dict[str, List[float]] = {
            "PAR_IBT": [0.0, 10.9, 0.3, 1.4, 0.1, 2.6, 68.5, 1.89, 1.4, 0.9, 1.216, 1.1, 2.5, 0.29],
            "PAR_TBSE": [0.1, 21.9, 0.9, 3.9, 0.5, 8.0, 69.3, 12.64, 3.6, 2.5, 1.119, 3.0, 7.5, 0.30]
        }
        
        index = [
            "Min", "Max", "Q1", "Q3", "D1", "D9", "F (Moyenne)", "Variance", 
            "Ecart-type", "MAPE", "Coeff de Variation", "Etendue Interquantiles",
            "Etendue Interdéciles", "Coefficients de Yule"
        ]
        
        df = pd.DataFrame(data, index=index)
        df.index.name = "indicator"
        df.reset_index(inplace=True)
        
        # Ajout de la colonne ID_Projet
        df["id_projet"] = self.project_id
        
        return df
    
    def create_sqlite_table(self) -> None:
        """Crée ou écrase la table dans la base SQLite"""
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            indicator TEXT,
            par_ibt REAL,
            par_tbse REAL,
            id_projet INTEGER
        )
        """
        
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            # Suppression de la table si elle existe déjà
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            # Création de la nouvelle table
            cursor.execute(create_table_query)
            conn.commit()
    
    def insert_data(self) -> None:
        """Insère les données du DataFrame dans la table SQLite"""
        df = self.build_dataframe()
        
        # Conversion des données en tuples pour l'insertion
        data_to_insert = [
            (row["indicator"], row["PAR_IBT"], row["PAR_TBSE"], row["id_projet"])
            for _, row in df.iterrows()
        ]
        
        insert_query = f"""
        INSERT INTO {self.table_name} 
        (indicator, par_ibt, par_tbse, id_projet) 
        VALUES (?, ?, ?, ?)
        """
        
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
    
    def run(self) -> None:
        """Méthode principale qui exécute toutes les étapes"""
        df = self.build_dataframe()
        print("DataFrame généré :\n")
        print(df)
        print("\nNom du fichier SQLite :", self.database_name)
        print("\nPas de clé primaire auto-générée")
        
        self.create_sqlite_table()
        self.insert_data()


# Exemple d'utilisation
if __name__ == "__main__":
    indicator = AFS_AffordabilityIndicatorDW(project_id=1)
    indicator.run()