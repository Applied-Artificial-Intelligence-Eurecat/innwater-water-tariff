import sqlite3
import pandas as pd

class ComonTarifTableInsert:
    """
    Service pour gérer la table comon_tarif :
    - création si elle n'existe pas
    - insertion à partir d'un DataFrame
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_table(self):
        """
        Crée la table comon_tarif si elle n'existe pas.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comon_tarif (
                id_projet INTEGER,
                type_tarif TEXT,
                indice TEXT,
                bornes INTEGER,
                prix_ht_op REAL,
                redevances REAL,
                prix_htva REAL,
                montant_tva_unite_service REAL,
                prix_ttc REAL
            )
        """)
        conn.commit()
        conn.close()

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Insère les données d'un DataFrame dans la table comon_tarif.
        """
        required_columns = [
            "id_projet",
            "type_tarif",
            "indice",
            "bornes",
            "prix_ht_op",
            "redevances",
            "prix_htva",
            "montant_tva_unite_service",
            "prix_ttc"
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing_cols}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            insert_query = """
                INSERT INTO comon_tarif (
                    id_projet,
                    type_tarif,
                    indice,
                    bornes,
                    prix_ht_op,
                    redevances,
                    prix_htva,
                    montant_tva_unite_service,
                    prix_ttc
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            data_to_insert = df[required_columns].values.tolist()
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
        finally:
            conn.close()


def main():
    db_path = "database.db"

    data = {
        "id_projet": [1]*10,
        "type_tarif": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP"],
        "indice": ["k0", "k1", "k2", "k0", "k1", "k2", "k3", "k0", "k1", "k2"],
        "bornes": [0, 15, 30, 0, 15, 30, 60, 0, 15, 30],
        "prix_ht_op": [2.178, 3.959, 4.978, 1.3, 2.12, 2.21, 2.5, 0.878, 1.839, 2.768],
        "redevances": [0.16, 0.16, 0.16, 0.04, 0.04, 0.04, 0.04, 0.12, 0.12, 0.12],
        "prix_htva": [2.338, 4.119, 5.138, 1.34, 2.16, 2.25, 2.54, 0.998, 1.959, 2.888],
        "montant_tva_unite_service": [0.154958, 0.257139, 0.285648, 0.134, 0.216, 0.225, 0.254, 0.020958, 0.041139, 0.060648],
        "prix_ttc": [2.492958, 4.376139, 5.423648, 1.474, 2.376, 2.475, 2.794, 1.018958, 2.000139, 2.948648]
    }

    df = pd.DataFrame(data)
    service = ComonTarifTableInsert(db_path)
    service.create_table()
    service.insert_dataframe(df)

    print("✅ Données insérées avec succès dans la table comon_tarif.")


if __name__ == "__main__":
    main()
