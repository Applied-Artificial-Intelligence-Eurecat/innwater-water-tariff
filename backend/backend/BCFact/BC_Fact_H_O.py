import sqlite3

class BC_Fact_H_O:
    def __init__(self, db_name="database.db", table_name="partie_base_c_et_fact_table"):
        """
        Initialise la connexion à la base de données SQLite.
        
        :param db_name: Nom du fichier de la base de données.
        :param table_name: Nom de la table cible.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connecté à {self.db_name}")
        except sqlite3.Error as e:
            print(f"Erreur de connexion : {e}")

    def disconnect(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            self.connection.close()
            print("Connexion fermée.")

    def fetch_all(self):
        """Récupère toutes les lignes de la table."""
        if not self.cursor:
            raise Exception("Pas de connexion active. Appelez connect() d'abord.")
        query = f"SELECT * FROM {self.table_name}"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return []

    def insert(self, columns, values):
        """
        Insère une ligne dans la table.
        
        :param columns: Liste des colonnes (ex: ['col1', 'col2']).
        :param values: Liste des valeurs correspondantes.
        """
        if not self.cursor:
            raise Exception("Pas de connexion active. Appelez connect() d'abord.")
        placeholders = ", ".join(["?"] * len(values))
        cols = ", ".join(columns)
        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Ligne insérée avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion : {e}")

# === Main ===
if __name__ == "__main__":
    # Crée l'objet
    db = BC_Fact_H_O()

    # Connexion à la base
    db.connect()

    # Récupère toutes les lignes
    rows = db.fetch_all()
    if rows:
        print("Données de la table :")
        for row in rows:
            print(row)
    else:
        print("Aucune donnée trouvée.")

    # Déconnexion
    db.disconnect()
