import sqlite3

class comonTvaRedTBSECreateSrv:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def create_table(self):
        """
        Crée la table comonTvaRedevanceTBSE si elle n'existe pas déjà
        dans la base database.db
        """
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comonTvaRedevanceTBSE (
                id_projet INTEGER NOT NULL,
                type_tva TEXT NOT NULL,
                taux_tva_pct REAL NOT NULL,
                redevances_accise_eur_m3 REAL NOT NULL
            );
        """)

        connection.commit()
        connection.close()


# Exemple d’utilisation
if __name__ == "__main__":
    service = comonTvaRedTBSECreateSrv()
    service.create_table()
    print("Table comonTvaRedevanceTBSE créée avec succès dans database.db")
