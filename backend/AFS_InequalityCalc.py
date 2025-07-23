import pandas as pd
import sqlite3

class AFS_InequalityCalc:
    def __init__(self, project_id):
        self.project_id = project_id
        self.database_name = "database.db"
    
    def build_dataframe(self):
        """
        Génère un DataFrame pandas avec la structure spécifiée
        et l'ID de projet fourni.
        """
        data = {
            "ensemble": ["Gini", "Schutz"],
            "ibt": [95.6, 92.3],
            "tbse": [79.3, 70.1],
            "id_projet": [self.project_id, self.project_id]
        }
        
        df = pd.DataFrame(data)
        return df
    
    def display_dataframe(self):
        """
        Affiche le DataFrame généré.
        """
        df = self.build_dataframe()
        print(df)
    
    def create_sqlite_table(self):
        """
        Crée ou écrase la table AFS_InequalityCalc dans la base SQLite.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS AFS_InequalityCalc (
            ensemble TEXT,
            ibt REAL,
            tbse REAL,
            id_projet INTEGER
        )
        """
        
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS AFS_InequalityCalc")
                cursor.execute(create_table_query)
                conn.commit()
            return True, "Table créée avec succès"
        except sqlite3.Error as e:
            return False, str(e)
    
    def insert_data(self):
        """
        Insère les données du DataFrame dans la table SQLite.
        """
        df = self.build_dataframe()
        
        insert_query = """
        INSERT INTO AFS_InequalityCalc (ensemble, ibt, tbse, id_projet)
        VALUES (?, ?, ?, ?)
        """
        
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                data_tuples = [tuple(x) for x in df.to_numpy()]
                cursor.executemany(insert_query, data_tuples)
                conn.commit()
            return True, "Données insérées avec succès"
        except sqlite3.Error as e:
            return False, str(e)
    
    def get_data_from_db(self):
        """
        Récupère les données de la base de données pour ce projet.
        """
        query = "SELECT ensemble, ibt, tbse FROM AFS_InequalityCalc WHERE id_projet = ?"
        
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (self.project_id,))
                rows = cursor.fetchall()
                
                if not rows:
                    return None
                
                columns = ['ensemble', 'ibt', 'tbse']
                return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return None

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance avec ID projet 123
    inequality_calc = AFS_InequalityCalc(123)
    
    # Affichage du DataFrame
    inequality_calc.display_dataframe()
    
    # Création de la table SQLite
    success, message = inequality_calc.create_sqlite_table()
    print(message)
    
    # Insertion des données
    success, message = inequality_calc.insert_data()
    print(message)
    
    print("\nNom du fichier SQLite : database.db")
    print("\nPas de clé primaire auto-générée")
