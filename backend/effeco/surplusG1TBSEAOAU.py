import sqlite3
import logging
from typing import Optional, Any, List

class DatabaseManager:
    def __init__(self, db_path: str = "database.db"):
        """
        Initialise la classe avec le chemin de la base de données
        
        Args:
            db_path (str): Chemin vers le fichier de base de données SQLite
        """
        self.db_path = db_path
        self.connection = None
        self.setup_logging()
    
    def setup_logging(self):
        """Configure le système de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asceptime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """
        Établit une connexion à la base de données
        
        Returns:
            bool: True si la connexion réussit, False sinon
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dictionnaire
            self.logger.info(f"Connexion à la base de données {self.db_path} établie")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.logger.info("Connexion à la base de données fermée")
    
    def __enter__(self):
        """Permet d'utiliser la classe avec un context manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme la connexion à la fin du context manager"""
        self.disconnect()
    
    def update_surplusG1TBSE(self) -> Optional[int]:
        """
        Exécute la requête UPDATE sur la table surplusG1TBSE
        
        Returns:
            Optional[int]: Nombre de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            # Requête SQL avec la formule spécifiée
            sql_query = """
            UPDATE surplusG1TBSE
            SET ln_qb_avec_redev = 
                LN(c_m3_trim_1 / 90) 
                + (0.25 * LN(revenu_net_mois / 30)) 
                - (ABS(-0.31) * LN(0.9 + 0.12))
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour ln_qb_avec_redev réussie. {rows_affected} lignes affectées.")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour ln_qb_avec_redev: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def update_tbse_redev_qb_m3_jour(self, id_projet: int) -> Optional[int]:
        """
        Met à jour tbse_redev_qb_m3_jour avec EXP(ln_qb_avec_redev) pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_qb_m3_jour = EXP(ln_qb_avec_redev)
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour tbse_redev_qb_m3_jour réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour tbse_redev_qb_m3_jour: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_qb_avec_redev_sans_tva(self, id_projet: int) -> Optional[int]:
        """
        Met à jour qb_avec_redev_sans_tva avec tbse_redev_qb_m3_jour * 90 pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET qb_avec_redev_sans_tva = tbse_redev_qb_m3_jour * 90
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour qb_avec_redev_sans_tva réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour qb_avec_redev_sans_tva: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_i1(self, id_projet: int) -> Optional[int]:
        """
        Met à jour tbse_redev_i1 avec la formule complexe pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_i1 = 
                (0.31 * demande_inverse_bi) / (1 - 0.31) *
                (
                    POWER(qstar_m3_jour, -((1 - 0.31) / 0.31)) 
                    - POWER(tbse_redev_qb_m3_jour, -((1 - 0.31) / 0.31))
                )
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour tbse_redev_i1 réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour tbse_redev_i1: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_i2(self, id_projet: int) -> Optional[int]:
        """
        Met à jour tbse_redev_i2 avec 5.9 * (tbse_redev_qb_m3_jour - qstar_m3_jour) pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_i2 = 5.9 * (tbse_redev_qb_m3_jour - qstar_m3_jour)
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour tbse_redev_i2 réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour tbse_redev_i2: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_t1(self, id_projet: int) -> Optional[int]:
        """
        Met à jour tbse_redev_t1 avec la valeur de tbse_redev_i1 pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_t1 = tbse_redev_i1
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour tbse_redev_t1 réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour tbse_redev_t1: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_t2(self, id_projet: int) -> Optional[int]:
        """
        Met à jour tbse_redev_t2 avec -tbse_redev_i2 pour un id_projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            Optional[int]: Nombre de lignes affectées (1 si succès) ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_t2 = -tbse_redev_i2
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            if rows_affected > 0:
                self.logger.info(f"Mise à jour tbse_redev_t2 réussie pour id_projet {id_projet}")
            else:
                self.logger.warning(f"Aucune ligne trouvée avec id_projet {id_projet}")
                
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour tbse_redev_t2: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def update_tbse_redev_for_all_projects(self) -> Optional[int]:
        """
        Met à jour tbse_redev_qb_m3_jour pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_qb_m3_jour = EXP(ln_qb_avec_redev)
            WHERE ln_qb_avec_redev IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour tbse_redev_qb_m3_jour réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale tbse_redev_qb_m3_jour: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_qb_avec_redev_sans_tva_for_all_projects(self) -> Optional[int]:
        """
        Met à jour qb_avec_redev_sans_tva pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET qb_avec_redev_sans_tva = tbse_redev_qb_m3_jour * 90
            WHERE tbse_redev_qb_m3_jour IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour qb_avec_redev_sans_tva réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale qb_avec_redev_sans_tva: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_i1_for_all_projects(self) -> Optional[int]:
        """
        Met à jour tbse_redev_i1 pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_i1 = 
                (0.31 * demande_inverse_bi) / (1 - 0.31) *
                (
                    POWER(qstar_m3_jour, -((1 - 0.31) / 0.31)) 
                    - POWER(tbse_redev_qb_m3_jour, -((1 - 0.31) / 0.31))
                )
            WHERE demande_inverse_bi IS NOT NULL 
                AND qstar_m3_jour IS NOT NULL 
                AND tbse_redev_qb_m3_jour IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour tbse_redev_i1 réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale tbse_redev_i1: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_i2_for_all_projects(self) -> Optional[int]:
        """
        Met à jour tbse_redev_i2 pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_i2 = 5.9 * (tbse_redev_qb_m3_jour - qstar_m3_jour)
            WHERE tbse_redev_qb_m3_jour IS NOT NULL 
                AND qstar_m3_jour IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour tbse_redev_i2 réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale tbse_redev_i2: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_t1_for_all_projects(self) -> Optional[int]:
        """
        Met à jour tbse_redev_t1 pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_t1 = tbse_redev_i1
            WHERE tbse_redev_i1 IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour tbse_redev_t1 réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale tbse_redev_t1: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def update_tbse_redev_t2_for_all_projects(self) -> Optional[int]:
        """
        Met à jour tbse_redev_t2 pour tous les projets
        
        Returns:
            Optional[int]: Nombre total de lignes affectées ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            UPDATE surplusG1TBSE
            SET tbse_redev_t2 = -tbse_redev_i2
            WHERE tbse_redev_i2 IS NOT NULL
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            rows_affected = cursor.rowcount
            self.connection.commit()
            
            self.logger.info(f"Mise à jour tbse_redev_t2 réussie pour {rows_affected} projets")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour globale tbse_redev_t2: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def get_project_info(self, id_projet: int) -> Optional[dict]:
        """
        Récupère les informations d'un projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet
            
        Returns:
            Optional[dict]: Dictionnaire avec les informations du projet ou None si non trouvé
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            sql_query = """
            SELECT * FROM surplusG1TBSE WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(sql_query, (id_projet,))
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            else:
                self.logger.warning(f"Aucun projet trouvé avec id_projet {id_projet}")
                return None
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la récupération du projet: {e}")
            return None

    def execute_all_updates_for_project(self, id_projet: int) -> dict:
        """
        Exécute toutes les mises à jour pour un projet spécifique dans l'ordre logique
        
        Args:
            id_projet (int): L'identifiant du projet
            
        Returns:
            dict: Résumé des mises à jour effectuées
        """
        results = {
            'id_projet': id_projet,
            'ln_qb_avec_redev_updated': False,
            'tbse_redev_updated': False,
            'qb_sans_tva_updated': False,
            'tbse_redev_i1_updated': False,
            'tbse_redev_i2_updated': False,
            'tbse_redev_t1_updated': False,
            'tbse_redev_t2_updated': False,
            'errors': []
        }
        
        try:
            # 1. Mise à jour ln_qb_avec_redev (si nécessaire)
            ln_result = self.update_surplusG1TBSE()
            if ln_result is not None:
                results['ln_qb_avec_redev_updated'] = True
            
            # 2. Mise à jour tbse_redev_qb_m3_jour
            tbse_result = self.update_tbse_redev_qb_m3_jour(id_projet)
            if tbse_result == 1:
                results['tbse_redev_updated'] = True
            elif tbse_result is None:
                results['errors'].append('Erreur lors de la mise à jour tbse_redev_qb_m3_jour')
            
            # 3. Mise à jour qb_avec_redev_sans_tva
            qb_result = self.update_qb_avec_redev_sans_tva(id_projet)
            if qb_result == 1:
                results['qb_sans_tva_updated'] = True
            elif qb_result is None:
                results['errors'].append('Erreur lors de la mise à jour qb_avec_redev_sans_tva')
            
            # 4. Mise à jour tbse_redev_i1
            i1_result = self.update_tbse_redev_i1(id_projet)
            if i1_result == 1:
                results['tbse_redev_i1_updated'] = True
            elif i1_result is None:
                results['errors'].append('Erreur lors de la mise à jour tbse_redev_i1')
            
            # 5. Mise à jour tbse_redev_i2
            i2_result = self.update_tbse_redev_i2(id_projet)
            if i2_result == 1:
                results['tbse_redev_i2_updated'] = True
            elif i2_result is None:
                results['errors'].append('Erreur lors de la mise à jour tbse_redev_i2')
            
            # 6. Mise à jour tbse_redev_t1
            t1_result = self.update_tbse_redev_t1(id_projet)
            if t1_result == 1:
                results['tbse_redev_t1_updated'] = True
            elif t1_result is None:
                results['errors'].append('Erreur lors de la mise à jour tbse_redev_t1')
            
            # 7. Mise à jour tbse_redev_t2
            t2_result = self.update_tbse_redev_t2(id_projet)
            if t2_result == 1:
                results['tbse_redev_t2_updated'] = True
            elif t2_result is None:
                results['errors'].append('Erreur lors de la mise à jour tbse_redev_t2')
            
            return results
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de toutes les mises à jour: {e}")
            results['errors'].append(str(e))
            return results

    def check_required_columns(self, id_projet: int, calculation_type: str = "all") -> dict:
        """
        Vérifie si les colonnes requises pour les calculs sont présentes et non nulles
        
        Args:
            id_projet (int): L'identifiant du projet
            calculation_type (str): Type de calcul à vérifier ("i1", "i2", "t1", "t2", "all")
            
        Returns:
            dict: Statut de présence des colonnes requises
        """
        project_info = self.get_project_info(id_projet)
        if not project_info:
            return {'has_all_required': False, 'missing_columns': ['projet_non_trouve']}
        
        required_columns = []
        
        if calculation_type in ["i1", "all"]:
            required_columns.extend(['demande_inverse_bi', 'qstar_m3_jour', 'tbse_redev_qb_m3_jour'])
        
        if calculation_type in ["i2", "all"]:
            required_columns.extend(['tbse_redev_qb_m3_jour', 'qstar_m3_jour'])
        
        if calculation_type in ["t1", "all"]:
            required_columns.extend(['tbse_redev_i1'])
        
        if calculation_type in ["t2", "all"]:
            required_columns.extend(['tbse_redev_i2'])
        
        # Supprimer les doublons
        required_columns = list(set(required_columns))
        missing_columns = []
        
        for column in required_columns:
            if column not in project_info or project_info[column] is None:
                missing_columns.append(column)
        
        return {
            'has_all_required': len(missing_columns) == 0,
            'missing_columns': missing_columns,
            'project_exists': True,
            'calculation_type': calculation_type
        }
    
    def execute_custom_query(self, query: str, params: tuple = ()) -> Optional[Any]:
        """
        Exécute une requête SQL personnalisée
        
        Args:
            query (str): Requête SQL à exécuter
            params (tuple): Paramètres pour la requête préparée
            
        Returns:
            Résultats de la requête ou None en cas d'erreur
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                self.logger.info(f"Requête SELECT exécutée. {len(results)} résultats.")
                return [dict(row) for row in results]
            else:
                rows_affected = cursor.rowcount
                self.connection.commit()
                self.logger.info(f"Requête exécutée. {rows_affected} lignes affectées.")
                return rows_affected
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            if self.connection:
                self.connection.rollback()
            return None

# Exemple d'utilisation
if __name__ == "__main__":
    # Utilisation avec context manager (recommandé)
    with DatabaseManager("database.db") as db_manager:
        id_projet_test = 123  # Remplacez par un ID réel
        
        # Vérification des colonnes requises pour t2
        check_result = db_manager.check_required_columns(id_projet_test, "t2")
        print(f"🔍 Vérification des colonnes requises pour tbse_redev_t2: {check_result}")
        
        if not check_result['has_all_required']:
            print(f"⚠️  Colonnes manquantes: {check_result['missing_columns']}")
        
        # Méthode 1: Mise à jour individuelle
        print("\n🔧 Mise à jour individuelle des champs:")
        
        # 1. Mise à jour initiale de ln_qb_avec_redev pour tous les projets
        rows_updated = db_manager.update_surplusG1TBSE()
        print(f"✅ Mise à jour ln_qb_avec_redev : {rows_updated} lignes modifiées")
        
        # 2. Mise à jour de tbse_redev_qb_m3_jour pour un projet spécifique
        rows_updated = db_manager.update_tbse_redev_qb_m3_jour(id_projet_test)
        print(f"✅ Mise à jour tbse_redev_qb_m3_jour : {rows_updated} lignes modifiées")
        
        # 3. Mise à jour de qb_avec_redev_sans_tva pour un projet spécifique
        rows_updated = db_manager.update_qb_avec_redev_sans_tva(id_projet_test)
        print(f"✅ Mise à jour qb_avec_redev_sans_tva : {rows_updated} lignes modifiées")
        
        # 4. Mise à jour de tbse_redev_i1 pour un projet spécifique
        rows_updated = db_manager.update_tbse_redev_i1(id_projet_test)
        print(f"✅ Mise à jour tbse_redev_i1 : {rows_updated} lignes modifiées")
        
        # 5. Mise à jour de tbse_redev_i2 pour un projet spécifique
        rows_updated = db_manager.update_tbse_redev_i2(id_projet_test)
        print(f"✅ Mise à jour tbse_redev_i2 : {rows_updated} lignes modifiées")
        
        # 6. Mise à jour de tbse_redev_t1 pour un projet spécifique
        rows_updated = db_manager.update_tbse_redev_t1(id_projet_test)
        print(f"✅ Mise à jour tbse_redev_t1 : {rows_updated} lignes modifiées")
        
        # 7. Mise à jour de tbse_redev_t2 pour un projet spécifique
        rows_updated = db_manager.update_tbse_redev_t2(id_projet_test)
        print(f"✅ Mise à jour tbse_redev_t2 : {rows_updated} lignes modifiées")
        
        # Méthode 2: Mise à jour en une seule fois
        print("\n🚀 Mise à jour complète du projet:")
        results = db_manager.execute_all_updates_for_project(id_projet_test)
        print(f"Résultats pour le projet {id_projet_test}: {results}")
        
        # Vérification des données
        project_info = db_manager.get_project_info(id_projet_test)
        if project_info:
            print(f"\n📊 Données du projet {id_projet_test}:")
            print(f"   ln_qb_avec_redev: {project_info.get('ln_qb_avec_redev')}")
            print(f"   tbse_redev_qb_m3_jour: {project_info.get('tbse_redev_qb_m3_jour')}")
            print(f"   qb_avec_redev_sans_tva: {project_info.get('qb_avec_redev_sans_tva')}")
            print(f"   tbse_redev_i1: {project_info.get('tbse_redev_i1')}")
            print(f"   tbse_redev_i2: {project_info.get('tbse_redev_i2')}")
            print(f"   tbse_redev_t1: {project_info.get('tbse_redev_t1')}")
            print(f"   tbse_redev_t2: {project_info.get('tbse_redev_t2')}")
            print(f"   demande_inverse_bi: {project_info.get('demande_inverse_bi')}")
            print(f"   qstar_m3_jour: {project_info.get('qstar_m3_jour')}")