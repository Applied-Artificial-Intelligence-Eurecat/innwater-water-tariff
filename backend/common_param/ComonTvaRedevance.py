import sqlite3

class ComonTvaRedevance:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.drop_table_if_exists()  # Supprime la table si elle existe
        self.create_table()
    
    def drop_table_if_exists(self):
        """Supprime la table si elle existe déjà"""
        drop_table_sql = "DROP TABLE IF EXISTS comoTva_redevance;"
        self.cursor.execute(drop_table_sql)
        self.conn.commit()
    
    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS comoTva_redevance (
            id_projet INTEGER NOT NULL,
            type_taxe TEXT NOT NULL,
            taux_tva_pourcent REAL NOT NULL,
            redevances_accise_euro_m3 REAL NOT NULL
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()
    
    def insert_record(self, id_projet, type_taxe, taux_tva_pourcent, redevances_accise_euro_m3):
        insert_sql = """
        INSERT INTO comoTva_redevance (id_projet, type_taxe, taux_tva_pourcent, redevances_accise_euro_m3)
        VALUES (?, ?, ?, ?);
        """
        self.cursor.execute(insert_sql, (id_projet, type_taxe, taux_tva_pourcent, redevances_accise_euro_m3))
        self.conn.commit()
    
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM comoTva_redevance;")
        return self.cursor.fetchall()
    
    def fetch_by_project(self, id_projet):
        self.cursor.execute("SELECT * FROM comoTva_redevance WHERE id_projet = ?;", (id_projet,))
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Exemple d'utilisation avec vos données
if __name__ == "__main__":
    db = ComonTvaRedevance()
    
    # Exemple d'insertion de données
    # db.insert_record(1, "TVA", 20.0, 15.50)
    # db.insert_record(2, "Accise", 10.0, 25.75)
    
    # Affichage de tous les enregistrements
    # records = db.fetch_all()
    # print("Tous les enregistrements:", records)
    
    db.close()