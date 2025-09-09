import sqlite3
from typing import Dict, List, Optional, Union

class DatabaseManager:
    """
    Classe pour gérer une base de données SQLite avec création de tables.
    """
    
    def __init__(self, db_name: str = "database.db"):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_name (str): Nom du fichier de base de données (par défaut: "database.db")
        """
        self.db_name = db_name
        self.connection = None
    
    def connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion : {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def create_table(self, table_name: str, columns: Dict[str, str], primary_key: Optional[str] = None) -> bool:
        """
        Crée une table dans la base de données.
        
        Args:
            table_name (str): Nom de la table à créer
            columns (Dict[str, str]): Dictionnaire {nom_colonne: type_sql}
            primary_key (str, optional): Nom de la colonne clé primaire
            
        Returns:
            bool: True si la table a été créée avec succès, False sinon
            
        Exemple:
            columns = {
                "id": "INTEGER",
                "nom": "TEXT NOT NULL",
                "age": "INTEGER",
                "email": "TEXT UNIQUE"
            }
            db.create_table("utilisateurs", columns, primary_key="id")
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            # Construction de la requête SQL
            column_definitions = []
            
            for col_name, col_type in columns.items():
                col_def = f"{col_name} {col_type}"
                if primary_key and col_name == primary_key:
                    col_def += " PRIMARY KEY"
                column_definitions.append(col_def)
            
            columns_sql = ", ".join(column_definitions)
            sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            self.connection.commit()
            
            print(f"Table '{table_name}' créée avec succès.")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table '{table_name}' : {e}")
            return False
    
    def create_table_from_list(self, table_name: str, column_names: List[str], 
                              column_type: str = "TEXT", primary_key: Optional[str] = None) -> bool:
        """
        Crée une table à partir d'une liste de noms de colonnes.
        
        Args:
            table_name (str): Nom de la table à créer
            column_names (List[str]): Liste des noms de colonnes
            column_type (str): Type SQL par défaut pour toutes les colonnes (défaut: "TEXT")
            primary_key (str, optional): Nom de la colonne clé primaire
            
        Returns:
            bool: True si la table a été créée avec succès, False sinon
        """
        columns = {name: column_type for name in column_names}
        return self.create_table(table_name, columns, primary_key)
    
    def table_exists(self, table_name: str) -> bool:
        """
        Vérifie si une table existe dans la base de données.
        
        Args:
            table_name (str): Nom de la table à vérifier
            
        Returns:
            bool: True si la table existe, False sinon
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table_name,))
            
            return cursor.fetchone() is not None
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la vérification de la table : {e}")
            return False
    
    def get_table_info(self, table_name: str) -> Optional[List[tuple]]:
        """
        Récupère les informations sur les colonnes d'une table.
        
        Args:
            table_name (str): Nom de la table
            
        Returns:
            List[tuple]: Informations sur les colonnes ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations : {e}")
            return None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[List[tuple]]:
        """
        Exécute une requête SQL personnalisée.
        
        Args:
            query (str): Requête SQL à exécuter
            params (tuple, optional): Paramètres pour la requête
            
        Returns:
            List[tuple]: Résultats de la requête ou None
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None
    
    def __enter__(self):
        """Support du context manager."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager."""
        self.disconnect()


# Exemple d'utilisation
if __name__ == "__main__":
    # Utilisation basique
    db = DatabaseManager("database.db")
    
    # Création d'une table avec types spécifiés
    columns_utilisateurs = {
        "id": "INTEGER",
        "nom": "TEXT NOT NULL",
        "prenom": "TEXT NOT NULL",
        "age": "INTEGER",
        "email": "TEXT UNIQUE"
    }
    
    db.create_table("utilisateurs", columns_utilisateurs, primary_key="id")
    
    # Création d'une table à partir d'une liste (comme votre liste de colonnes)
    ma_liste_colonnes = [
        "id_projet", "menage", "assaini", "constante", "taille_famille",
        "snwa", "swim", "garden_weather"
    ]
    
    db.create_table_from_list("ma_table", ma_liste_colonnes, primary_key="id_projet")
    
    # Vérification de l'existence d'une table
    if db.table_exists("utilisateurs"):
        print("La table 'utilisateurs' existe")
    
    # Utilisation avec context manager
    with DatabaseManager("database.db") as db_manager:
        columns = {"id": "INTEGER", "data": "TEXT"}
        db_manager.create_table("test_table", columns, primary_key="id")
    
    db.disconnect()