import pandas as pd
import sqlite3

class CommonSeuilManager:
    def __init__(self, id_projet: int = 1):
        # Identifiant du projet
        self.id_projet = id_projet

        # Données fixes avec noms de colonnes normalisés
        self.data = [
            {"seuil": "PAR", "unites": 3, "comments": "en %", "id_projet": self.id_projet},
            {"seuil": "CAR", "unites": 3, "comments": "en %", "id_projet": self.id_projet},
            {"seuil": "Pauvrete", "unites": 800, "comments": "en euros, Niveau de vie", "id_projet": self.id_projet}
        ]
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Génère un DataFrame structuré avec les colonnes normalisées et id_projet.
        """
        df = pd.DataFrame(self.data, columns=["id_projet", "seuil", "unites", "comments"])
        return df

    def create_table_and_insert(self, db_name: str = "database.db"):
        """
        Supprime la table si elle existe, la recrée avec les colonnes normalisées, 
        puis insère le contenu fixe du DataFrame.
        """
        df = self.get_dataframe()

        # Connexion à la base
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Supprimer la table si elle existe déjà
        cursor.execute("DROP TABLE IF EXISTS social_data_seuil_manager")

        # Création de la table avec colonnes normalisées
        cursor.execute("""
            CREATE TABLE social_data_seuil_manager (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projet INTEGER NOT NULL,
                seuil TEXT NOT NULL,
                unites REAL,
                comments TEXT
            )
        """)

        # Insertion des données fixes
        df.to_sql("social_data_seuil_manager", conn, if_exists="append", index=False)

        conn.commit()
        conn.close()
        print(f"Données fixes insérées dans {db_name} → table social_data_seuil_manager (table recréée)")

# Exemple d'utilisation
if __name__ == "__main__":
    seuil_manager = CommonSeuilManager()
    seuil_manager.create_table_and_insert()
