import sqlite3

class c_Ab_srvCreate:
    def __init__(self, db_name="database.db"):
        """
        Initialise la connexion à la base SQLite.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        Supprime la table commonAb si elle existe, puis la recrée.
        """
        # Supprimer la table si elle existe
        self.cursor.execute("DROP TABLE IF EXISTS commonAb;")

        # Créer la table (aucune clé primaire)
        self.cursor.execute("""
            CREATE TABLE commonAb (
                id_projet INTEGER,
                type_abonnement TEXT NOT NULL,
                prix_ht_op REAL NOT NULL,
                redevances REAL NOT NULL,
                prix_ht_tva REAL NOT NULL,
                montant_tva_par_unite_service REAL NOT NULL,
                prix_ttc REAL NOT NULL
            );
        """)
        self.conn.commit()

    def close(self):
        """
        Ferme la connexion à la base SQLite.
        """
        self.conn.close()


if __name__ == "__main__":
    ab_creator = c_Ab_srvCreate("database.db")
    ab_creator.create_table()
    ab_creator.close()
    print("Table 'commonAb' recréée avec succès ✅")
