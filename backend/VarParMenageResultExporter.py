import sqlite3
import csv
from pathlib import Path

class VarParMenageResultExporter:
    def __init__(self, db_path="database.db"):
        """
        Initialise l'exportateur avec le chemin de la base de données SQLite
        
        Args:
            db_path (str): Chemin vers le fichier de base de données SQLite (par défaut: database.db)
        """
        self.db_path = db_path
        self.table_name = "VarParMenageResult"
        
    def export_to_csv(self, output_path="VarParMenageResult_export.csv", batch_size=1000):
        """
        Exporte les données de la table vers un fichier CSV
        
        Args:
            output_path (str): Chemin du fichier CSV de sortie
            batch_size (int): Taille des lots pour la lecture des données
        """
        # Vérifier que la base de données existe
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"La base de données {self.db_path} n'existe pas")
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les noms des colonnes
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            # Compter le nombre total de lignes
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            total_rows = cursor.fetchone()[0]
            
            print(f"Export de {total_rows} lignes de la table '{self.table_name}' vers {output_path}")
            
            # Ouvrir le fichier CSV en mode écriture
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Écrire l'en-tête
                writer.writerow(column_names)
                
                # Lire les données par lots
                offset = 0
                rows_exported = 0
                
                while offset < total_rows:
                    cursor.execute(
                        f"SELECT * FROM {self.table_name} LIMIT ? OFFSET ?",
                        (batch_size, offset)
                    )
                    
                    batch = cursor.fetchall()
                    
                    if not batch:
                        break
                    
                    # Écrire le lot dans le CSV
                    writer.writerows(batch)
                    rows_exported += len(batch)
                    offset += batch_size
                    
                    # Afficher la progression
                    progress = (rows_exported / total_rows) * 100
                    print(f"Progression: {rows_exported}/{total_rows} lignes ({progress:.1f}%)", end='\r')
            
            print(f"\n✓ Export terminé ! {rows_exported} lignes exportées vers {output_path}")
            
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite: {e}")
            raise
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_table_schema(self):
        """
        Retourne le schéma de la table sous forme de dictionnaire
        
        Returns:
            dict: Dictionnaire avec les noms de colonnes et leurs types
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            schema = {}
            
            for col in cursor.fetchall():
                schema[col[1]] = col[2]  # col[1] = nom, col[2] = type
            
            return schema
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du schéma: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def verify_export(self, csv_path):
        """
        Vérifie que l'export s'est bien déroulé en comparant le nombre de lignes
        
        Args:
            csv_path (str): Chemin du fichier CSV exporté
        """
        try:
            # Compter les lignes dans la base
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            db_count = cursor.fetchone()[0]
            
            # Compter les lignes dans le CSV (sans compter l'en-tête)
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                csv_count = sum(1 for line in csvfile) - 1
            
            print(f"Vérification:")
            print(f"  - Lignes dans la base: {db_count}")
            print(f"  - Lignes dans le CSV: {csv_count}")
            
            if db_count == csv_count:
                print("✓ Export vérifié: les nombres correspondent !")
            else:
                print("⚠️  Attention: différence dans le nombre de lignes")
                
        except Exception as e:
            print(f"Erreur lors de la vérification: {e}")
        finally:
            if conn:
                conn.close()

# Exemple d'utilisation simplifié
if __name__ == "__main__":
    # Créer l'exportateur avec le nom de base par défaut
    exporter = VarParMenageResultExporter("database.db")
    
    try:
        # Afficher le schéma (optionnel)
        print("📋 Schéma de la table VarParMenageResult:")
        schema = exporter.get_table_schema()
        for col_name, col_type in schema.items():
            print(f"  {col_name}: {col_type}")
        
        print("\n" + "="*50)
        
        # Exporter les données
        output_file = "VarParMenageResult_export.csv"
        exporter.export_to_csv(output_file)
        
        # Vérifier l'export
        print("\n" + "="*50)
        exporter.verify_export(output_file)
        
    except FileNotFoundError:
        print(f"❌ Erreur: Le fichier database.db n'a pas été trouvé.")
        print("Veuillez vous assurer que:")
        print("1. Le fichier database.db est dans le même dossier que ce script")
        print("2. Le nom de la base de données est correct")
        print("3. La table 'VarParMenageResult' existe dans la base")
    except sqlite3.Error as e:
        print(f"❌ Erreur de base de données: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")