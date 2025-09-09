import sqlite3
import pandas as pd


class CommoAbsrvinsert:
    def __init__(self, db_name="abonnements.db"):
        """
        Initialise la connexion à la base SQLite.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def insert_dataframe(self, df: pd.DataFrame):
        """
        Insère les données du DataFrame dans la table 'commonAb'.
        """
        for _, row in df.iterrows():
            try:
                self.cursor.execute("""
                    INSERT INTO commonAb 
                    (id_projet, type_abonnement, prix_ht_op, redevances, prix_ht_tva, 
                     montant_tva_par_unite_service, prix_ttc)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, tuple(row))
            except sqlite3.IntegrityError as e:
                print(f"⚠️ Erreur d'insertion pour id_projet={row['id_projet']} : {e}")

        self.conn.commit()

    def close(self):
        """
        Ferme la connexion à la base SQLite.
        """
        self.conn.close()
