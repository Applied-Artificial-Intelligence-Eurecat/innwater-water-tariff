import sqlite3

class comonNordinCreateSrv:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def create_table(self):
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Supprimer la table si elle existe déjà
        cursor.execute("DROP TABLE IF EXISTS comonNordin")
        
        # Créer la table comonNordin sans clé primaire
        cursor.execute("""
            CREATE TABLE comonNordin (
                id_projet INTEGER,
                type_nordin TEXT,
                num_tranche INTEGER,
                d_nordin_op TEXT,
                d_nordin_redevances_ht REAL,
                d_nordin_ttc REAL
            )
        """)
        
        # Valider les changements et fermer la connexion
        conn.commit()
        conn.close()
        print("Table 'comonNordin' créée avec succès.")

# Exemple d'utilisation
if __name__ == "__main__":
    srv = comonNordinCreateSrv()
    srv.create_table()
