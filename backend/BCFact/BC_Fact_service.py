import sqlite3
import pandas as pd

class BC_Fact_service:
    def __init__(self, db_path="database.db", table_name="partie_base_c_et_fact_table"):
        self.db_path = db_path
        self.table_name = table_name

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Insère un DataFrame pandas dans la table SQLite.
        Le DataFrame doit avoir les mêmes colonnes que la table
        (sauf 'id' et 'created_at' qui sont gérés automatiquement).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                df.to_sql(self.table_name, conn, if_exists="append", index=False)
            print(f"{len(df)} lignes insérées dans {self.table_name}.")
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")


def main():
    # Exemple de DataFrame à insérer (à compléter avec toutes les colonnes réelles)
    data = {
        "vexp_cc_men": [1.2, 2.5],
        "vexp_cc_ass": [3.4, 4.5],
        "vexp_cc_const": [5.6, 6.7],
        # ⚠️ Ajouter ici toutes les colonnes nécessaires à la table sauf 'id' et 'created_at'
    }

    df = pd.DataFrame(data)

    # Instanciation du service
    service = BC_Fact_service()

    # Insertion du DataFrame
    service.insert_dataframe(df)


if __name__ == "__main__":
    main()
