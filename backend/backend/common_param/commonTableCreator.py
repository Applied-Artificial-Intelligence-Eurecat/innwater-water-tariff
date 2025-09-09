import sqlite3
from common.tbse_table import CommonTBSETable  # Adjust import path as needed

class SQLiteTBSETableCreator:
    """
    Classe pour créer et gérer la table TBSETable dans SQLite avec mode DEV
    """
    
    def __init__(self, table_name="tbse_table", db_path="database.db", DEV=False, **kwargs):
        """
        Initialise le créateur de table pour SQLite
        
        Args:
            table_name (str): Nom de la table
            db_path (str): Chemin vers la base de données SQLite
            DEV (bool): Mode développement - si True, supprime et recrée la table
            **kwargs: Arguments supplémentaires pour CommonTBSETable
        """
        self.table_name = table_name
        self.db_path = db_path
        self.DEV = DEV
        self.table_kwargs = kwargs
        self.table_instance = None
        self.connection = None
    
    def create_connection(self):
        """Établit une connexion à la base de données SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            print(f"Connexion à {self.db_path} établie avec succès")
            return self.connection
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def drop_table_if_exists(self):
        """Supprime la table si elle existe (uniquement en mode DEV)"""
        if not self.DEV:
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            self.connection.commit()
            print(f"Table '{self.table_name}' supprimée (mode DEV)")
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de la table: {e}")
            raise
    
    def table_exists(self):
        """Vérifie si la table existe dans la base de données"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='{self.table_name}'
            """)
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Erreur lors de la vérification: {e}")
            return False
    
    def create_table(self):
        """
        Lance la création de la table dans SQLite
        Gère la suppression/recréation selon le mode DEV
        """
        try:
            # Établir la connexion
            self.create_connection()
            
            # Logique selon le mode DEV
            if self.DEV:
                print("Mode DEV activé - suppression et recréation de la table")
                self.drop_table_if_exists()
                should_create = True
            else:
                # En mode production, on vérifie si la table existe déjà
                if self.table_exists():
                    print(f"Table '{self.table_name}' existe déjà (mode PROD)")
                    should_create = False
                else:
                    print(f"Table '{self.table_name}' n'existe pas - création")
                    should_create = True
            
            # Création de la table si nécessaire
            if should_create:
                # Création de l'instance de table
                self.table_instance = CommonTBSETable(
                    table_name=self.table_name,
                    connection=self.connection,
                    **self.table_kwargs
                )
                
                # Lancement de la création de la table
                self.table_instance.create_table()
                
                print(f"Table '{self.table_name}' créée avec succès dans {self.db_path}")
            else:
                print(f"Table '{self.table_name}' non recréée (mode PROD)")
                # On peut quand même initialiser l'instance pour l'utilisation
                self.table_instance = CommonTBSETable(
                    table_name=self.table_name,
                    connection=self.connection,
                    **self.table_kwargs
                )
            
            return self.table_instance
            
        except ImportError as e:
            print(f"Erreur d'importation: {e}")
            raise
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            raise
        except Exception as e:
            print(f"Erreur lors de la création de la table: {e}")
            raise
        finally:
            # Fermer la connexion
            if self.connection:
                self.connection.close()
                print("Connexion fermée")
    
    def get_table_info(self):
        """Affiche des informations sur la table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les informations de la table
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = cursor.fetchall()
            
            print(f"\nInformations de la table '{self.table_name}':")
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Compter les lignes
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            count = cursor.fetchone()[0]
            print(f"Nombre de lignes: {count}")
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations: {e}")
    
    def get_table_instance(self):
        """
        Retourne l'instance de la table
        
        Returns:
            CommonTBSETable: Instance de la table
        """
        return self.table_instance


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple 1: Mode DEV (suppression et recréation)
    print("=== MODE DÉVELOPPEMENT ===")
    dev_creator = SQLiteTBSETableCreator(
        table_name="ma_table_tbse",
        db_path="database.db",
        DEV=True,  # Mode développement activé
        # Ajouter d'autres paramètres nécessaires pour CommonTBSETable
    )
    dev_table = dev_creator.create_table()
    dev_creator.get_table_info()
    
    print("\n" + "="*50 + "\n")
    
    # Exemple 2: Mode PROD (création seulement si n'existe pas)
    print("=== MODE PRODUCTION ===")
    prod_creator = SQLiteTBSETableCreator(
        table_name="ma_table_tbse",
        db_path="database.db",
        DEV=False,  # Mode production
        # Ajouter d'autres paramètres nécessaires pour CommonTBSETable
    )
    prod_table = prod_creator.create_table()
    prod_creator.get_table_info()

