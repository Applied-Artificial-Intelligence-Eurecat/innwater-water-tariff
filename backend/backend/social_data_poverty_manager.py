import pandas as pd
import sqlite3

class PovertyDataManager:
    def __init__(self, db_name='poverty_data.db'):
        self.db_name = db_name
        
    def create_dataframe(self, id_projet=None):
        """Crée le DataFrame avec la structure demandée"""
        data = {
            "id_projet": [id_projet] * 6 if id_projet is not None else [None] * 6,
            "categorie": ["Ménages", "Ménages", "Individus", "Individus", "Enfants", "Enfants"],
            "groupe": ["Oxford", "OCDE", "Oxford", "OCDE", "Oxford", "OCDE"],
            "valeur": [52.8, 47.2, 59.3, 52.9, 65.9, 57.9]
        }
        return pd.DataFrame(data)
    
    def create_table(self):
        """Crée la table en supprimant d'abord si elle existe déjà"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Suppression de la table si elle existe
        cursor.execute('DROP TABLE IF EXISTS common_social_data')
        
        # Création de la table
        cursor.execute('''
        CREATE TABLE common_social_data (
            id_projet INTEGER,
            categorie TEXT NOT NULL,
            groupe TEXT NOT NULL,
            valeur REAL NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Table common_social_data recréée dans {self.db_name}")
    
    def insert_data(self, df):
        """Insère les données du DataFrame dans la table"""
        conn = sqlite3.connect(self.db_name)
        
        # Vérification que les colonnes correspondent
        if not all(col in df.columns for col in ['id_projet', 'categorie', 'groupe', 'valeur']):
            raise ValueError("Le DataFrame ne contient pas les colonnes attendues")
        
        # Insertion des données
        df[['id_projet', 'categorie', 'groupe', 'valeur']].to_sql(
            'common_social_data',
            conn,
            if_exists='append',
            index=False
        )
        
        conn.close()
        print(f"{len(df)} lignes insérées avec succès")
    
    def get_data(self, id_projet=None):
        """Récupère les données depuis la table"""
        conn = sqlite3.connect(self.db_name)
        
        if id_projet is not None:
            query = "SELECT id_projet, categorie, groupe, valeur FROM common_social_data WHERE id_projet = ?"
            params = (int(id_projet),)
        else:
            query = "SELECT id_projet, categorie, groupe, valeur FROM common_social_data"
            params = ()
            
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        
        # Conversion des types
        df['id_projet'] = df['id_projet'].astype('Int64')
        
        return df

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialisation
    manager = PovertyDataManager(db_name='database.db')
    
    # Création de la table (avec suppression si existe déjà)
    manager.create_table()
    
    # Création d'un DataFrame avec id_projet = 1
    df_data = manager.create_dataframe(id_projet=1)
    print("DataFrame original:")
    print(df_data)
    
    # Insertion des données
    manager.insert_data(df_data)
    
    # Récupération des données
    loaded_data = manager.get_data(id_projet=1)
    print("\nDonnées récupérées:")
    print(loaded_data)
