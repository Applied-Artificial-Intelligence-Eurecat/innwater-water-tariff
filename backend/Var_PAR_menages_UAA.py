import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Union
import os
import sqlite3

class Var_PAR_menages_UAA:
    """
    Classe pour créer et gérer des DataFrames avec la structure spécifique
    du fichier Var_PAR_menages_UAA.xls et interagir avec une base de données SQLite
    """
    
    def __init__(self):
        self.columns = [
            'id_projet', 'menage', 'a_t0_ibt', 'a_tmin_ibt', 'a_t_ibt',
            'a_t_ibt_pp', 'a_t0_tbse', 'a_tmin_tbse', 'a_t_tbse'
        ]
        self.table_name = "Var_PAR_menages_UAA"
        self.database_name = "database.db"
    
    def create_dataframe(self, n_rows: int = 10, random_data: bool = False) -> pd.DataFrame:
        """
        Crée un DataFrame avec la structure demandée
        
        Args:
            n_rows: Nombre de lignes à créer
            random_data: Si True, génère des données aléatoires, sinon des données par défaut
            
        Returns:
            pd.DataFrame: DataFrame avec la structure spécifiée
        """
        data = {}
        
        # Colonne id_projet
        data['id_projet'] = [f'PROJ_{i:03d}' for i in range(1, n_rows + 1)]
        
        # Colonne menage
        data['menage'] = [f'MEN_{i:03d}' for i in range(1, n_rows + 1)]
        
        if random_data:
            # Données aléatoires pour les autres colonnes
            np.random.seed(42)  # Pour la reproductibilité
            data['a_t0_ibt'] = np.random.uniform(1000, 5000, n_rows).round(2)
            data['a_tmin_ibt'] = np.random.uniform(500, 2500, n_rows).round(2)
            data['a_t_ibt'] = np.random.uniform(800, 4000, n_rows).round(2)
            data['a_t_ibt_pp'] = np.random.uniform(700, 3500, n_rows).round(2)
            data['a_t0_tbse'] = np.random.uniform(2000, 10000, n_rows).round(2)
            data['a_tmin_tbse'] = np.random.uniform(1000, 5000, n_rows).round(2)
            data['a_t_tbse'] = np.random.uniform(1500, 7500, n_rows).round(2)
        else:
            # Données par défaut (valeurs nulles ou par défaut)
            data['a_t0_ibt'] = [0.0] * n_rows
            data['a_tmin_ibt'] = [0.0] * n_rows
            data['a_t_ibt'] = [0.0] * n_rows
            data['a_t_ibt_pp'] = [0.0] * n_rows
            data['a_t0_tbse'] = [0.0] * n_rows
            data['a_tmin_tbse'] = [0.0] * n_rows
            data['a_t_tbse'] = [0.0] * n_rows
        
        return pd.DataFrame(data, columns=self.columns)
    
    def read_excel_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Lit le fichier Excel Var_PAR_menages_UAA.xls et crée un DataFrame avec la structure demandée
        Les données sont toujours dans la première feuille (feuille 1)
        
        Args:
            file_path: Chemin vers le fichier Excel
            **kwargs: Arguments supplémentaires pour pd.read_excel()
            
        Returns:
            pd.DataFrame: DataFrame avec la structure spécifiée
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le fichier ne contient pas les colonnes requises
        """
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas")
        
        try:
            # Lire le fichier Excel - toujours la première feuille (index 0)
            df_excel = pd.read_excel(file_path, sheet_name=0, **kwargs)
            
            # Vérifier que toutes les colonnes requises sont présentes
            missing_columns = set(self.columns) - set(df_excel.columns)
            if missing_columns:
                raise ValueError(f"Colonnes manquantes dans le fichier Excel: {missing_columns}")
            
            # Sélectionner et réorganiser les colonnes dans l'ordre souhaité
            df_final = df_excel[self.columns].copy()
            
            # Nettoyer les données
            df_final = self._clean_data(df_final)
            
            return df_final
            
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier Excel: {str(e)}")
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie les données du DataFrame (méthode interne)
        
        Args:
            df: DataFrame à nettoyer
            
        Returns:
            pd.DataFrame: DataFrame nettoyé
        """
        df_clean = df.copy()
        
        # Remplacer les valeurs NaN par 0 pour les colonnes numériques
        numeric_columns = [col for col in self.columns if col not in ['id_projet', 'menage']]
        df_clean[numeric_columns] = df_clean[numeric_columns].fillna(0)
        
        # S'assurer que les types de données sont corrects
        df_clean['id_projet'] = df_clean['id_projet'].astype(str)
        df_clean['menage'] = df_clean['menage'].astype(str)
        
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
        
        return df_clean
    
    def create_from_dict(self, data_dict: Dict) -> pd.DataFrame:
        """
        Crée un DataFrame à partir d'un dictionnaire de données
        
        Args:
            data_dict: Dictionnaire avec les données pour chaque colonne
            
        Returns:
            pd.DataFrame: DataFrame avec la structure spécifiée
        """
        # Vérification que toutes les colonnes sont présentes
        for col in self.columns:
            if col not in data_dict:
                raise ValueError(f"La colonne '{col}' est manquante dans le dictionnaire")
        
        return pd.DataFrame(data_dict, columns=self.columns)
    
    def get_column_info(self) -> Dict:
        """
        Retourne des informations sur les colonnes du DataFrame
        
        Returns:
            Dict: Dictionnaire avec les descriptions des colonnes
        """
        column_descriptions = {
            'id_projet': 'Identifiant unique du projet',
            'menage': 'Identifiant du ménage associé au projet',
            'a_t0_ibt': 'Montant initial IBTE (Indicateur Budget Temps)',
            'a_tmin_ibt': 'Montant minimum IBTE',
            'a_t_ibt': 'Montant actuel IBTE',
            'a_t_ibt_pp': 'Montant IBTE prévisionnel',
            'a_t0_tbse': 'Montant initial TBSE (autre indicateur)',
            'a_tmin_tbse': 'Montant minimum TBSE',
            'a_t_tbse': 'Montant actuel TBSE'
        }
        
        return column_descriptions
    
    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Valide qu'un DataFrame a la structure correcte
        
        Args:
            df: DataFrame à valider
            
        Returns:
            bool: True si le DataFrame est valide
        """
        return all(col in df.columns for col in self.columns)
    
    def save_to_excel(self, df: pd.DataFrame, file_path: str, **kwargs) -> None:
        """
        Sauvegarde le DataFrame dans un fichier Excel
        
        Args:
            df: DataFrame à sauvegarder
            file_path: Chemin du fichier de sortie
            **kwargs: Arguments supplémentaires pour pd.DataFrame.to_excel()
        """
        if not self.validate_dataframe(df):
            raise ValueError("Le DataFrame n'a pas la structure requise")
        
        df.to_excel(file_path, index=False, **kwargs)
        print(f"DataFrame sauvegardé avec succès dans {file_path}")
    
    def create_database_table(self, db_path: Optional[str] = None) -> None:
        """
        Crée la table Var_PAR_menages_UAA dans la base de données SQLite
        
        Args:
            db_path: Chemin vers la base de données (optionnel)
                    Si non spécifié, utilise self.database_name
        """
        if db_path is None:
            db_path = self.database_name
        
        # Définition du schéma de la table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id_projet TEXT PRIMARY KEY,
            menage TEXT NOT NULL,
            a_t0_ibt REAL DEFAULT 0,
            a_tmin_ibt REAL DEFAULT 0,
            a_t_ibt REAL DEFAULT 0,
            a_t_ibt_pp REAL DEFAULT 0,
            a_t0_tbse REAL DEFAULT 0,
            a_tmin_tbse REAL DEFAULT 0,
            a_t_tbse REAL DEFAULT 0
        )
        """
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Création de la table
            cursor.execute(create_table_query)
            conn.commit()
            
            print(f"Table '{self.table_name}' créée avec succès dans la base de données '{db_path}'")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la création de la table: {e}")
        except Exception as e:
            print(f"Erreur lors de la création de la table: {e}")
        finally:
            if conn:
                conn.close()
    
    def insert_dataframe_to_db(self, df: pd.DataFrame, db_path: Optional[str] = None) -> None:
        """
        Insère les données d'un DataFrame dans la table de la base de données
        
        Args:
            df: DataFrame à insérer
            db_path: Chemin vers la base de données (optionnel)
        """
        if not self.validate_dataframe(df):
            raise ValueError("Le DataFrame n'a pas la structure requise")
        
        if db_path is None:
            db_path = self.database_name
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            
            # Insertion des données
            df.to_sql(self.table_name, conn, if_exists='append', index=False)
            
            print(f"Données insérées avec succès dans la table '{self.table_name}'")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de l'insertion des données: {e}")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données: {e}")
        finally:
            if conn:
                conn.close()
    
    def read_from_db(self, db_path: Optional[str] = None) -> pd.DataFrame:
        """
        Lit toutes les données de la table de la base de données
        
        Args:
            db_path: Chemin vers la base de données (optionnel)
            
        Returns:
            pd.DataFrame: DataFrame avec les données de la table
        """
        if db_path is None:
            db_path = self.database_name
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            
            # Lecture des données
            query = f"SELECT * FROM {self.table_name}"
            df = pd.read_sql(query, conn)
            
            return df
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la lecture des données: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Erreur lors de la lecture des données: {e}")
            return pd.DataFrame()
        finally:
            if conn:
                conn.close()

    def update_varparmenageresult_table(self, df: pd.DataFrame, db_path: Optional[str] = None) -> None:
        """
        Met à jour les colonnes appropriées de la table VarParMenageResult
        avec les données du DataFrame en faisant le matching sur id_projet et menage.
        
        Args:
            df: DataFrame contenant les données à mettre à jour
            db_path: Chemin vers la base de données (optionnel)
        """
        if not self.validate_dataframe(df):
            raise ValueError("Le DataFrame n'a pas la structure requise")
        
        if db_path is None:
            db_path = self.database_name
        
        # Mapping des colonnes entre les deux tables
        column_mapping = {
            'a_t0_ibt': 'a_t0_ibt',
            'a_tmin_ibt': 'a_tmin_ibt',
            'a_t_ibt': 'a_t_ibt',
            'a_t_ibt_pp': 'a_t_ibt_pp',
            'a_t0_tbse': 'a_t0_tbse',
            'a_tmin_tbse': 'a_tmin_tbse',
            'a_t_tbse': 'a_t_tbse'
        }
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Préparer la requête de mise à jour
            update_columns = []
            for source_col, target_col in column_mapping.items():
                update_columns.append(f"{target_col} = ?")
            
            update_query = f"""
            UPDATE VarParMenageResult 
            SET {', '.join(update_columns)}
            WHERE id_projet = ? AND menage = ?
            """
            
            # Parcourir chaque ligne du DataFrame et mettre à jour la table
            for _, row in df.iterrows():
                # Préparer les valeurs pour la mise à jour
                update_values = [row[source_col] for source_col in column_mapping.keys()]
                
                # Ajouter les conditions WHERE
                update_values.extend([row['id_projet'], row['menage']])
                
                # Exécuter la mise à jour
                cursor.execute(update_query, update_values)
            
            conn.commit()
            print(f"Mise à jour réussie de {len(df)} enregistrement(s) dans la table VarParMenageResult")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la mise à jour: {e}")
            conn.rollback()
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            conn.rollback()
        finally:
            if conn:
                conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance de la classe
    var_par_menages = Var_PAR_menages_UAA()
    
    # Exemple 2: Lecture du fichier Excel Var_PAR_menages_UAA.xls (première feuille automatiquement)
    print("\nExemple 2: Lecture du fichier Var_PAR_menages_UAA.xls (feuille 1 automatique)")
    try:
        file_path = "Var_PAR_menages_UAA.xls"
        df_excel = var_par_menages.read_excel_file(file_path)
        print(f"DataFrame lu depuis {file_path} (feuille 1):")
        print(df_excel.head())
        print(f"\nNombre de lignes: {len(df_excel)}")
        
    except FileNotFoundError:
        print(f"Fichier '{file_path}' non trouvé. Veuillez vérifier le chemin.")
    except Exception as e:
        print(f"Erreur lors de la lecture: {e}")
    
      # Exemple 6: Mise à jour de la table VarParMenageResult
    print("\nExemple 6: Mise à jour de la table VarParMenageResult")
    var_par_menages.update_varparmenageresult_table(df_excel)
    
    # # Exemple 3: Création de la table dans la base de données
    # print("\nExemple 3: Création de la table dans la base de données")
    # var_par_menages.create_database_table()
    
    # # Exemple 4: Insertion des données dans la base de données
    # print("\nExemple 4: Insertion des données dans la base de données")
    # var_par_menages.insert_dataframe_to_db(df_random)
    
    # # Exemple 5: Lecture des données depuis la base de données
    # print("\nExemple 5: Lecture des données depuis la base de données")
    # df_from_db = var_par_menages.read_from_db()
    # print("Données lues depuis la base de données:")
    # print(df_from_db)