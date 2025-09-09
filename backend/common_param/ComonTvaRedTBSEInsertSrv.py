# comonTvaRedTBSEInsertSrv.py

import sqlite3
import pandas as pd

class ComonTvaRedTBSEInsertSrv:
    def __init__(self, db_path: str):
        """
        Initialise la connexion à la base SQLite.
        :param db_path: chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        """
        Crée la table comonTvaRedevanceTBSE si elle n'existe pas.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS comonTvaRedevanceTBSE (
            id_projet INTEGER NOT NULL,
            type_tva TEXT NOT NULL,
            taux_tva_pct REAL NOT NULL,
            redevances_accise_eur_m3 REAL NOT NULL
        );
        """
        self.conn.execute(create_table_query)
        self.conn.commit()

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Insère les données d'un DataFrame dans la table comonTvaRedevanceTBSE.
        :param df: DataFrame avec les colonnes id_projet, type_tva, taux_tva_pct, redevances_accise_eur_m3
        """
        required_columns = {'id_projet', 'type_tva', 'taux_tva_pct', 'redevances_accise_eur_m3'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Le DataFrame doit contenir les colonnes: {required_columns}")

        df.to_sql('comonTvaRedevanceTBSE', self.conn, if_exists='append', index=False)

    def close(self):
        """
        Ferme la connexion à la base.
        """
        self.conn.close()


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    # Création du DataFrame avec les valeurs fournies
    df = pd.DataFrame({
        'id_projet': [1, 1, 1],
        'type_tva': ['EPA', 'A', 'EPA'],
        'taux_tva_pct': [0, 10, 2.1],
        'redevances_accise_eur_m3': [0.16, 0.04, 0.12]
    })

    # Insertion dans la base
    inserter = ComonTvaRedTBSEInsertSrv('database.db')
    inserter.insert_dataframe(df)
    inserter.close()
