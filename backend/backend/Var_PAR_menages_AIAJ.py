import sqlite3
import os
from typing import List, Optional, Dict, Any

class DatabaseManager:
    def __init__(self, db_name: str = "database.db"):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_name (str): Nom du fichier de base de données SQLite
        """
        self.db_name = db_name
        self.connection = None
        self.connect()
        
    def connect(self) -> None:
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            # Activer les foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
            print(f"Connexion à la base de données '{self.db_name}' établie avec succès")
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            self.connection = None
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")
    
    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Exécute une requête SQL
        
        Args:
            query (str): Requête SQL à exécuter
            params (tuple): Paramètres pour la requête
            
        Returns:
            sqlite3.Cursor: Curseur avec le résultat
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            self.connection.rollback()
            raise
    
    def update_par_columns(self, project_id: int, table_name: str = "VarParMenageResult") -> int:
        """
        Met à jour les colonnes par_ibt et par_tbse pour un projet spécifique
        
        Args:
            project_id (int): ID du projet à mettre à jour
            table_name (str): Nom de la table
            
        Returns:
            int: Nombre de lignes affectées
        """
        query = f"""
            UPDATE {table_name} 
            SET 
                par_ibt = CASE 
                    WHEN revenunetmois = 0 OR revenunetmois IS NULL THEN NULL 
                    ELSE 100.0 * (sepa_tmin_ibt / 3.0) / revenunetmois 
                END,
                par_tbse = CASE 
                    WHEN revenunetmois = 0 OR revenunetmois IS NULL THEN NULL 
                    ELSE 100.0 * (sepa_tmin_tbse / 3.0) / revenunetmois 
                END
            WHERE id_projet = ?
        """
        
        try:
            cursor = self.execute_query(query, (project_id,))
            rows_affected = cursor.rowcount
            print(f"Mise à jour réussie pour le projet ID {project_id}")
            print(f"Nombre de lignes affectées : {rows_affected}")
            return rows_affected
        except Exception as e:
            print(f"Erreur lors de la mise à jour du projet {project_id}: {e}")
            return 0
    
    def update_all_projects(self, table_name: str = "VarParMenageResult") -> int:
        """
        Met à jour tous les projets de la table
        
        Args:
            table_name (str): Nom de la table
            
        Returns:
            int: Nombre total de lignes affectées
        """
        query = f"""
            UPDATE {table_name} 
            SET 
                par_ibt = CASE 
                    WHEN revenunetmois = 0 OR revenunetmois IS NULL THEN NULL 
                    ELSE 100.0 * (sepa_tmin_ibt / 3.0) / revenunetmois 
                END,
                par_tbse = CASE 
                    WHEN revenunetmois = 0 OR revenunetmois IS NULL THEN NULL 
                    ELSE 100.0 * (sepa_tmin_tbse / 3.0) / revenunetmois 
                END
        """
        
        try:
            cursor = self.execute_query(query)
            rows_affected = cursor.rowcount
            print(f"Mise à jour massive réussie")
            print(f"Total des lignes affectées : {rows_affected}")
            return rows_affected
        except Exception as e:
            print(f"Erreur lors de la mise à jour massive: {e}")
            return 0
    
    def get_project_data(self, project_id: int, table_name: str = "VarParMenageResult") -> Optional[Dict[str, Any]]:
        """
        Récupère les données d'un projet spécifique
        
        Args:
            project_id (int): ID du projet
            table_name (str): Nom de la table
            
        Returns:
            Optional[Dict]: Données du projet ou None si non trouvé
        """
        query = f"""
            SELECT id_projet, sepa_tmin_ibt, sepa_tmin_tbse, revenunetmois, par_ibt, par_tbse
            FROM {table_name} 
            WHERE id_projet = ?
        """
        
        try:
            cursor = self.execute_query(query, (project_id,))
            row = cursor.fetchone()
            
            if row:
                columns = ['id_projet', 'sepa_tmin_ibt', 'sepa_tmin_tbse', 'revenunetmois', 'par_ibt', 'par_tbse']
                return dict(zip(columns, row))
            else:
                print(f"Aucun projet trouvé avec l'ID {project_id}")
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return None
    
    def create_table_if_not_exists(self, table_name: str = "VarParMenageResult") -> bool:
        """
        Crée la table si elle n'existe pas (méthode utilitaire)
        
        Args:
            table_name (str): Nom de la table à créer
            
        Returns:
            bool: True si la table a été créée ou existe déjà
        """
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projet INTEGER NOT NULL,
                sepa_tmin_ibt REAL,
                sepa_tmin_tbse REAL,
                revenunetmois REAL,
                par_ibt REAL,
                par_tbse REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        try:
            self.execute_query(query)
            print(f"Table '{table_name}' vérifiée/créée avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de la création de la table: {e}")
            return False
    
    def insert_sample_data(self, table_name: str = "VarParMenageResult") -> None:
        """
        Insère des données d'exemple pour tester
        """
        sample_data = [
            (1, 1500, 1200, 3000, None, None),
            (2, 1800, 1500, 4500, None, None),
            (3, 900, 800, 0, None, None),  # revenunetmois = 0 pour tester
        ]
        
        query = f"""
            INSERT INTO {table_name} (id_projet, sepa_tmin_ibt, sepa_tmin_tbse, revenunetmois, par_ibt, par_tbse)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, sample_data)
            self.connection.commit()
            print(f"Données d'exemple insérées dans '{table_name}'")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données: {e}")
            self.connection.rollback()

    def check_existing_data(self, table_name: str = "VarParMenageResult", limit: int = 5) -> None:
        """
        Vérifie les données existantes dans la table
        
        Args:
            table_name (str): Nom de la table
            limit (int): Nombre de lignes à afficher
        """
        query = f"""
            SELECT id_projet, sepa_tmin_ibt, sepa_tmin_tbse, revenunetmois, par_ibt, par_tbse
            FROM {table_name} 
            LIMIT {limit}
        """
        
        try:
            cursor = self.execute_query(query)
            rows = cursor.fetchall()
            
            if rows:
                print(f"\n=== DONNÉES EXISTANTES DANS {table_name} (premiers {limit} enregistrements) ===")
                columns = ['id_projet', 'sepa_tmin_ibt', 'sepa_tmin_tbse', 'revenunetmois', 'par_ibt', 'par_tbse']
                print(" | ".join(f"{col:>15}" for col in columns))
                print("-" * (16 * len(columns) - 1))
                
                for row in rows:
                    print(" | ".join(f"{str(val):>15}" for val in row))
            else:
                print(f"Aucune donnée trouvée dans la table {table_name}")
                
        except Exception as e:
            print(f"Erreur lors de la vérification des données: {e}")

def main():
    """Fonction principale pour démontrer l'utilisation de la classe"""
    
    # Initialisation de la classe avec la bonne base de données
    db_manager = DatabaseManager("database.db")
    
    try:
        # Vérification des données existantes
        print("=== VÉRIFICATION DES DONNÉES EXISTANTES ===")
        db_manager.check_existing_data("VarParMenageResult", 10)
        
        # Si la table n'existe pas, la créer et insérer des données de test
        # Décommentez les lignes suivantes si vous voulez créer la table et insérer des données de test
        # db_manager.create_table_if_not_exists("VarParMenageResult")
        # db_manager.insert_sample_data("VarParMenageResult")
        
        # Mise à jour d'un projet spécifique (exemple avec projet ID 1)
        print("\n=== MISE À JOUR PROJET SPÉCIFIQUE (ID 1) ===")
        rows_affected = db_manager.update_par_columns(1, "VarParMenageResult")
        
        if rows_affected > 0:
            # Affichage des données après mise à jour
            print("\n=== DONNÉES APRÈS MISE À JOUR SPÉCIFIQUE ===")
            project_data = db_manager.get_project_data(1, "VarParMenageResult")
            if project_data:
                print(f"Projet 1: {project_data}")
        
        # Option pour mettre à jour tous les projets
        print("\n=== MISE À JOUR DE TOUS LES PROJETS ===")
        response = input("Voulez-vous mettre à jour tous les projets ? (y/N): ")
        if response.lower() in ['y', 'yes', 'oui']:
            total_rows_affected = db_manager.update_all_projects("VarParMenageResult")
            print(f"Total de {total_rows_affected} lignes mises à jour")
            
            # Affichage d'un échantillon des données mises à jour
            print("\n=== ÉCHANTILLON APRÈS MISE À JOUR MASSIVE ===")
            db_manager.check_existing_data("VarParMenageResult", 5)
        
    except Exception as e:
        print(f"Erreur dans le main: {e}")
    
    finally:
        # Fermeture propre de la connexion
        db_manager.disconnect()

if __name__ == "__main__":
    main()