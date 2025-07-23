import sqlite3
import logging
from functools import lru_cache

class ProjectCheckService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_service()
        return cls._instance
    
    def _init_service(self):
        """Initialisation du service"""
        self.logger = logging.getLogger('ProjectCheckService')
        self.database_path = 'database.db'  # À remplacer par votre config
        
    @lru_cache(maxsize=128)
    def check_project_exists(self, project_id, table_name):
        """Vérifie si un projet existe dans une table spécifique"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Vérifie d'abord que la table existe
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                if not cursor.fetchone():
                    self.logger.error(f"Table '{table_name}' introuvable")
                    return False
                
                # Cherche le projet dans la table spécifique
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE id_projet = ?", (project_id,))
                return cursor.fetchone() is not None
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur DB: {str(e)}")
            return False

    @staticmethod
    def main():
        """Méthode principale pour tester la fonctionnalité"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        print("Test de vérification d'existence de projet")
        
        # Paramètres de test
        project_id = 1
        table_name = "AFS_pop_hh_in_difficulty"
        
        # Création d'une instance du service
        service = ProjectCheckService()
        
        # Appel de la méthode project_exists
        exists = service.check_project_exists(project_id, table_name)
        
        # Affichage du résultat
        print(f"\nRésultat: Le projet {project_id} {'existe' if exists else 'n\'existe pas'} dans la table {table_name}")

if __name__ == "__main__":
    ProjectCheckService.main()