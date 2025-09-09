import sqlite3
from contextlib import contextmanager
from typing import Dict, Optional, List
import logging
from enum import Enum

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UpdateOperation(Enum):
    """Énumération des opérations de mise à jour disponibles"""
    I1 = "i1"
    I2 = "i2"
    T1 = "t1"
    T2 = "t2"
    T1_T2_EURO = "t1_t2_euro"

class SurplusG1TBSEAXBB:
    """
    Gestionnaire de base de données pour les mises à jour de la table surplusG1TBSE
    
    Cette classe fournit des méthodes pour mettre à jour différentes colonnes
    de la table surplusG1TBSE en fonction de l'id_projet.
    """
    
    def __init__(self, db_name: str = "database.db"):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_name (str): Nom du fichier de base de données SQLite
        """
        self.db_name = db_name
        self._validate_database()
    
    def _validate_database(self) -> None:
        """Valide que la base de données et la table existent"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='surplusG1TBSE';
                """)
                if not cursor.fetchone():
                    logger.warning("Table 'surplusG1TBSE' non trouvée dans la base de données")
        except Exception as e:
            logger.error(f"Erreur lors de la validation de la base de données: {e}")
    
    @contextmanager
    def get_connection(self):
        """
        Gestionnaire de contexte pour la connexion à la base de données
        
        Yields:
            sqlite3.Connection: Connexion à la base de données
            
        Raises:
            sqlite3.Error: En cas d'erreur de base de données
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute("PRAGMA foreign_keys = ON")  # Active les clés étrangères
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Erreur de transaction: {e}")
            raise e
        finally:
            if conn:
                conn.close()
    
    def _execute_update(self, query: str, params: tuple, operation_name: str) -> bool:
        """
        Méthode générique pour exécuter une mise à jour
        
        Args:
            query (str): Requête SQL de mise à jour
            params (tuple): Paramètres de la requête
            operation_name (str): Nom de l'opération pour les logs
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                rows_affected = cursor.rowcount
                if rows_affected > 0:
                    logger.info(f"Mise à jour {operation_name} réussie pour id_projet {params[0]}: {rows_affected} ligne(s) modifiée(s)")
                    return True
                else:
                    logger.warning(f"Aucune ligne trouvée pour id_projet {params[0]} lors de l'opération {operation_name}")
                    return False
                
        except sqlite3.Error as e:
            logger.error(f"Erreur SQLite lors de la mise à jour {operation_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'opération {operation_name}: {e}")
            return False
    
    def project_exists(self, id_projet: int) -> bool:
        """
        Vérifie si un projet existe dans la base de données
        
        Args:
            id_projet (int): L'identifiant du projet
            
        Returns:
            bool: True si le projet existe, False sinon
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM surplusG1TBSE WHERE id_projet = ? LIMIT 1", (id_projet,))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Erreur lors de la vérification d'existence du projet {id_projet}: {e}")
            return False
    
    def update_surplusG1TBSE_by_id_i1(self, id_projet: int) -> bool:
        """
        Met à jour tbse_redev_trim_i1 = tbse_redev_i1 * 90
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.project_exists(id_projet):
            logger.warning(f"Projet {id_projet} non trouvé")
            return False
            
        query = """
        UPDATE surplusG1TBSE
        SET tbse_redev_trim_i1 = tbse_redev_i1 * 90
        WHERE id_projet = ?;
        """
        return self._execute_update(query, (id_projet,), "i1")
    
    def update_surplusG1TBSE_by_id_i2(self, id_projet: int) -> bool:
        """
        Met à jour tbse_redev_trim_i2 = tbse_redev_i2 * 90
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.project_exists(id_projet):
            logger.warning(f"Projet {id_projet} non trouvé")
            return False
            
        query = """
        UPDATE surplusG1TBSE
        SET tbse_redev_trim_i2 = tbse_redev_i2 * 90
        WHERE id_projet = ?;
        """
        return self._execute_update(query, (id_projet,), "i2")
    
    def update_surplusG1TBSE_by_id_t1(self, id_projet: int) -> bool:
        """
        Met à jour tbse_redev_trim_t1 = tbse_redev_trim_i1
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.project_exists(id_projet):
            logger.warning(f"Projet {id_projet} non trouvé")
            return False
            
        query = """
        UPDATE surplusG1TBSE
        SET tbse_redev_trim_t1 = tbse_redev_trim_i1
        WHERE id_projet = ?;
        """
        return self._execute_update(query, (id_projet,), "t1")
    
    def update_surplusG1TBSE_by_id_t2(self, id_projet: int) -> bool:
        """
        Met à jour tbse_redev_trim_t2 = -tbse_redev_trim_i2
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.project_exists(id_projet):
            logger.warning(f"Projet {id_projet} non trouvé")
            return False
            
        query = """
        UPDATE surplusG1TBSE
        SET tbse_redev_trim_t2 = -tbse_redev_trim_i2
        WHERE id_projet = ?;
        """
        return self._execute_update(query, (id_projet,), "t2")
    
    def update_surplusG1TBSE_by_id_t1_t2_euro(self, id_projet: int) -> bool:
        """
        Met à jour tbse_redev_trim_t1_t2_euro = tbse_redev_trim_t1 + tbse_redev_trim_t2
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.project_exists(id_projet):
            logger.warning(f"Projet {id_projet} non trouvé")
            return False
            
        query = """
        UPDATE surplusG1TBSE
        SET tbse_redev_trim_t1_t2_euro = tbse_redev_trim_t1 + tbse_redev_trim_t2
        WHERE id_projet = ?;
        """
        return self._execute_update(query, (id_projet,), "t1_t2_euro")
    
    def update_single_operation(self, id_projet: int, operation: UpdateOperation) -> bool:
        """
        Met à jour une seule opération spécifiée
        
        Args:
            id_projet (int): L'identifiant du projet
            operation (UpdateOperation): L'opération à exécuter
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        operation_map = {
            UpdateOperation.I1: self.update_surplusG1TBSE_by_id_i1,
            UpdateOperation.I2: self.update_surplusG1TBSE_by_id_i2,
            UpdateOperation.T1: self.update_surplusG1TBSE_by_id_t1,
            UpdateOperation.T2: self.update_surplusG1TBSE_by_id_t2,
            UpdateOperation.T1_T2_EURO: self.update_surplusG1TBSE_by_id_t1_t2_euro
        }
        
        return operation_map[operation](id_projet)
    
    def update_all_operations(self, id_projet: int, stop_on_error: bool = True) -> Dict[str, bool]:
        """
        Exécute toutes les opérations de mise à jour pour un projet donné
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            stop_on_error (bool): Si True, arrête à la première erreur
            
        Returns:
            Dict[str, bool]: Résultat de chaque opération
        """
        logger.info(f"Début des mises à jour pour le projet {id_projet}")
        
        if not self.project_exists(id_projet):
            logger.error(f"Projet {id_projet} non trouvé - abandon de toutes les opérations")
            return {}
        
        operations = [
            ('i1', self.update_surplusG1TBSE_by_id_i1),
            ('i2', self.update_surplusG1TBSE_by_id_i2),
            ('t1', self.update_surplusG1TBSE_by_id_t1),
            ('t2', self.update_surplusG1TBSE_by_id_t2),
            ('t1_t2_euro', self.update_surplusG1TBSE_by_id_t1_t2_euro)
        ]
        
        results = {}
        
        for op_name, op_func in operations:
            try:
                result = op_func(id_projet)
                results[op_name] = result
                
                if not result and stop_on_error:
                    logger.error(f"Arrêt des opérations après l'échec de {op_name}")
                    break
                    
            except Exception as e:
                logger.error(f"Erreur lors de l'opération {op_name}: {e}")
                results[op_name] = False
                if stop_on_error:
                    break
        
        success_count = sum(results.values())
        total_ops = len(results)
        logger.info(f"Fin des mises à jour: {success_count}/{total_ops} opérations réussies")
        
        return results
    
    def update_multiple_projects(self, project_ids: List[int], stop_on_error: bool = False) -> Dict[int, Dict[str, bool]]:
        """
        Met à jour plusieurs projets
        
        Args:
            project_ids (List[int]): Liste des identifiants de projet
            stop_on_error (bool): Si True, arrête à la première erreur
            
        Returns:
            Dict[int, Dict[str, bool]]: Résultats pour chaque projet
        """
        all_results = {}
        
        for project_id in project_ids:
            logger.info(f"Traitement du projet {project_id}")
            try:
                results = self.update_all_operations(project_id, stop_on_error=False)
                all_results[project_id] = results
                
                if not any(results.values()) and stop_on_error:
                    logger.error(f"Arrêt du traitement après l'échec complet du projet {project_id}")
                    break
                    
            except Exception as e:
                logger.error(f"Erreur lors du traitement du projet {project_id}: {e}")
                all_results[project_id] = {}
                if stop_on_error:
                    break
        
        return all_results

def main():
    """Exemple d'utilisation avec mises à jour individuelles pour chaque opération"""
    
    print("=" * 70)
    print("SURPLUS G1 TBSE AXBB - MISES À JOUR INDIVIDUELLES")
    print("=" * 70)
    
    # Initialisation de la classe
    db_manager = SurplusG1TBSEAXBB("database.db")
    
    # ID du projet à traiter
    project_id = 1
    
    if not db_manager.project_exists(project_id):
        logger.error(f"Le projet {project_id} n'existe pas dans la base de données")
        return
    
    logger.info(f"Le projet {project_id} existe - début des mises à jour individuelles")
    print()
    
    # === MISES À JOUR INDIVIDUELLES ===
    
    print("--- 1. Mise à jour I1 (tbse_redev_trim_i1 = tbse_redev_i1 * 90) ---")
    success_i1 = db_manager.update_surplusG1TBSE_by_id_i1(project_id)
    status_i1 = "✅ RÉUSSIE" if success_i1 else "❌ ÉCHOUÉE"
    print(f"Résultat: {status_i1}")
    print()
    
    print("--- 2. Mise à jour I2 (tbse_redev_trim_i2 = tbse_redev_i2 * 90) ---")
    success_i2 = db_manager.update_surplusG1TBSE_by_id_i2(project_id)
    status_i2 = "✅ RÉUSSIE" if success_i2 else "❌ ÉCHOUÉE"
    print(f"Résultat: {status_i2}")
    print()
    
    print("--- 3. Mise à jour T1 (tbse_redev_trim_t1 = tbse_redev_trim_i1) ---")
    success_t1 = db_manager.update_surplusG1TBSE_by_id_t1(project_id)
    status_t1 = "✅ RÉUSSIE" if success_t1 else "❌ ÉCHOUÉE"
    print(f"Résultat: {status_t1}")
    print()
    
    print("--- 4. Mise à jour T2 (tbse_redev_trim_t2 = -tbse_redev_trim_i2) ---")
    success_t2 = db_manager.update_surplusG1TBSE_by_id_t2(project_id)
    status_t2 = "✅ RÉUSSIE" if success_t2 else "❌ ÉCHOUÉE"
    print(f"Résultat: {status_t2}")
    print()
    
    print("--- 5. Mise à jour T1_T2_EURO (tbse_redev_trim_t1_t2_euro = tbse_redev_trim_t1 + tbse_redev_trim_t2) ---")
    success_t1_t2_euro = db_manager.update_surplusG1TBSE_by_id_t1_t2_euro(project_id)
    status_t1_t2_euro = "✅ RÉUSSIE" if success_t1_t2_euro else "❌ ÉCHOUÉE"
    print(f"Résultat: {status_t1_t2_euro}")
    print()
    
    # === RÉSUMÉ FINAL ===
    
    results = {
        'I1': success_i1,
        'I2': success_i2,
        'T1': success_t1,
        'T2': success_t2,
        'T1_T2_EURO': success_t1_t2_euro
    }
    
    success_count = sum(results.values())
    total_operations = len(results)
    
    print("=" * 70)
    print("RÉSUMÉ DES OPÉRATIONS")
    print("=" * 70)
    
    for operation, success in results.items():
        status = "✅ RÉUSSIE" if success else "❌ ÉCHOUÉE"
        print(f"{operation:15} : {status}")
    
    print()
    print(f"TOTAL : {success_count}/{total_operations} opérations réussies")
    
    if success_count == total_operations:
        print("🎉 TOUTES LES OPÉRATIONS ONT RÉUSSI !")
    elif success_count > 0:
        print("⚠️  QUELQUES OPÉRATIONS ONT ÉCHOUÉ")
    else:
        print("💥 TOUTES LES OPÉRATIONS ONT ÉCHOUÉ")

if __name__ == "__main__":
    main()