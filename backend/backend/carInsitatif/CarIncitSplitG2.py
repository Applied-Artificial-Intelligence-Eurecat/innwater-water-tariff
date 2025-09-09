import pandas as pd
import sqlite3
from typing import Optional

class CarIncitSplitG2:
    def __init__(self):
        """
        Initialise la classe avec la base de données database.db
        """
        self.db_path = "database.db"
        self.table_source = "carInsitatifdataintermed"
        self.table_cible = "CarInsitatifdataintermedG2"
        self.connection = None
        self.filtered_df = None
    
    def connect(self) -> None:
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            print("Connexion à la base de données établie avec succès")
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")
    
    def check_table_exists(self, table_name: str) -> bool:
        """Vérifie si une table existe dans la base de données"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT count(*) FROM sqlite_master 
                WHERE type='table' AND name='{table_name}'
            """)
            return cursor.fetchone()[0] > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la vérification de la table: {e}")
            return False
    
    def clear_table(self, table_name: str) -> bool:
        """Vide le contenu de la table sans la supprimer"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {table_name}")
            self.connection.commit()
            print(f"✅ Table {table_name} vidée")
            return True
        except sqlite3.Error as e:
            print(f"❌ Erreur lors du vidage de la table: {e}")
            return False
    
    def execute_query(self) -> Optional[pd.DataFrame]:
        """
        Exécute la requête SQL et retourne un DataFrame avec le même schéma
        """
        if not self.connection:
            self.connect()
        
        try:
            # Requête SQL pour récupérer les données filtrées
            query = f"""
            SELECT *
            FROM {self.table_source}
            WHERE is_connected_sewage = 1
            AND overconsumption_per_capita IS NOT NULL
            """
            
            # Lecture des données dans un DataFrame
            df = pd.read_sql_query(query, self.connection)
            
            # Vérification que le schéma est identique
            schema_query = f"PRAGMA table_info({self.table_source});"
            schema_info = pd.read_sql_query(schema_query, self.connection)
            original_columns = schema_info['name'].tolist()
            
            # Vérification que toutes les colonnes sont présentes
            if set(df.columns) == set(original_columns):
                print("✅ Le DataFrame a le même schéma que la table originale")
                self.filtered_df = df
                return df
            else:
                print("❌ Attention: le schéma du DataFrame diffère de la table originale")
                missing_cols = set(original_columns) - set(df.columns)
                extra_cols = set(df.columns) - set(original_columns)
                print(f"Colonnes manquantes: {missing_cols}")
                print(f"Colonnes supplémentaires: {extra_cols}")
                return None
                
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            return None
    
    def save_to_database(self) -> bool:
        """
        Insère les données dans la table cible existante
        """
        if self.filtered_df is None or self.filtered_df.empty:
            print("❌ Aucune donnée à sauvegarder en base")
            return False
        
        try:
            # Vérification si la table cible existe
            if not self.check_table_exists(self.table_cible):
                print(f"❌ La table {self.table_cible} n'existe pas")
                return False
            
            # Vidage de la table avant insertion des nouvelles données
            if not self.clear_table(self.table_cible):
                return False
            
            # Insertion des données dans la table existante
            self.filtered_df.to_sql(
                name=self.table_cible,
                con=self.connection,
                if_exists='append',  # Ajoute les données à la table existante
                index=False
            )
            print(f"✅ Données insérées dans la table: {self.table_cible}")
            print(f"✅ {len(self.filtered_df)} lignes ajoutées")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion en base: {e}")
            return False
    
    def get_filtered_data(self) -> Optional[pd.DataFrame]:
        """Retourne le DataFrame filtré"""
        return self.filtered_df
    
    def get_stats(self) -> None:
        """Affiche les statistiques descriptives des données filtrées"""
        if self.filtered_df is not None:
            print("📊 Statistiques des données filtrées:")
            print(f"Nombre de lignes: {len(self.filtered_df)}")
            print(f"Nombre de colonnes: {len(self.filtered_df.columns)}")
            print(f"Table source: {self.table_source}")
            print(f"Table cible: {self.table_cible}")
            print("\nAperçu des données:")
            print(self.filtered_df.head())
        else:
            print("❌ Aucune donnée disponible pour les statistiques")

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialisation de la classe
    splitter = CarIncitSplitG2()
    
    try:
        # Exécution de la requête
        df_filtered = splitter.execute_query()
        
        if df_filtered is not None:
            # Affichage des statistiques
            splitter.get_stats()
            
            # Sauvegarde en base de données
            success = splitter.save_to_database()
            
            if success:
                print("✅ Opération terminée avec succès!")
            else:
                print("❌ Erreur lors de la sauvegarde")
        else:
            print("❌ Aucune donnée filtrée à sauvegarder")
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    finally:
        # Fermeture de la connexion
        splitter.disconnect()