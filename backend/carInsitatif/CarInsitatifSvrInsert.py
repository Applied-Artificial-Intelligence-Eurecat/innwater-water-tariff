import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np

class CarInsitatifSvrInsert:
    def __init__(self, db_path: str):
        """
        Initialise la classe avec le chemin de la base de données
        
        Args:
            db_path (str): Chemin vers le fichier de base de données SQLite
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self) -> None:
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Valide le DataFrame avant insertion selon les contraintes de la table
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données à insérer
            
        Returns:
            bool: True si le DataFrame est valide, False sinon
        """
        required_columns = [
            'household_id', 'is_connected_sewage', 'is_poor_household',
            'household_size', 'household_income', 'water_consumption_tbse',
            'water_consumption_ibt_pp', 'water_consumption_ibt',
            'overconsumption_volume', 'is_overconsuming',
            'overconsumption_per_capita', 'bill_amount_ibt',
            'bill_amount_ibt_pp', 'bill_amount_tbse',
            'overconsumption_expenditure', 'per_capita'
        ]
        
        # Vérification des colonnes requises
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            print(f"Colonnes manquantes: {missing_columns}")
            return False
        
        # Vérification des types de données et contraintes
        try:
            # Vérification des valeurs binaires (0 ou 1)
            binary_columns = ['is_connected_sewage', 'is_poor_household', 'is_overconsuming']
            for col in binary_columns:
                if not df[col].isin([0, 1]).all():
                    print(f"Colonne {col} contient des valeurs autres que 0 ou 1")
                    return False
            
            # Vérification des valeurs entières positives strictes
            if (df['household_size'] <= 0).any():
                print("Colonne household_size contient des valeurs <= 0")
                return False
            
            # Vérification des valeurs numériques non négatives
            non_negative_columns = [
                'household_income', 'water_consumption_tbse',
                'water_consumption_ibt_pp', 'water_consumption_ibt',
                'overconsumption_volume', 'overconsumption_per_capita',
                'bill_amount_ibt', 'bill_amount_ibt_pp', 'bill_amount_tbse',
                'overconsumption_expenditure', 'per_capita'
            ]
            
            for col in non_negative_columns:
                if (df[col] < 0).any():
                    print(f"Colonne {col} contient des valeurs négatives")
                    return False
            
            # Vérification des valeurs manquantes
            if df[required_columns].isnull().any().any():
                print("Le DataFrame contient des valeurs manquantes dans les colonnes requises")
                return False
                
        except Exception as e:
            print(f"Erreur lors de la validation: {e}")
            return False
        
        return True
    
    def prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare le DataFrame pour l'insertion en convertissant les types de données
        
        Args:
            df (pd.DataFrame): DataFrame à préparer
            
        Returns:
            pd.DataFrame: DataFrame préparé
        """
        # Faire une copie pour éviter de modifier l'original
        df_prepared = df.copy()
        
        # Convertir les colonnes binaires en int
        binary_columns = ['is_connected_sewage', 'is_poor_household', 'is_overconsuming']
        for col in binary_columns:
            if col in df_prepared.columns:
                df_prepared[col] = df_prepared[col].astype(int)
        
        # S'assurer que household_size est entier
        if 'household_size' in df_prepared.columns:
            df_prepared['household_size'] = df_prepared['household_size'].astype(int)
        
        # S'assurer que household_id est entier
        if 'household_id' in df_prepared.columns:
            df_prepared['household_id'] = df_prepared['household_id'].astype(int)
        
        # Remplacer les NaN par None pour SQLite
        df_prepared = df_prepared.replace({np.nan: None})
        
        return df_prepared
    
    def insert_dataframe(self, df: pd.DataFrame, batch_size: int = 1000) -> List[Optional[int]]:
        """
        Insère les données d'un DataFrame dans la table carInsitatifdataintermed
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données à insérer
            batch_size (int): Taille des lots pour l'insertion (optimisation mémoire)
            
        Returns:
            List[Optional[int]]: Liste des IDs des enregistrements insérés
        """
        if df.empty:
            print("Le DataFrame est vide")
            return []
        
        if not self.validate_dataframe(df):
            print("DataFrame invalide - vérifiez les contraintes du schéma")
            return []
        
        try:
            # Préparer le DataFrame
            df_prepared = self.prepare_dataframe(df)
            
            self.connect()
            
            query = """
            INSERT INTO carInsitatifdataintermed (
                household_id, is_connected_sewage, is_poor_household,
                household_size, household_income, water_consumption_tbse,
                water_consumption_ibt_pp, water_consumption_ibt,
                overconsumption_volume, is_overconsuming,
                overconsumption_per_capita, bill_amount_ibt,
                bill_amount_ibt_pp, bill_amount_tbse,
                overconsumption_expenditure, per_capita
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            inserted_ids = []
            total_records = len(df_prepared)
            
            # Insertion par lots pour optimiser la mémoire
            for i in range(0, total_records, batch_size):
                batch = df_prepared.iloc[i:i + batch_size]
                batch_size_current = len(batch)
                
                # Convertir le batch en liste de tuples
                records = []
                for _, row in batch.iterrows():
                    record = (
                        int(row['household_id']), 
                        int(row['is_connected_sewage']), 
                        int(row['is_poor_household']),
                        int(row['household_size']), 
                        float(row['household_income']), 
                        float(row['water_consumption_tbse']),
                        float(row['water_consumption_ibt_pp']), 
                        float(row['water_consumption_ibt']),
                        float(row['overconsumption_volume']), 
                        int(row['is_overconsuming']),
                        float(row['overconsumption_per_capita']), 
                        float(row['bill_amount_ibt']),
                        float(row['bill_amount_ibt_pp']), 
                        float(row['bill_amount_tbse']),
                        float(row['overconsumption_expenditure']), 
                        float(row['per_capita'])
                    )
                    records.append(record)
                
                # Exécuter l'insertion du lot
                self.cursor.executemany(query, records)
                
                # Récupérer le dernier ID inséré
                last_id = self.cursor.lastrowid
                
                # Calculer les IDs pour ce lot
                if last_id is not None:
                    batch_ids = list(range(last_id - batch_size_current + 1, last_id + 1))
                    inserted_ids.extend(batch_ids)
                
                print(f"Lot {i//batch_size + 1} inséré: {batch_size_current} enregistrements")
            
            self.connection.commit()
            print(f"Total de {len(inserted_ids)} enregistrement(s) inséré(s) avec succès")
            
            return inserted_ids
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de l'insertion: {e}")
            if self.connection:
                self.connection.rollback()
            return []
        except Exception as e:
            print(f"Erreur inattendue lors de l'insertion: {e}")
            if self.connection:
                self.connection.rollback()
            return []
        finally:
            self.disconnect()
    
    def get_table_info(self) -> None:
        """
        Affiche les informations sur la structure de la table
        """
        try:
            self.connect()
            self.cursor.execute("PRAGMA table_info(carInsitatifdataintermed)")
            columns = self.cursor.fetchall()
            
            print("Structure de la table carInsitatifdataintermed:")
            print("-" * 80)
            for col in columns:
                print(f"Colonne: {col[1]}, Type: {col[2]}, Nullable: {not col[3]}, PK: {col[5]}")
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations de la table: {e}")
        finally:
            self.disconnect()

# Exemple d'utilisation avec DataFrame
if __name__ == "__main__":
    # Initialisation de la classe
    db_insert = CarInsitatifSvrInsert("database.db")
    
    # Afficher les informations de la table
    db_insert.get_table_info()
    
    # Création d'un DataFrame d'exemple conforme au schéma
    data = {
        'household_id': [12345, 12346, 12347],
        'is_connected_sewage': [1, 1, 0],
        'is_poor_household': [0, 1, 1],
        'household_size': [4, 2, 3],
        'household_income': [2500.50, 1200.0, 800.75],
        'water_consumption_tbse': [25.0, 15.5, 12.0],
        'water_consumption_ibt_pp': [6.25, 7.75, 4.0],
        'water_consumption_ibt': [25.0, 15.5, 12.0],
        'overconsumption_volume': [5.0, 0.0, 0.0],
        'is_overconsuming': [1, 0, 0],
        'overconsumption_per_capita': [1.25, 0.0, 0.0],
        'bill_amount_ibt': [45.75, 25.3, 18.5],
        'bill_amount_ibt_pp': [11.44, 12.65, 6.17],
        'bill_amount_tbse': [40.0, 25.3, 18.5],
        'overconsumption_expenditure': [5.75, 0.0, 0.0],
        'per_capita': [625.125, 600.0, 266.92]
    }
    
    df = pd.DataFrame(data)
    
    # Insertion du DataFrame
    inserted_ids = db_insert.insert_dataframe(df, batch_size=100)
    print(f"IDs des enregistrements insérés: {inserted_ids}")