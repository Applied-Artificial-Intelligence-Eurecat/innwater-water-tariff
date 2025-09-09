import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import warnings
import sqlite3
import os

class VARCARMENAGEV3_excel_loader:
    """
    Classe pour lire un fichier Excel contenant des données de projet
    et construire un DataFrame avec un schéma spécifique.
    """
    
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        """
        Initialise le lecteur Excel.
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            sheet_name (str, optional): Nom de la feuille à lire. 
                                      Si None, lit la première feuille.
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.df = None
        
        # Définition du schéma attendu
        self.expected_columns = [
            'id_projet', 'menage', 'tailledelafamille', 'nbreenfants', 'nbreadultes',
            'revenunetmois', 'ucoxford', 'ucocde', 'niveaudevieoxford', 'niveaudevieocde',
            'poor_oxford', 'poor_ocde', 'assaini', 'sep_t0_ibt_ep', 'sep_tmin_ibt_ep',
            'sep_t_ibt_ep', 'sep_t_ibt_pp_ep', 'sep_t0_tbse_ep', 'sep_tmin_tbse_ep',
            'sep_t_tbse_ep', 'a_t0_ibt', 'a_tmin_ibt', 'a_t_ibt', 'a_t_ibt_pp',
            'a_t0_tbse', 'a_tmin_tbse', 'a_t_tbse', 'sepa_t0_ibt', 'sepa_tmin_ibt',
            'sepa_t_ibt', 'sepa_t_ibt_pp', 'sepa_t0_tbse', 'sepa_tmin_tbse',
            'sepa_t_tbse', 'car_ibt', 'car_tbse', 'car_ibt_1', 'car_tbse_1',
            'car_ibt_2', 'car_tbse_2', 'car_ibt_3', 'car_tbse_3',
            'seuil_depenses_trim_par_pct_3_r', 'exces_dep_0_inclus_ibt', 'exces_dep_0_inclus_tbse'
        ]
        
        # Types de données pour chaque colonne
        self.column_types = {
            'id_projet': 'object',
            'menage': 'object',
            'tailledelafamille': 'int64',
            'nbreenfants': 'int64',
            'nbreadultes': 'int64',
            'revenunetmois': 'float64',
            'ucoxford': 'float64',
            'ucocde': 'float64',
            'niveaudevieoxford': 'float64',
            'niveaudevieocde': 'float64',
            'poor_oxford': 'int64',
            'poor_ocde': 'int64',
            'assaini': 'int64'
        }
        
        # Les autres colonnes sont par défaut en float64
        for col in self.expected_columns:
            if col not in self.column_types:
                self.column_types[col] = 'float64'
    
    def read_excel(self) -> pd.DataFrame:
        """
        Lit le fichier Excel et retourne un DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame avec les données du fichier Excel
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le fichier ne contient pas les colonnes attendues
        """
        try:
            # Lecture du fichier Excel
            if self.sheet_name:
                self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            else:
                self.df = pd.read_excel(self.file_path)
            
            # Nettoyage des noms de colonnes (suppression des espaces)
            self.df.columns = self.df.columns.str.strip()
            
            # Vérification des colonnes
            self._validate_columns()
            
            # Application des types de données
            self._apply_data_types()
            
            # Nettoyage des données
            self._clean_data()
            
            return self.df
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier {self.file_path} n'a pas été trouvé.")
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier: {str(e)}")
    
    def _validate_columns(self):
        """Valide que toutes les colonnes attendues sont présentes."""
        missing_columns = set(self.expected_columns) - set(self.df.columns)
        if missing_columns:
            warnings.warn(f"Colonnes manquantes: {missing_columns}")
            # Ajout des colonnes manquantes avec des valeurs NaN
            for col in missing_columns:
                self.df[col] = np.nan
        
        # Réorganiser les colonnes dans l'ordre attendu
        self.df = self.df[self.expected_columns]
    
    def _apply_data_types(self):
        """Applique les types de données aux colonnes."""
        for col, dtype in self.column_types.items():
            if col in self.df.columns:
                try:
                    if dtype in ['int64']:
                        # Conversion en entier avec gestion des NaN
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                        self.df[col] = self.df[col].astype('Int64')  # Type nullable
                    elif dtype == 'float64':
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    else:
                        self.df[col] = self.df[col].astype(dtype)
                except Exception as e:
                    warnings.warn(f"Impossible de convertir la colonne {col} en {dtype}: {e}")
    
    def _clean_data(self):
        """Nettoie les données du DataFrame."""
        # Suppression des lignes complètement vides
        self.df = self.df.dropna(how='all')
        
        # Réinitialisation de l'index
        self.df = self.df.reset_index(drop=True)
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        Retourne des informations sur les données.
        
        Returns:
            dict: Informations sur le DataFrame
        """
        if self.df is None:
            return {"error": "Aucune donnée chargée. Utilisez read_excel() d'abord."}
        
        return {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "memory_usage": self.df.memory_usage(deep=True).sum()
        }
    
    def get_summary_stats(self) -> pd.DataFrame:
        """
        Retourne des statistiques descriptives sur les colonnes numériques.
        
        Returns:
            pd.DataFrame: Statistiques descriptives
        """
        if self.df is None:
            raise ValueError("Aucune donnée chargée. Utilisez read_excel() d'abord.")
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_columns].describe()
    
    def export_to_csv(self, output_path: str, **kwargs):
        """
        Exporte le DataFrame vers un fichier CSV.
        
        Args:
            output_path (str): Chemin de sortie pour le fichier CSV
            **kwargs: Arguments additionnels pour pandas.to_csv()
        """
        if self.df is None:
            raise ValueError("Aucune donnée chargée. Utilisez read_excel() d'abord.")
        
        self.df.to_csv(output_path, index=False, **kwargs)
        print(f"Données exportées vers {output_path}")
    
    def create_database_table(self, db_path: str = "database.db"):
        """
        Crée une table VarCarMenageResult dans la base de données SQLite.
        Supprime la table si elle existe déjà et la recrée.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
        """
        if self.df is None:
            raise ValueError("Aucune donnée chargée. Utilisez read_excel() d'abord.")
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Suppression de la table si elle existe
            cursor.execute("DROP TABLE IF EXISTS VarCarMenageResult")
            
            # Création de la table avec le schéma approprié
            create_table_sql = """
            CREATE TABLE VarCarMenageResult (
                id_projet TEXT,
                menage TEXT,
                tailledelafamille INTEGER,
                nbreenfants INTEGER,
                nbreadultes INTEGER,
                revenunetmois REAL,
                ucoxford REAL,
                ucocde REAL,
                niveaudevieoxford REAL,
                niveaudevieocde REAL,
                poor_oxford INTEGER,
                poor_ocde INTEGER,
                assaini INTEGER,
                sep_t0_ibt_ep REAL,
                sep_tmin_ibt_ep REAL,
                sep_t_ibt_ep REAL,
                sep_t_ibt_pp_ep REAL,
                sep_t0_tbse_ep REAL,
                sep_tmin_tbse_ep REAL,
                sep_t_tbse_ep REAL,
                a_t0_ibt REAL,
                a_tmin_ibt REAL,
                a_t_ibt REAL,
                a_t_ibt_pp REAL,
                a_t0_tbse REAL,
                a_tmin_tbse REAL,
                a_t_tbse REAL,
                sepa_t0_ibt REAL,
                sepa_tmin_ibt REAL,
                sepa_t_ibt REAL,
                sepa_t_ibt_pp REAL,
                sepa_t0_tbse REAL,
                sepa_tmin_tbse REAL,
                sepa_t_tbse REAL,
                car_ibt REAL,
                car_tbse REAL,
                car_ibt_1 REAL,
                car_tbse_1 REAL,
                car_ibt_2 REAL,
                car_tbse_2 REAL,
                car_ibt_3 REAL,
                car_tbse_3 REAL,
                seuil_depenses_trim_par_pct_3_r REAL,
                exces_dep_0_inclus_ibt REAL,
                exces_dep_0_inclus_tbse REAL
            )
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            
            print(f"Table VarCarMenageResult créée avec succès dans {db_path}")
            print(f"Nombre de colonnes: {len(self.expected_columns)}")
            
        except Exception as e:
            print(f"Erreur lors de la création de la table: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def insert_data_to_database(self, db_path: str = "database.db", if_exists: str = 'replace'):
        """
        Insère les données du DataFrame dans la table VarCarMenageResult.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
            if_exists (str): Que faire si la table existe ('fail', 'replace', 'append')
        """
        if self.df is None:
            raise ValueError("Aucune donnée chargée. Utilisez read_excel() d'abord.")
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            
            # Insertion des données
            self.df.to_sql('VarCarMenageResult', conn, if_exists=if_exists, index=False)
            
            # Vérification du nombre d'enregistrements insérés
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM VarCarMenageResult")
            count = cursor.fetchone()[0]
            
            print(f"Données insérées avec succès dans la table VarCarMenageResult")
            print(f"Nombre d'enregistrements: {count}")
            
        except Exception as e:
            print(f"Erreur lors de l'insertion des données: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def load_and_store_to_database(self, db_path: str = "database.db"):
        """
        Méthode complète qui lit le fichier Excel et stocke les données dans la base de données.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
        """
        try:
            # Lecture des données Excel
            print("Lecture du fichier Excel...")
            df = self.read_excel()
            
            # Création de la table
            print("Création de la table dans la base de données...")
            self.create_database_table(db_path)
            
            # Insertion des données
            print("Insertion des données...")
            self.insert_data_to_database(db_path)
            
            print(f"Processus terminé avec succès!")
            print(f"Base de données: {db_path}")
            print(f"Table: VarCarMenageResult")
            print(f"Enregistrements: {len(df)}")
            
        except Exception as e:
            print(f"Erreur durant le processus: {e}")
            raise
    
    def query_database(self, query: str, db_path: str = "database.db") -> pd.DataFrame:
        """
        Exécute une requête SQL sur la base de données et retourne un DataFrame.
        
        Args:
            query (str): Requête SQL à exécuter
            db_path (str): Chemin vers la base de données SQLite
            
        Returns:
            pd.DataFrame: Résultats de la requête
        """
        try:
            conn = sqlite3.connect(db_path)
            result_df = pd.read_sql_query(query, conn)
            conn.close()
            return result_df
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            raise
    
    def export_database_to_csv(self, db_path: str = "database.db", csv_filename: str = "VarCarMenageResultCSV.csv"):
        """
        Lit la table VarCarMenageResult de la base de données et l'exporte vers un fichier CSV.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
            csv_filename (str): Nom du fichier CSV de sortie
        """
        try:
            # Vérification de l'existence de la base de données
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"La base de données {db_path} n'existe pas.")
            
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            
            # Vérification de l'existence de la table
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='VarCarMenageResult'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                raise ValueError("La table VarCarMenageResult n'existe pas dans la base de données.")
            
            # Lecture de toute la table
            query = "SELECT * FROM VarCarMenageResult"
            df_from_db = pd.read_sql_query(query, conn)
            
            # Vérification que la table n'est pas vide
            if df_from_db.empty:
                print("Attention: La table VarCarMenageResult est vide.")
            
            # Export vers CSV
            df_from_db.to_csv(csv_filename, index=False, encoding='utf-8')
            
            # Informations sur l'export
            print(f"Export réussi vers {csv_filename}")
            print(f"Nombre d'enregistrements exportés: {len(df_from_db)}")
            print(f"Nombre de colonnes: {len(df_from_db.columns)}")
            print(f"Taille du fichier: {os.path.getsize(csv_filename)} bytes")
            
            # Aperçu des premières lignes
            if not df_from_db.empty:
                print(f"\nAperçu des données exportées:")
                print(df_from_db.head(3).to_string())
            
            return df_from_db
            
        except Exception as e:
            print(f"Erreur lors de l'export vers CSV: {e}")
            raise
        finally:
            if conn:
                conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple d'utilisation de la classe VARCARMENAGEV3_excel_loader
    try:
        # Initialisation du lecteur avec votre fichier
        reader = VARCARMENAGEV3_excel_loader("VARCARMENAGEV3.xls")
        
        # Lecture des données
        df = reader.read_excel()
        
        # Affichage des informations
        print("Informations sur les données:")
        info = reader.get_data_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Affichage des premières lignes
        print("\nPremières lignes du DataFrame:")
        print(df.head())
        
        # Statistiques descriptives
        print("\nStatistiques descriptives:")
        print(reader.get_summary_stats())
        
        # Création de la table dans la base de données et insertion des données
        print("\n=== Stockage en base de données ===")
        reader.load_and_store_to_database("database.db")
        
        # Exemple de requête sur la base de données
        print("\n=== Test de requête ===")
        query_result = reader.query_database("SELECT COUNT(*) as total_records FROM VarCarMenageResult")
        print(f"Nombre total d'enregistrements en base: {query_result['total_records'].iloc[0]}")
        
        # Exemple d'autres requêtes possibles
        print("\nExemples de requêtes disponibles:")
        print("- SELECT * FROM VarCarMenageResult LIMIT 5")
        print("- SELECT AVG(revenunetmois) FROM VarCarMenageResult")
        print("- SELECT menage, tailledelafamille FROM VarCarMenageResult WHERE poor_oxford = 1")
        
        # Export de la table vers CSV
        print("\n=== Export vers CSV ===")
        exported_df = reader.export_database_to_csv("database.db", "VarCarMenageResultCSV.csv")
        
        # Export vers CSV (optionnel)
        # reader.export_to_csv("donnees_projet.csv")
        
    except Exception as e:
        print(f"Erreur: {e}")