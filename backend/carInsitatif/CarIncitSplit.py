import pandas as pd
import sqlite3
from typing import Optional

class CarIncitSplit:
    def __init__(self):
        """
        Initialise la classe avec la base de données database.db
        """
        self.db_path = "database.db"
        self.table_source = "carInsitatifdataintermed"
        self.table_cible = "carInsitatifdataintermedG1"
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
    
    def execute_query(self) -> Optional[pd.DataFrame]:
        """
        Exécute la requête SQL et retourne un DataFrame avec le même schéma
        
        Returns:
            pd.DataFrame: DataFrame filtré avec le même schéma que la table originale
        """
        if not self.connection:
            self.connect()
        
        try:
            # Requête SQL pour récupérer les données filtrées
            query = f"""
            SELECT *
            FROM {self.table_source}
            WHERE is_connected_sewage = 0
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
                return None
                
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            return None
    
    def save_to_database(self) -> bool:
        """
        Sauvegarde le DataFrame filtré dans la table cible de la base de données
        
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        if self.filtered_df is not None:
            try:
                # Sauvegarde dans la table cible
                self.filtered_df.to_sql(
                    name=self.table_cible,
                    con=self.connection,
                    if_exists='replace',  # Remplace la table si elle existe
                    index=False
                )
                print(f"✅ Données sauvegardées dans la table: {self.table_cible}")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde en base: {e}")
                return False
        else:
            print("❌ Aucune donnée à sauvegarder en base")
            return False
    
    def get_filtered_data(self) -> Optional[pd.DataFrame]:
        """
        Retourne le DataFrame filtré
        
        Returns:
            pd.DataFrame: Données filtrées ou None si non disponible
        """
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
    splitter = CarIncitSplit()
    
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
            
    finally:
        # Fermeture de la connexion
        splitter.disconnect()