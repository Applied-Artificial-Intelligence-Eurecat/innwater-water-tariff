import sqlite3
from typing import Optional, Dict, List, Any, Tuple
import logging

class surplusATabBuilder:
    """
    Classe pour gérer une table SQLite contenant les données de surplus agrégé
    avec un schéma complexe incluant les calculs de coûts et consommations.
    """
    
    def __init__(self, table_name: str = "surplusagrege", db_name: str = "database.db"):
        """
        Initialise la connexion à la base de données SQLite.
        
        Args:
            table_name (str): Nom de la table à créer/gérer
            db_name (str): Nom de la base de données SQLite (par défaut: database.db)
        """
        self.db_name = db_name
        self.db_path = db_name  # Pour maintenir la compatibilité avec le reste du code
        self.table_name = table_name
        self.connection = None
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Affichage des informations dans __init__
        self.logger.info(f"Initialisation avec base de données: {self.db_name}")
        self.logger.info(f"Nom de la table: {self.table_name}")
    
    def connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
            self.logger.info(f"Connexion établie à la base de données: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la connexion: {e}")
            raise
    
    def disconnect(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            self.connection.close()
            self.logger.info("Connexion fermée")
    
    def drop_table_if_exists(self):
        """
        Supprime la table si elle existe déjà.
        """
        drop_table_sql = f"DROP TABLE IF EXISTS {self.table_name};"
        
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(drop_table_sql)
            self.connection.commit()
            self.logger.info(f"Table '{self.table_name}' supprimée si elle existait")
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la suppression de la table: {e}")
            raise
    
    def create_table(self, drop_if_exists: bool = True):
        """
        Crée la table avec le schéma spécifié.
        Utilise des types de données appropriés pour chaque colonne.
        
        Args:
            drop_if_exists (bool): Si True, supprime la table existante avant de la recréer
        """
        # Supprimer la table si demandé
        if drop_if_exists:
            self.drop_table_if_exists()
        
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            -- Identifiants principaux
            id_projet INTEGER PRIMARY KEY,
            menage INTEGER,
            assaini INTEGER,
            menages_pauvres INTEGER,
            
            -- Consommation de base
            consommation_eau_m3_trimestre REAL,
            
            -- Coûts TBSE HT (Hors Taxes)
            c_tbse_a_ht_qb_m3_trim REAL,
            c_tbse_a_ht_i1 REAL,
            c_tbse_a_ht_i2 REAL,
            c_tbse_a_ht_t1 REAL,
            c_tbse_a_ht_t2 REAL,
            c_tbse_a_ht_t1_t2_eur_trim REAL,
            
            -- Coûts TBSE Redevance
            c_tbse_a_redev_qb_m3_trim REAL,
            c_tbse_a_redev_i1 REAL,
            c_tbse_a_redev_i2 REAL,
            c_tbse_a_redev_t1 REAL,
            c_tbse_a_redev_t2 REAL,
            c_tbse_a_redev_t1_t2_eur_trim REAL,
            
            -- Coûts TBSE TTC (Toutes Taxes Comprises)
            c_tbse_a_ttc_qb_m3_trim REAL,
            c_tbse_a_ttc_i1 REAL,
            c_tbse_a_ttc_i2 REAL,
            c_tbse_a_ttc_t1 REAL,
            c_tbse_a_ttc_t2 REAL,
            c_tbse_a_ttc_t1_t2_eur_trim REAL,
            
            -- Différentiels et références
            diff_quantile_ref REAL,
            
            -- Coûts IBT HT (Increasing Block Tariff - Hors Taxes)
            c_ibt_a_ht_c_ht_pp REAL,
            c_ibt_a_ht_surco REAL,
            c_ibt_a_ht_c_ht_surco REAL,
            c_ibt_a_ht_pp_i1 REAL,
            c_ibt_a_ht_pp_i2 REAL,
            c_ibt_a_ht_pp_t1 REAL,
            c_ibt_a_ht_pp_t2 REAL,
            c_ibt_a_ht_pp_t1_t2_eur_trim REAL,
            c_ibt_a_ht_mp_i1 REAL,
            c_ibt_a_ht_mp_i2 REAL,
            c_ibt_a_ht_mp_t1 REAL,
            c_ibt_a_ht_mp_t2 REAL,
            c_ibt_a_ht_mp_t1_t2_eur_trim REAL,
            
            -- Coûts IBT Redevance
            c_ibt_a_redev_conso_red_ht REAL,
            c_ibt_a_redev_surconso REAL,
            c_ibt_a_redev_conso_surpercept REAL,
            c_ibt_a_redev_pp_i1 REAL,
            c_ibt_a_redev_pp_i2 REAL,
            c_ibt_a_redev_pp_t1 REAL,
            c_ibt_a_redev_pp_t2 REAL,
            c_ibt_a_redev_pp_t1_t2_eur_trim REAL,
            c_ibt_a_redev_mp_i1 REAL,
            c_ibt_a_redev_mp_i2 REAL,
            c_ibt_a_redev_mp_t1 REAL,
            c_ibt_a_redev_mp_t2 REAL,
            c_ibt_a_redev_mp_t1_t2_eur_trim REAL,
            
            -- Coûts IBT TTC
            c_ibt_a_ttc_c_finale_ttc REAL,
            c_ibt_a_ttc_surco REAL,
            c_ibt_a_ttc_c_surpercept REAL,
            c_ibt_a_ttc_d_ibt_a REAL,
            c_ibt_a_ttc_cout_env_non_recup REAL,
            c_ibt_a_ttc_recup_1 REAL,
            c_ibt_a_ttc_non_recup_1 REAL,
            c_ibt_a_ttc_pp_i1 REAL,
            c_ibt_a_ttc_pp_i2 REAL,
            c_ibt_a_ttc_pp_t1 REAL,
            c_ibt_a_ttc_pp_t2 REAL,
            c_ibt_a_ttc_pp_t1_t2_eur_trim REAL,
            c_ibt_a_ttc_mp_i1 REAL,
            c_ibt_a_ttc_mp_i2 REAL,
            c_ibt_a_ttc_mp_t1 REAL,
            c_ibt_a_ttc_mp_t2 REAL,
            c_ibt_a_ttc_mp_t1_t2_eur_trim REAL,
            
            -- Indicateurs d'optimisation
            sous_opt INTEGER,
            sur_opt INTEGER,
            opt_egal INTEGER,
            
            -- Statistiques de consommation
            surconso_menages INTEGER,
            sous_conso_menages INTEGER,
            ecart_ibt_moins REAL,
            ecart_ibt_plus REAL,
            
            -- Agrégations et coûts négatifs
            sous_conso_spl_agreg_ibt_neg REAL,
            sous_conso_spl_brut_ibt_neg REAL,
            sous_conso_cout_ibt_neg REAL,
            surconso_approx_spl_agreg_ibt_pos REAL,
            surconso_approx_spl_brut_ibt_pos REAL,
            surconso_approx_cout_ibt_pos REAL
        );
        """
        
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            self.logger.info(f"Table '{self.table_name}' créée avec succès")
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la création de la table: {e}")
            raise
    
    def insert_data(self, data: Dict[str, Any]) -> int:
        """
        Insère une ligne de données dans la table.
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les données à insérer
            
        Returns:
            int: ID du projet inséré
        """
        # Liste de toutes les colonnes (sans id_projet qui est auto-incrémenté)
        columns = [
            'menage', 'assaini', 'menages_pauvres', 'consommation_eau_m3_trimestre',
            'c_tbse_a_ht_qb_m3_trim', 'c_tbse_a_ht_i1', 'c_tbse_a_ht_i2',
            'c_tbse_a_ht_t1', 'c_tbse_a_ht_t2', 'c_tbse_a_ht_t1_t2_eur_trim',
            'c_tbse_a_redev_qb_m3_trim', 'c_tbse_a_redev_i1', 'c_tbse_a_redev_i2',
            'c_tbse_a_redev_t1', 'c_tbse_a_redev_t2', 'c_tbse_a_redev_t1_t2_eur_trim',
            'c_tbse_a_ttc_qb_m3_trim', 'c_tbse_a_ttc_i1', 'c_tbse_a_ttc_i2',
            'c_tbse_a_ttc_t1', 'c_tbse_a_ttc_t2', 'c_tbse_a_ttc_t1_t2_eur_trim',
            'diff_quantile_ref', 'c_ibt_a_ht_c_ht_pp', 'c_ibt_a_ht_surco',
            'c_ibt_a_ht_c_ht_surco', 'c_ibt_a_ht_pp_i1', 'c_ibt_a_ht_pp_i2',
            'c_ibt_a_ht_pp_t1', 'c_ibt_a_ht_pp_t2', 'c_ibt_a_ht_pp_t1_t2_eur_trim',
            'c_ibt_a_ht_mp_i1', 'c_ibt_a_ht_mp_i2', 'c_ibt_a_ht_mp_t1',
            'c_ibt_a_ht_mp_t2', 'c_ibt_a_ht_mp_t1_t2_eur_trim',
            'c_ibt_a_redev_conso_red_ht', 'c_ibt_a_redev_surconso',
            'c_ibt_a_redev_conso_surpercept', 'c_ibt_a_redev_pp_i1',
            'c_ibt_a_redev_pp_i2', 'c_ibt_a_redev_pp_t1', 'c_ibt_a_redev_pp_t2',
            'c_ibt_a_redev_pp_t1_t2_eur_trim', 'c_ibt_a_redev_mp_i1',
            'c_ibt_a_redev_mp_i2', 'c_ibt_a_redev_mp_t1', 'c_ibt_a_redev_mp_t2',
            'c_ibt_a_redev_mp_t1_t2_eur_trim', 'c_ibt_a_ttc_c_finale_ttc',
            'c_ibt_a_ttc_surco', 'c_ibt_a_ttc_c_surpercept', 'c_ibt_a_ttc_d_ibt_a',
            'c_ibt_a_ttc_cout_env_non_recup', 'c_ibt_a_ttc_recup_1',
            'c_ibt_a_ttc_non_recup_1', 'c_ibt_a_ttc_pp_i1', 'c_ibt_a_ttc_pp_i2',
            'c_ibt_a_ttc_pp_t1', 'c_ibt_a_ttc_pp_t2', 'c_ibt_a_ttc_pp_t1_t2_eur_trim',
            'c_ibt_a_ttc_mp_i1', 'c_ibt_a_ttc_mp_i2', 'c_ibt_a_ttc_mp_t1',
            'c_ibt_a_ttc_mp_t2', 'c_ibt_a_ttc_mp_t1_t2_eur_trim', 'sous_opt',
            'sur_opt', 'opt_egal', 'surconso_menages', 'sous_conso_menages',
            'ecart_ibt_moins', 'ecart_ibt_plus', 'sous_conso_spl_agreg_ibt_neg',
            'sous_conso_spl_brut_ibt_neg', 'sous_conso_cout_ibt_neg',
            'surconso_approx_spl_agreg_ibt_pos', 'surconso_approx_spl_brut_ibt_pos',
            'surconso_approx_cout_ibt_pos'
        ]
        
        # Filtrer les colonnes présentes dans les données
        available_columns = [col for col in columns if col in data]
        values = [data[col] for col in available_columns]
        
        placeholders = ','.join(['?' for _ in available_columns])
        columns_str = ','.join(available_columns)
        
        insert_sql = f"""
        INSERT INTO {self.table_name} ({columns_str})
        VALUES ({placeholders})
        """
        
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, values)
            self.connection.commit()
            
            project_id = cursor.lastrowid
            self.logger.info(f"Données insérées avec succès. ID projet: {project_id}")
            return project_id
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'insertion: {e}")
            raise
    
    def insert_batch(self, data_list: List[Dict[str, Any]]) -> List[int]:
        """
        Insère plusieurs lignes de données en batch.
        
        Args:
            data_list (List[Dict[str, Any]]): Liste de dictionnaires de données
            
        Returns:
            List[int]: Liste des IDs des projets insérés
        """
        inserted_ids = []
        
        try:
            if not self.connection:
                self.connect()
            
            for data in data_list:
                project_id = self.insert_data(data)
                inserted_ids.append(project_id)
            
            self.logger.info(f"{len(inserted_ids)} enregistrements insérés en batch")
            return inserted_ids
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'insertion en batch: {e}")
            raise
    
    def get_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un projet par son ID.
        
        Args:
            project_id (int): ID du projet
            
        Returns:
            Optional[Dict[str, Any]]: Dictionnaire des données ou None
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id_projet = ?", (project_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la récupération: {e}")
            raise
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Récupère tous les projets.
        
        Args:
            limit (Optional[int]): Limite du nombre de résultats
            
        Returns:
            List[Dict[str, Any]]: Liste des projets
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            sql = f"SELECT * FROM {self.table_name}"
            if limit:
                sql += f" LIMIT {limit}"
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la récupération: {e}")
            raise
    
    def update_data(self, project_id: int, data: Dict[str, Any]) -> bool:
        """
        Met à jour un projet existant.
        
        Args:
            project_id (int): ID du projet à mettre à jour
            data (Dict[str, Any]): Nouvelles données
            
        Returns:
            bool: True si la mise à jour a réussi
        """
        try:
            if not self.connection:
                self.connect()
            
            # Construire la requête de mise à jour
            set_clauses = []
            values = []
            
            for column, value in data.items():
                if column != 'id_projet':  # Ne pas permettre de modifier l'ID
                    set_clauses.append(f"{column} = ?")
                    values.append(value)
            
            if not set_clauses:
                self.logger.warning("Aucune donnée à mettre à jour")
                return False
            
            values.append(project_id)  # Pour la clause WHERE
            
            update_sql = f"""
            UPDATE {self.table_name} 
            SET {', '.join(set_clauses)} 
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(update_sql, values)
            self.connection.commit()
            
            if cursor.rowcount > 0:
                self.logger.info(f"Projet {project_id} mis à jour avec succès")
                return True
            else:
                self.logger.warning(f"Aucun projet trouvé avec l'ID {project_id}")
                return False
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la mise à jour: {e}")
            raise
    
    def delete_data(self, project_id: int) -> bool:
        """
        Supprime un projet.
        
        Args:
            project_id (int): ID du projet à supprimer
            
        Returns:
            bool: True si la suppression a réussi
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id_projet = ?", (project_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                self.logger.info(f"Projet {project_id} supprimé avec succès")
                return True
            else:
                self.logger.warning(f"Aucun projet trouvé avec l'ID {project_id}")
                return False
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la suppression: {e}")
            raise
    
    def get_count(self) -> int:
        """
        Retourne le nombre total d'enregistrements.
        
        Returns:
            int: Nombre d'enregistrements
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            return cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors du comptage: {e}")
            raise
    
    def __enter__(self):
        """Support pour l'utilisation avec 'with' statement."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fermeture automatique de la connexion."""
        self.disconnect()


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une instance et utiliser la classe
    db = surplusATabBuilder("surplusagrege", "database.db")
    
    try:
        # Créer la table (supprime la table existante par défaut)
        db.create_table()
        
    
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        db.disconnect()