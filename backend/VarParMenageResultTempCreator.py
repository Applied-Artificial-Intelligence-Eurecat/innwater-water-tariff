import pandas as pd
import numpy as np
import sqlite3
import os

class ExcelDataAnalyzer:
    """
    Classe spécialisée pour analyser le fichier Excel VARPARMENAGEV.xls
    et gérer la base de données SQLite
    """
    
    def __init__(self, file_path="VARPARMENAGEV.xls", db_path="database.db"):
        """
        Initialise l'analyseur avec le chemin du fichier et de la base de données
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            db_path (str): Chemin vers la base de données SQLite
        """
        self.file_path = file_path
        self.db_path = db_path
        self.df = None
        self.column_categories = self._define_column_categories()
    
    def _define_column_categories(self):
        """Définit les catégories de colonnes basées sur le schéma"""
        return {
            'identifiants': ['id_projet', 'menage'],
            'caracteristiques_famille': ['tailledelafamille', 'nbreenfants', 'nbreadultes'],
            'revenu': ['revenunetmois'],
            'unites_consommation': ['ucoxford', 'ucocde'],
            'niveau_vie': ['niveaudevieoxford', 'niveaudevieocde'],
            'pauvrete': ['poor_oxford', 'poor_ocde'],
            'assainissement': ['assaini'],
            'seuils_pauvrete_ep': [
                'sep_t0_ibt_ep', 'sep_tmin_ibt_ep', 'sep_t_ibt_ep', 'sep_t_ibt_pp_ep',
                'sep_t0_tbse_ep', 'sep_tmin_tbse_ep', 'sep_t_tbse_ep'
            ],
            'autres_variables': [
                'a_t0_ibt', 'a_tmin_ibt', 'a_t_ibt', 'a_t_ibt_pp', 'a_t0_tbse',
                'a_tmin_tbse', 'a_t_tbse', 'sepa_t0_ibt', 'sepa_tmin_ibt', 'sepa_t_ibt',
                'sepa_t_ibt_pp', 'sepa_t0_tbse', 'sepa_tmin_tbse', 'sepa_t_tbse',
                'par_ibt', 'par_tbse', 'par_ibt_1', 'par_tbse_1', 'par_ibt_2',
                'par_tbse_2', 'par_ibt_3', 'par_tbse_3', 'seuil_depenses_trim_par_pct_3_r',
                'exces_dep_0_inclus_ibt', 'exces_dep_0_inclus_tbse'
            ],
            'lz_tbse': [
                'lz_ina_tbse_menage', 'lz_ina_tbse_exces_dep_tbse',
                'lz_ina_tbse_rg_normalise', 'lz_ina_tbse_alpha', 'lz_ina_tbse_l_tbse'
            ],
            'cc_ina_tbse': [
                'cc_ina_nv_tbse_menage', 'cc_ina_nv_tbse_nivvie_ocde',
                'cc_ina_nv_tbse_rg_nivvie', 'cc_ina_nv_tbse_rg_ina_tbse',
                'cc_ina_nv_tbse_excdep_tbse', 'cc_ina_nv_tbse_alpha', 'cc_ina_nv_tbse_c_tbse'
            ],
            'lz_ibt': [
                'lz_ina_ibt_menage', 'lz_ina_ibt_exces_dep_ibt',
                'lz_ina_ibt_rg_normalise_ibt', 'lz_ina_ibt_alpha', 'lz_ina_ibt_l_ibt'
            ],
            'cc_ina_ibt': [
                'cc_ina_nivvie_ibt_menage', 'cc_ina_nivvie_ibt_niveau_de_vie_ocde',
                'cc_ina_nivvie_ibt_rang_nor_niveau_de_vie', 'cc_ina_nivvie_ibt_rg_inab_ibt',
                'cc_ina_nivvie_ibt_exces_dep_ibt', 'cc_ina_nivvie_ibt_alpha', 'cc_ina_nivvie_ibt_c_ibt'
            ],
            'cc_gen': ['cc_gen_rang', 'cc_gen_cg_tbse', 'cc_gen_cg_ibt']
        }
    
    def read_excel_file(self, sheet_name=0, **kwargs):
        """
        Lit le fichier Excel avec gestion des erreurs
        
        Args:
            sheet_name (str/int): Nom ou index de la feuille
            **kwargs: Arguments supplémentaires pour pd.read_excel()
        
        Returns:
            bool: True si la lecture a réussi, False sinon
        """
        try:
            self.df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                **kwargs
            )
            print(f"✓ Fichier '{self.file_path}' lu avec succès")
            print(f"✓ Shape: {self.df.shape}")
            return True
            
        except FileNotFoundError:
            print(f"✗ Erreur: Fichier '{self.file_path}' non trouvé")
            return False
        except Exception as e:
            print(f"✗ Erreur lors de la lecture: {e}")
            return False
    
    def manage_database_table(self):
        """
        Crée la table VarParMenageResultTemp dans la base de données
        et la supprime si elle existe déjà
        """
        # Définition du schéma de la table
        table_schema = """
        CREATE TABLE "VarParMenageResultTemp" (
            "id_projet"	INTEGER,
            "menage"	INTEGER,
            "tailledelafamille"	INTEGER,
            "nbreenfants"	INTEGER,
            "nbreadultes"	INTEGER,
            "revenunetmois"	REAL,
            "ucoxford"	REAL,
            "ucocde"	REAL,
            "niveaudevieoxford"	REAL,
            "niveaudevieocde"	REAL,
            "poor_oxford"	INTEGER,
            "poor_ocde"	INTEGER,
            "assaini"	INTEGER,
            "sep_t0_ibt_ep"	REAL,
            "sep_tmin_ibt_ep"	REAL,
            "sep_t_ibt_ep"	REAL,
            "sep_t_ibt_pp_ep"	REAL,
            "sep_t0_tbse_ep"	REAL,
            "sep_tmin_tbse_ep"	REAL,
            "sep_t_tbse_ep"	REAL,
            "a_t0_ibt"	REAL,
            "a_tmin_ibt"	REAL,
            "a_t_ibt"	REAL,
            "a_t_ibt_pp"	REAL,
            "a_t0_tbse"	REAL,
            "a_tmin_tbse"	REAL,
            "a_t_tbse"	REAL,
            "sepa_t0_ibt"	REAL,
            "sepa_tmin_ibt"	REAL,
            "sepa_t_ibt"	REAL,
            "sepa_t_ibt_pp"	REAL,
            "sepa_t0_tbse"	REAL,
            "sepa_tmin_tbse"	REAL,
            "sepa_t_tbse"	REAL,
            "par_ibt"	REAL,
            "par_tbse"	REAL,
            "par_ibt_1"	INTEGER,
            "par_tbse_1"	INTEGER,
            "par_ibt_2"	INTEGER,
            "par_tbse_2"	INTEGER,
            "par_ibt_3"	INTEGER,
            "par_tbse_3"	INTEGER,
            "seuil_depenses_trim_par_pct_3_r"	REAL,
            "exces_dep_0_inclus_ibt"	REAL,
            "exces_dep_0_inclus_tbse"	REAL,
            "lz_ina_tbse_menage"	INTEGER,
            "lz_ina_tbse_exces_dep_tbse"	REAL,
            "lz_ina_tbse_rg_normalise"	REAL,
            "lz_ina_tbse_alpha"	REAL,
            "lz_ina_tbse_l_tbse"	REAL,
            "cc_ina_nv_tbse_menage"	INTEGER,
            "cc_ina_nv_tbse_nivvie_ocde"	REAL,
            "cc_ina_nv_tbse_rg_nivvie"	REAL,
            "cc_ina_nv_tbse_rg_ina_tbse"	REAL,
            "cc_ina_nv_tbse_excdep_tbse"	REAL,
            "cc_ina_nv_tbse_alpha"	REAL,
            "cc_ina_nv_tbse_c_tbse"	REAL,
            "lz_ina_ibt_menage"	INTEGER,
            "lz_ina_ibt_exces_dep_ibt"	REAL,
            "lz_ina_ibt_rg_normalise_ibt"	REAL,
            "lz_ina_ibt_alpha"	REAL,
            "lz_ina_ibt_l_ibt"	REAL,
            "cc_ina_nivvie_ibt_menage"	INTEGER,
            "cc_ina_nivvie_ibt_niveau_de_vie_ocde"	REAL,
            "cc_ina_nivvie_ibt_rang_nor_niveau_de_vie"	REAL,
            "cc_ina_nivvie_ibt_rg_inab_ibt"	REAL,
            "cc_ina_nivvie_ibt_exces_dep_ibt"	REAL,
            "cc_ina_nivvie_ibt_alpha"	REAL,
            "cc_ina_nivvie_ibt_c_ibt"	REAL,
            "cc_gen_rang"	REAL,
            "cc_gen_cg_tbse"	REAL,
            "cc_gen_cg_ibt"	REAL
        );
        """
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si la table existe déjà
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='VarParMenageResultTemp'
            """)
            
            table_exists = cursor.fetchone()
            
            if table_exists:
                # Supprimer la table si elle existe
                print("✓ Table 'VarParMenageResultTemp' existe déjà")
                cursor.execute("DROP TABLE VarParMenageResultTemp")
                print("✓ Table 'VarParMenageResultTemp' supprimée")
            
            # Créer la nouvelle table
            cursor.execute(table_schema)
            print("✓ Table 'VarParMenageResultTemp' créée avec succès")
            
            # Valider les changements et fermer la connexion
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Erreur SQLite: {e}")
            return False
        except Exception as e:
            print(f"✗ Erreur lors de la gestion de la table: {e}")
            return False
    
    def insert_data_to_db(self):
        """
        Insère les données du DataFrame dans la table de la base de données
        """
        if self.df is None:
            print("✗ Aucune donnée à insérer. Veuillez d'abord lire le fichier Excel.")
            return False
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.db_path)
            
            # Insérer les données dans la table
            self.df.to_sql('VarParMenageResultTemp', conn, if_exists='replace', index=False)
            
            # Vérifier le nombre de lignes insérées
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM VarParMenageResultTemp")
            row_count = cursor.fetchone()[0]
            
            # Fermer la connexion
            conn.close()
            
            print(f"✓ Données insérées avec succès: {row_count} lignes")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Erreur SQLite lors de l'insertion: {e}")
            return False
        except Exception as e:
            print(f"✗ Erreur lors de l'insertion des données: {e}")
            return False
    
    def display_basic_info(self):
        """Affiche les informations de base du DataFrame"""
        if self.df is None:
            print("Aucune donnée chargée. Veuillez d'abord lire le fichier.")
            return
        
        print("\n" + "="*60)
        print("INFORMATIONS DE BASE DU DATAFRAME")
        print("="*60)
        
        print(f"\nDimensions: {self.df.shape[0]} lignes × {self.df.shape[1]} colonnes")
        
        print("\n5 premières lignes:")
        print(self.df.head())
        
        print("\nTypes de données:")
        print(self.df.dtypes)
        
        print("\nStatistiques descriptives:")
        print(self.df.describe())
    
    def display_column_categories(self):
        """Affiche les colonnes par catégories"""
        if self.df is None:
            print("Aucune donnée chargée.")
            return
        
        print("\n" + "="*60)
        print("CATÉGORIES DE COLONNES")
        print("="*60)
        
        for category, columns in self.column_categories.items():
            available_cols = [col for col in columns if col in self.df.columns]
            if available_cols:
                print(f"\n{category.upper().replace('_', ' ')} ({len(available_cols)}):")
                print(f"  {', '.join(available_cols)}")
    
    def check_missing_values(self):
        """Vérifie les valeurs manquantes"""
        if self.df is None:
            print("Aucune donnée chargée.")
            return
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        
        print("\n" + "="*60)
        print("VALEURS MANQUANTES")
        print("="*60)
        
        if missing.sum() == 0:
            print("✓ Aucune valeur manquante détectée")
        else:
            missing_df = pd.DataFrame({
                'Valeurs manquantes': missing,
                'Pourcentage': missing_percent
            })
            missing_df = missing_df[missing_df['Valeurs manquantes'] > 0]
            print(missing_df.sort_values('Pourcentage', ascending=False))
    
    def get_dataframe(self):
        """Retourne le DataFrame complet"""
        return self.df
    
    def get_category_data(self, category_name):
        """
        Retourne les données d'une catégorie spécifique
        
        Args:
            category_name (str): Nom de la catégorie
        
        Returns:
            pandas.DataFrame: Sous-ensemble des données
        """
        if self.df is None:
            print("Aucune donnée chargée.")
            return None
        
        if category_name not in self.column_categories:
            print(f"Catégorie '{category_name}' non trouvée.")
            return None
        
        columns = [col for col in self.column_categories[category_name] if col in self.df.columns]
        return self.df[columns]

# Exemple d'utilisation complet
if __name__ == "__main__":
    # Création de l'instance
    analyzer = ExcelDataAnalyzer("VARPARMENAGEV.xls", "database.db")
    
    # Lecture du fichier Excel
    if analyzer.read_excel_file():
        # Affichage des informations
        analyzer.display_basic_info()
        
        # Gestion de la table dans la base de données
        if analyzer.manage_database_table():
            # Insertion des données dans la base
            analyzer.insert_data_to_db()
        
        # Vérification des valeurs manquantes
        analyzer.check_missing_values()
        
        # Exemple: accès aux données de la catégorie 'revenu'
        revenu_data = analyzer.get_category_data('revenu')
        if revenu_data is not None:
            print(f"\nDonnées de revenu:")
            print(revenu_data.head())