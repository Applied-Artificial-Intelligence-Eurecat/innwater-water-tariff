import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import xlrd  # Bibliothèque spécifique pour les fichiers .xls
import openpyxl
import warnings
import os
import glob
warnings.filterwarnings('ignore')

class ExcelFileReloader:
    """
    Classe spécialisée pour charger data_La_Réunion_2.xls
    avec intégration base de données
    """
    
    def __init__(self, file_path='data_La_Réunion_2.xls', db_name='database.db', id_projet=1):
        """
        Initialise le rechargeur de fichier Excel .xls
        
        Parameters:
        file_path (str): Chemin vers le fichier Excel .xls
        db_name (str): Nom de la base de données SQLite
        id_projet (int): Identifiant du projet à ajouter aux données (défaut: 1)
        """
        self.file_path = file_path
        self.db_name = db_name
        self.id_projet = id_projet
        self.workbook = None
        self.df = None
        self.sheet_names = []
        self.file_format = None
        self.file_exists = False
        
        self.file_exists = self._check_file_exists(file_path)
        if self.file_exists:
            print(f"✅ Fichier trouvé: {file_path}")
            self.load_excel_file(file_path)
        else:
            print(f"❌ Fichier non trouvé: {file_path}")
            print("🔍 Recherche de fichiers .xls dans le répertoire...")
            self._find_and_load_xls_file()
    
    def _check_file_exists(self, file_path):
        """Vérifie si le fichier existe"""
        return os.path.exists(file_path)
    
    def _find_and_load_xls_file(self):
        """Recherche et charge automatiquement le fichier .xls"""
        xls_files = glob.glob("*.xls") + glob.glob("*.XLS")  # Cherche .xls et .XLS
        
        if xls_files:
            print("📋 Fichiers .xls trouvés:")
            for i, file in enumerate(xls_files, 1):
                print(f"  {i}. {file}")
            
            # Cherche spécifiquement data_La_Réunion_2.xls
            reunion_files = [f for f in xls_files if 'réunion' in f.lower() or 'reunion' in f.lower()]
            
            if reunion_files:
                self.file_path = reunion_files[0]
                print(f"🎯 Fichier Réunion trouvé: {self.file_path}")
                self.file_exists = True
                self.load_excel_file(self.file_path)
            else:
                # Prend le premier fichier .xls trouvé
                self.file_path = xls_files[0]
                print(f"📁 Utilisation du fichier: {self.file_path}")
                self.file_exists = True
                self.load_excel_file(self.file_path)
        else:
            print("❌ Aucun fichier .xls trouvé dans le répertoire")
            print("💡 Placez data_La_Réunion_2.xls dans le même dossier que ce script")
    
    def load_excel_file(self, file_path):
        """
        Charge le fichier data_La_Réunion_2.xls
        """
        self.file_path = file_path
        
        if not self._check_file_exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
        try:
            # Méthode 1: Chargement avec xlrd (recommandé pour .xls)
            print("📥 Chargement avec xlrd...")
            self.df = pd.read_excel(file_path, engine='xlrd')
            
            # Ajouter la colonne id_projet avec valeur par défaut 1
            self.df['id_projet'] = self.id_projet
            print(f"✅ Fichier {os.path.basename(file_path)} chargé avec succès")
            print(f"✅ Colonne 'id_projet' ajoutée avec valeur: {self.id_projet}")
            
            # Récupérer les noms des feuilles
            xlrd_book = xlrd.open_workbook(file_path, on_demand=True)
            self.sheet_names = xlrd_book.sheet_names()
            xlrd_book.release_resources()
            print(f"📄 Feuilles disponibles: {', '.join(self.sheet_names)}")
            
            # Afficher les informations de base
            print(f"📊 Shape: {self.df.shape}")
            print(f"🏷️ Colonnes: {list(self.df.columns)}")
            
            self.file_format = 'xls'
            
        except Exception as e:
            print(f"❌ Erreur avec xlrd: {e}")
            print("🔄 Tentative de chargement manuel...")
            self._load_manually(file_path)
    
    def _load_manually(self, file_path):
        """Charge le fichier manuellement avec xlrd"""
        try:
            import xlrd
            print("📥 Chargement manuel avec xlrd...")
            
            # Ouvrir le workbook
            book = xlrd.open_workbook(file_path)
            self.sheet_names = [sheet.name for sheet in book.sheets()]
            print(f"📄 Feuilles: {', '.join(self.sheet_names)}")
            
            # Charger la première feuille
            sheet = book.sheet_by_index(0)
            print(f"📋 Feuille active: {sheet.name}")
            print(f"📐 Dimensions: {sheet.nrows} lignes x {sheet.ncols} colonnes")
            
            # Convertir en DataFrame
            data = []
            for row_idx in range(sheet.nrows):
                row_data = []
                for col_idx in range(sheet.ncols):
                    cell_value = sheet.cell_value(row_idx, col_idx)
                    row_data.append(cell_value)
                data.append(row_data)
            
            # Créer le DataFrame (première ligne = headers)
            if len(data) > 0:
                self.df = pd.DataFrame(data[1:], columns=data[0])
                
                # Ajouter la colonne id_projet avec valeur par défaut 1
                self.df['id_projet'] = self.id_projet
                print(f"✅ Données chargées: {self.df.shape}")
                print(f"✅ Colonne 'id_projet' ajoutée avec valeur: {self.id_projet}")
                
                self.file_format = 'xls_manual'
            else:
                raise Exception("Aucune donnée dans le fichier")
                
        except Exception as e:
            print(f"❌ Erreur de chargement manuel: {e}")
            raise Exception(f"Impossible de charger {file_path}")
    
    def add_id_projet_to_dataframe(self):
        """Ajoute la colonne id_projet au DataFrame"""
        if self.df is not None:
            if 'id_projet' not in self.df.columns:
                self.df['id_projet'] = self.id_projet
                print(f"✅ Colonne 'id_projet' ajoutée avec la valeur: {self.id_projet}")
            else:
                print(f"ℹ️  Colonne 'id_projet' existe déjà avec valeurs: {self.df['id_projet'].unique()}")
            return True
        return False
    
    def _drop_table_if_exists(self, table_name):
        """Supprime la table si elle existe déjà"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Vérifier si la table existe
            cursor.execute(f"""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='{table_name}'
            """)
            
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Supprimer la table
                cursor.execute(f"DROP TABLE {table_name}")
                conn.commit()
                print(f"✅ Table '{table_name}' supprimée")
            else:
                print(f"ℹ️  Table '{table_name}' n'existe pas encore")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de la table: {e}")
            return False
    
    def analyze_data(self):
        """Analyse les données chargées"""
        if self.df is not None:
            print("\n" + "="*50)
            print("📊 ANALYSE DES DONNÉES")
            print("="*50)
            
            print(f"Shape: {self.df.shape}")
            print(f"Colonnes: {list(self.df.columns)}")
            print(f"\nTypes de données:")
            print(self.df.dtypes)
            
            print(f"\n🔍 Valeurs manquantes par colonne:")
            missing = self.df.isnull().sum()
            for col, count in missing.items():
                if count > 0:
                    print(f"  {col}: {count} valeurs manquantes")
            
            print(f"\n📈 Statistiques descriptives:")
            print(self.df.describe())
    
    def save_to_sqlite(self, table_name='reunion_data'):
        """Sauvegarde les données de La Réunion dans SQLite"""
        try:
            # Supprimer la table si elle existe déjà
            self._drop_table_if_exists(table_name)
            
            # S'assurer que id_projet est présent dans le DataFrame
            self.add_id_projet_to_dataframe()
            
            # Sauvegarder les données
            conn = sqlite3.connect(self.db_name)
            self.df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            print(f"✅ Données sauvegardées dans '{table_name}'")
            
            # Vérifier que l'id_projet est bien présent
            self._verify_id_projet_in_table(table_name)
            
            return True
        except Exception as e:
            print(f"❌ Erreur SQLite: {e}")
            return False
    
    def _verify_id_projet_in_table(self, table_name):
        """Vérifie que l'id_projet est bien présent dans la table"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Vérifier la structure de la table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            id_projet_exists = any('id_projet' in col[1] for col in columns)
            
            if id_projet_exists:
                # Vérifier les valeurs
                cursor.execute(f"SELECT DISTINCT id_projet FROM {table_name}")
                ids = cursor.fetchall()
                print(f"✅ id_projet vérifié: valeurs distinctes = {[id[0] for id in ids]}")
            else:
                print("❌ id_projet non trouvé dans la table")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Erreur de vérification: {e}")
    
    def export_to_csv(self, output_path='data_La_Réunion_2.csv'):
        """Exporte les données en CSV"""
        try:
            # S'assurer que id_projet est présent avant l'export
            self.add_id_projet_to_dataframe()
            self.df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✅ Données exportées vers {output_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
            return False
    
    def get_file_info(self):
        """Retourne les informations du fichier"""
        info = {
            'file_path': self.file_path,
            'file_exists': self.file_exists,
            'file_format': self.file_format,
            'sheet_names': self.sheet_names,
            'dataframe_shape': self.df.shape if self.df is not None else None,
            'columns': self.df.columns.tolist() if self.df is not None else [],
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB" if self.df is not None else None,
            'id_projet': self.id_projet
        }
        return info

    def get_dataframe(self):
        """Retourne le DataFrame avec id_projet"""
        if self.df is not None:
            # S'assurer que id_projet est ajouté
            self.add_id_projet_to_dataframe()
            return self.df
        return None

    def reload_data(self):
        """Recharge le fichier Excel"""
        if self.file_exists:
            print(f"🔄 Rechargement du fichier {self.file_path}...")
            self.load_excel_file(self.file_path)
            return True
        return False

# Exemple d'utilisation
if __name__ == "__main__":
    print("🔧 CHARGEMENT DE data_La_Réunion_2.xls")
    print("="*50)
    
    try:
        # Initialiser avec le fichier spécifique (id_projet = 1 par défaut)
        reloader = ExcelFileReloader('data_La_Réunion_2.xls')
        
        if reloader.file_exists and reloader.df is not None:
            # Afficher les informations
            info = reloader.get_file_info()
            print("\n📋 INFORMATIONS DU FICHIER:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            # Afficher un aperçu
            print("\n👀 APERÇU DES DONNÉES:")
            print(reloader.df.head())
            
            # Analyser les données
            reloader.analyze_data()
            
            # Sauvegarder en base de données avec suppression si existe
            print("\n💾 SAUVEGARDE EN BASE...")
            reloader.save_to_sqlite('la_reunion_data')
            
            # Exporter en CSV
            print("\n📤 EXPORT EN CSV...")
            reloader.export_to_csv()
            
            print("\n🎉 TRAITEMENT TERMINÉ AVEC SUCCÈS!")
            
        else:
            print("❌ Impossible de charger les données")
            print("💡 Vérifiez que:")
            print("  1. Le fichier data_La_Réunion_2.xls est dans le bon dossier")
            print("  2. Vous avez installé xlrd: pip install xlrd==1.2.0")
            print("  3. Le fichier n'est pas corrompu")
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        print("\n🔧 SOLUTION:")
        print("1. Vérifiez que le fichier data_La_Réunion_2.xls existe")
        print("2. Installez xlrd: pip install xlrd==1.2.0")
        print("3. Vérifiez les permissions du fichier")