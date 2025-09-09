import sqlite3

class comonTarifTableCreateSrv:
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.create_table()  # La table est créée dès l'initialisation

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Supprimer la table si elle existe déjà
        cursor.execute("DROP TABLE IF EXISTS comon_tarif")

        # Créer la table avec la structure demandée
        cursor.execute("""
            CREATE TABLE comon_tarif (
                id_projet INTEGER,
                type_tarif TEXT,
                indice INTEGER,
                bornes TEXT,
                prix_ht_op REAL,
                redevances REAL,
                prix_htva REAL,
                montant_tva_unite_service REAL,
                prix_ttc REAL
            )
        """)

        conn.commit()
        conn.close()


if __name__ == "__main__":
    table_creator = comonTarifTableCreateSrv()
    print("Table 'comon_tarif' initialisée avec succès dans database.db")
