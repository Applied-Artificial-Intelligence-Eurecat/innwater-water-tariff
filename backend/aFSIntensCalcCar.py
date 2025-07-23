import pandas as pd
import sqlite3

class aFSIntensCalcCar:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def build_dataframe(self, id_projet=1):
        # Construction des données sous forme de dictionnaire
        data = {
            'Déficit Apparent': ['Moyenne', 'Médiane', 'Variance', 'Ecart-type', 'cv', 'MAPE'],
            'CAR IBT': [10, 0, 390, 20, 2, 14],
            'CAR TBSE': [29, 0, 1719, 41, 1, 34],
            'Delta CAR': [-20, 0, 0, 0, 0, 0],
            'id_projet': [id_projet] * 6  # Ajout de la colonne id_projet identique pour chaque ligne
        }

        # Conversion en DataFrame
        df = pd.DataFrame(data)

        # Conversion des colonnes en entiers (si applicable)
        df['CAR IBT'] = df['CAR IBT'].astype(int)
        df['CAR TBSE'] = df['CAR TBSE'].astype(int)
        df['Delta CAR'] = df['Delta CAR'].astype(int)
        df['id_projet'] = df['id_projet'].astype(int)

        return df

    def create_table_in_db(self):
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Suppression de la table si elle existe déjà
        cursor.execute("DROP TABLE IF EXISTS aFSIntensCalcCar")

        # Création de la nouvelle table avec colonnes en INTEGER
        cursor.execute("""
            CREATE TABLE aFSIntensCalcCar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                DeficitApparent TEXT,
                CAR_IBT INTEGER,
                CAR_TBSE INTEGER,
                Delta_CAR INTEGER,
                id_projet INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def insert_data(self, id_projet=1):
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Récupération des données à insérer avec id_projet
        df = self.build_dataframe(id_projet=id_projet)

        # Insertion des données ligne par ligne
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO aFSIntensCalcCar (DeficitApparent, CAR_IBT, CAR_TBSE, Delta_CAR, id_projet)
                VALUES (?, ?, ?, ?, ?)
            """, (row['Déficit Apparent'], row['CAR IBT'], row['CAR TBSE'], row['Delta CAR'], row['id_projet']))

        # Validation et fermeture
        conn.commit()
        conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    builder = aFSIntensCalcCar()
    builder.create_table_in_db()           # Crée la table (avec colonnes INTEGER)
    builder.insert_data(id_projet=1001)    # Insère les données en précisant l'id_projet

    print("Table aFSIntensCalcCar créée et données entières insérées dans database.db")
