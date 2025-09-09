import sqlite3
import pandas as pd
from sqlite3 import Error

class CommonTBSETable:
    def __init__(self, db_file="database.db"):
        self.db_file = db_file
        self.connection = None
    
    def create_connection(self):
        """Crée une connexion à la base de données SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            return self.connection
        except Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None
    
    def drop_table_if_exists(self):
        """Supprime la table si elle existe déjà"""
        drop_table_sql = "DROP TABLE IF EXISTS CommonTarifTBSEModel;"
        
        try:
            conn = self.create_connection()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(drop_table_sql)
                conn.commit()
                print("Table CommonTarifTBSEModel supprimée si elle existait")
            else:
                print("Erreur: Impossible de se connecter à la base de données")
        except Error as e:
            print(f"Erreur lors de la suppression de la table: {e}")
        finally:
            if conn:
                conn.close()
    
    def create_table(self):
        """Crée la table CommonTarifTBSEModel avec la structure demandée"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS CommonTarifTBSEModel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projet INTEGER,
            nature_tarif TEXT,
            type_tarif TEXT,
            prix_ht_op REAL,
            redevances REAL,
            prix_ht_tva REAL,
            montant_tva_unite_service REAL,
            prix_ttc REAL
        );
        """
        
        try:
            conn = self.create_connection()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
                print("Table CommonTarifTBSEModel créée avec succès")
            else:
                print("Erreur: Impossible de se connecter à la base de données")
        except Error as e:
            print(f"Erreur lors de la création de la table: {e}")
        finally:
            if conn:
                conn.close()
    
    def recreate_table(self):
        """Supprime et recrée la table (méthode utilitaire)"""
        self.drop_table_if_exists()
        self.create_table()
    
    def insert_data(self, id_projet, nature_tarif, type_tarif, prix_ht_op, redevances, 
                   prix_ht_tva, montant_tva_unite_service, prix_ttc):
        """Insère des données dans la table"""
        insert_sql = """
        INSERT INTO CommonTarifTBSEModel 
        (id_projet, nature_tarif, type_tarif, prix_ht_op, redevances, prix_ht_tva, montant_tva_unite_service, prix_ttc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        data = (id_projet, nature_tarif, type_tarif, prix_ht_op, redevances, 
                prix_ht_tva, montant_tva_unite_service, prix_ttc)
        
        try:
            conn = self.create_connection()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(insert_sql, data)
                conn.commit()
                print("Données insérées avec succès")
                return cursor.lastrowid
        except Error as e:
            print(f"Erreur lors de l'insertion des données: {e}")
        finally:
            if conn:
                conn.close()
    
    def insert_dataframe(self, df):
        """
        Insère un DataFrame pandas dans la table CommonTarifTBSEModel
        
        Args:
            df (pandas.DataFrame): DataFrame avec les colonnes:
                id_projet, nature_tarif, type_tarif, prix_ht_op, redevances,
                prix_ht_tva, montant_tva_unite_service, prix_ttc
        """
        try:
            conn = self.create_connection()
            if conn is not None:
                # Conversion des virgules en points pour les nombres
                numeric_columns = ['prix_ht_op', 'redevances', 'prix_ht_tva', 
                                 'montant_tva_unite_service', 'prix_ttc']
                
                for col in numeric_columns:
                    if col in df.columns:
                        # Convertit les chaînes avec virgules en floats
                        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
                
                # Insertion des données
                df.to_sql('CommonTarifTBSEModel', conn, if_exists='append', index=False)
                conn.commit()
                print(f"{len(df)} lignes insérées avec succès depuis le DataFrame")
            else:
                print("Erreur: Impossible de se connecter à la base de données")
        except Error as e:
            print(f"Erreur lors de l'insertion du DataFrame: {e}")
        except Exception as e:
            print(f"Erreur lors du traitement des données: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_all_data(self):
        """Récupère toutes les données de la table"""
        select_sql = "SELECT * FROM CommonTarifTBSEModel"
        
        try:
            conn = self.create_connection()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(select_sql)
                rows = cursor.fetchall()
                return rows
        except Error as e:
            print(f"Erreur lors de la récupération des données: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_all_data_as_dataframe(self):
        """Récupère toutes les données de la table sous forme de DataFrame pandas"""
        try:
            conn = self.create_connection()
            if conn is not None:
                df = pd.read_sql_query("SELECT * FROM CommonTarifTBSEModel", conn)
                return df
        except Error as e:
            print(f"Erreur lors de la récupération des données: {e}")
        finally:
            if conn:
                conn.close()
    
    def close_connection(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()

# Exemple d'utilisation avec DataFrame
if __name__ == "__main__":
    # Création de l'instance
    tarse_table = CommonTBSETable()
    
    # Suppression et création de la table
    tarse_table.recreate_table()
    
    # Création d'un DataFrame avec les données fournies
    data = {
        'id_projet': [1, 1, 1, 1, 1, 1],
        'nature_tarif': ['TBSE EP', 'TBSE EP', 'TBSE A', 'TBSE A', 'TBSE EPA', 'TBSE EPA'],
        'type_tarif': ['Abonnement', 'Prix unitaire (au mètre 3)', 
                      'Abonnement', 'Prix unitaire (au mètre 3)', 
                      'Abonnement', 'Prix unitaire (au mètre 3)'],
        'prix_ht_op': ['47,0249', '0,9000', '59,2885', '0,4000', '106,3134', '1,3000'],
        'redevances': ['0,0000', '0,1200', '0,0000', '0,0400', '0,0000', '0,1600'],
        'prix_ht_tva': ['47,0249', '1,0200', '59,2885', '0,4400', '106,3134', '1,4600'],
        'montant_tva_unite_service': ['0,9875', '0,0214', '5,9289', '0,0440', '6,9164', '0,0654'],
        'prix_ttc': ['48,0124', '1,0414', '65,2174', '0,4840', '113,2298', '1,5254']
    }
    
    df = pd.DataFrame(data)
    print("DataFrame à insérer:")
    print(df)
    print("\n")
    
    # Insertion du DataFrame
    tarse_table.insert_dataframe(df)
    
    # Vérification des données insérées
    print("Données dans la base après insertion:")
    result_df = tarse_table.get_all_data_as_dataframe()
    print(result_df)