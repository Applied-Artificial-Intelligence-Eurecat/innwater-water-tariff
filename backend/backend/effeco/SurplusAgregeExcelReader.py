import pandas as pd
import numpy as np
import sqlite3
from typing import Optional

class SurplusAgregeExcelReader:
    """
    Classe pour lire le fichier Excel surplusagrege.xls et créer un DataFrame
    avec le schéma spécifique des données de surplus agrégé.
    """
    
    def __init__(self, file_path: str = "surplusagrege.xls", db_path: str = "database.db"):
        """
        Initialise le lecteur de fichier Excel et la connexion à la base de données.
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            db_path (str): Chemin vers la base de données SQLite
        """
        self.file_path = file_path
        self.db_path = db_path
        self.dataframe = None
        self.connection = None
    
    def connect_to_database(self) -> bool:
        """
        Établit une connexion à la base de données SQLite.
        
        Returns:
            bool: True si la connexion a réussi, False sinon
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            print(f"Connexion à la base de données {self.db_path} établie avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")
            return False
    
    def disconnect_from_database(self) -> None:
        """
        Ferme la connexion à la base de données.
        """
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")
    
    def save_to_database(self, df: pd.DataFrame, table_name: str = "surplus_agrege") -> bool:
        """
        Sauvegarde le DataFrame dans la base de données.
        
        Args:
            df (pd.DataFrame): DataFrame à sauvegarder
            table_name (str): Nom de la table de destination
            
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        if not self.connection:
            print("Aucune connexion à la base de données")
            return False
        
        try:
            # Sauvegarder le DataFrame dans la base de données
            df.to_sql(table_name, self.connection, if_exists='replace', index=False)
            print(f"Données sauvegardées dans la table '{table_name}' avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde dans la base de données: {e}")
            return False
    
    def read_excel_file(self, sheet_name: str = None, **kwargs) -> pd.DataFrame:
        """
        Lit le fichier Excel et retourne un DataFrame.
        
        Args:
            sheet_name (str): Nom de la feuille à lire (None pour la première)
            **kwargs: Arguments additionnels pour pd.read_excel()
            
        Returns:
            pd.DataFrame: DataFrame contenant les données
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            Exception: Pour autres erreurs de lecture
        """
        try:
            # Paramètres optimisés pour fichier .xls avec une seule feuille
            read_params = {
                'header': 0,  # Première ligne comme en-têtes
                'engine': 'xlrd',  # Moteur pour les fichiers .xls
            }
            
            # Ajouter sheet_name seulement s'il est spécifié
            if sheet_name is not None:
                read_params['sheet_name'] = sheet_name
            
            # Mettre à jour avec les paramètres fournis
            read_params.update(kwargs)
            
            print(f"Lecture du fichier Excel: {self.file_path}")
            df = pd.read_excel(self.file_path, **read_params)
            
            print(f"Fichier lu avec succès. Dimensions: {df.shape}")
            return df
            
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier Excel: {e}")
            raise


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une instance du lecteur
    reader = SurplusAgregeExcelReader("surplusagrege.xls", "database.db")
    
    try:
        # Connexion à la base de données
        if reader.connect_to_database():
            # Lire le fichier Excel
            df = reader.read_excel_file()
            
            # Afficher les premières lignes
            print("\n=== PREMIÈRES LIGNES ===")
            print(df.head())
            
            # Afficher les informations de base
            print("\n=== INFORMATIONS DE BASE ===")
            print(f"Dimensions: {df.shape}")
            print(f"Colonnes: {list(df.columns)}")
            
            # Sauvegarder dans la base de données
            if reader.save_to_database(df):
                print("\n=== SAUVEGARDE RÉUSSIE ===")
                print("Les données ont été sauvegardées dans la base de données")
            
            # Fermer la connexion à la base de données
            reader.disconnect_from_database()
        
    except Exception as e:
        print(f"Erreur: {e}")
        # S'assurer que la connexion est fermée même en cas d'erreur
        if reader.connection:
            reader.disconnect_from_database()