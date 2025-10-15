import pandas as pd
import sqlite3

class SocialDataManager:
    def __init__(self, db_name='database.db', id_projet=None):
        """Initialisation avec le nom de la base de données et un id_projet"""
        self.db_name = db_name
        self.id_projet = id_projet  # Attribut id_projet ajouté
        
    def create_dataframe(self):
        """Crée le DataFrame avec la structure demandée, en utilisant id_projet"""
        if self.id_projet is None:
            raise ValueError("L'id_projet doit être fourni pour créer le DataFrame")
        
        data = {
            "id_projet": [self.id_projet] * 6,
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
    
    def get_data(self):
        """Récupère les données depuis la table"""
        conn = sqlite3.connect(self.db_name)
        
        # Si un id_projet est fourni, on filtre les résultats
        if self.id_projet is not None:
            query = "SELECT id_projet, categorie, groupe, valeur FROM common_social_data WHERE id_projet = ?"
            params = (self.id_projet,)
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
    # Initialisation avec id_projet=1
    manager = SocialDataManager(db_name='database.db', id_projet=1)
    
    # Création de la table (avec suppression si elle existe déjà)
    manager.create_table()
    
    # Création d'un DataFrame avec l'id_projet initialisé
    df_data = manager.create_dataframe()
    print("DataFrame original:")
    print(df_data)
    
    # Insertion des données
    manager.insert_data(df_data)
    
    # Récupération des données
    loaded_data = manager.get_data()
    print("\nDonnées récupérées:")
    print(loaded_data)
