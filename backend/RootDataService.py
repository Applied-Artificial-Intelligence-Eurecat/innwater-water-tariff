import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
import logging

class RootDataService:
    """
    Service pour récupérer les données de la table la_reunion_data 
    et les convertir en DataFrame pandas.
    """
    
    def __init__(self, db_path: str = "database.db", default_id_projet: int = 1):
        """
        Initialise le service avec le chemin vers la base de données.
        
        Args:
            db_path (str): Chemin vers le fichier de base de données SQLite
            default_id_projet (int): ID de projet par défaut pour les requêtes
        """
        self.db_path = db_path
        self.table_name = "la_reunion_data"
        self.default_id_projet = default_id_projet
        self.logger = logging.getLogger(__name__)
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Crée et retourne une connexion à la base de données.
        
        Returns:
            sqlite3.Connection: Connexion à la base de données
        """
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la connexion à la base de données: {e}")
            raise
    
    def get_all_data(self, id_projet: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère toutes les données de la table la_reunion_data pour un projet donné.
        
        Args:
            id_projet (Optional[int]): ID du projet. Si None, utilise la valeur par défaut
        
        Returns:
            pd.DataFrame: DataFrame contenant toutes les données du projet
        """
        project_id = id_projet if id_projet is not None else self.default_id_projet
        query = f"SELECT * FROM {self.table_name} WHERE id_projet = ?"
        return self._execute_query(query, [project_id])
    
    def get_all_data_all_projects(self) -> pd.DataFrame:
        """
        Récupère toutes les données de la table pour tous les projets.
        
        Returns:
            pd.DataFrame: DataFrame contenant toutes les données de tous les projets
        """
        query = f"SELECT * FROM {self.table_name}"
        return self._execute_query(query)
    
    def get_data_by_conditions(self, conditions: Dict[str, Any], id_projet: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère les données avec des conditions WHERE pour un projet donné.
        
        Args:
            conditions (Dict[str, Any]): Dictionnaire des conditions
                Exemple: {"revenu": 50000, "maison (1 = oui)": 1}
            id_projet (Optional[int]): ID du projet. Si None, utilise la valeur par défaut
        
        Returns:
            pd.DataFrame: DataFrame filtré selon les conditions
        """
        project_id = id_projet if id_projet is not None else self.default_id_projet
        
        if not conditions:
            return self.get_all_data(project_id)
        
        where_clauses = ['id_projet = ?']
        params = [project_id]
        
        for column, value in conditions.items():
            if isinstance(value, (list, tuple)):
                placeholders = ','.join(['?' for _ in value])
                where_clauses.append(f'"{column}" IN ({placeholders})')
                params.extend(value)
            else:
                where_clauses.append(f'"{column}" = ?')
                params.append(value)
        
        where_clause = " AND ".join(where_clauses)
        query = f'SELECT * FROM {self.table_name} WHERE {where_clause}'
        
        return self._execute_query(query, params)
    
    def get_data_by_id_projet(self, id_projet: int) -> pd.DataFrame:
        """
        Récupère les données pour un id_projet spécifique.
        
        Args:
            id_projet (int): ID du projet
        
        Returns:
            pd.DataFrame: DataFrame filtré par id_projet
        """
        query = f"SELECT * FROM {self.table_name} WHERE id_projet = ?"
        return self._execute_query(query, [id_projet])
    
    def get_data_with_limit(self, limit: int = 100, offset: int = 0, id_projet: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère un nombre limité de données avec pagination pour un projet donné.
        
        Args:
            limit (int): Nombre maximum de lignes à retourner
            offset (int): Nombre de lignes à ignorer
            id_projet (Optional[int]): ID du projet. Si None, utilise la valeur par défaut
        
        Returns:
            pd.DataFrame: DataFrame paginé
        """
        project_id = id_projet if id_projet is not None else self.default_id_projet
        query = f"SELECT * FROM {self.table_name} WHERE id_projet = ? LIMIT ? OFFSET ?"
        return self._execute_query(query, [project_id, limit, offset])
    
    def get_columns_info(self) -> pd.DataFrame:
        """
        Récupère les informations sur les colonnes de la table.
        
        Returns:
            pd.DataFrame: DataFrame avec les informations des colonnes
        """
        query = f"PRAGMA table_info({self.table_name})"
        return self._execute_query(query)
    
    def get_statistics(self, id_projet: Optional[int] = None) -> Dict[str, Any]:
        """
        Récupère des statistiques de base sur la table pour un projet donné.
        
        Args:
            id_projet (Optional[int]): ID du projet. Si None, utilise la valeur par défaut
        
        Returns:
            Dict[str, Any]: Dictionnaire contenant les statistiques
        """
        project_id = id_projet if id_projet is not None else self.default_id_projet
        stats = {}
        
        # Nombre total de lignes pour le projet
        count_query = f"SELECT COUNT(*) as total_rows FROM {self.table_name} WHERE id_projet = ?"
        count_df = self._execute_query(count_query, [project_id])
        stats['total_rows'] = count_df.iloc[0]['total_rows']
        stats['id_projet'] = project_id
        
        # Statistiques sur quelques colonnes numériques importantes
        numeric_columns = ['revenu', 'nbpers', 'nenf', 'naa (Nombre d\'adultes actifs)']
        
        for col in numeric_columns:
            try:
                query = f'''
                SELECT 
                    MIN("{col}") as min_val,
                    MAX("{col}") as max_val,
                    AVG("{col}") as avg_val,
                    COUNT("{col}") as non_null_count
                FROM {self.table_name}
                WHERE "{col}" IS NOT NULL AND id_projet = ?
                '''
                stat_df = self._execute_query(query, [project_id])
                if not stat_df.empty:
                    stats[col] = stat_df.iloc[0].to_dict()
            except Exception as e:
                self.logger.warning(f"Impossible de calculer les stats pour {col}: {e}")
        
        return stats
    
    def get_projects_list(self) -> pd.DataFrame:
        """
        Récupère la liste de tous les projets disponibles avec leurs statistiques de base.
        
        Returns:
            pd.DataFrame: DataFrame contenant les informations sur chaque projet
        """
        query = f'''
        SELECT 
            id_projet,
            COUNT(*) as nb_records,
            MIN(revenu) as min_revenu,
            MAX(revenu) as max_revenu,
            AVG(revenu) as avg_revenu
        FROM {self.table_name}
        GROUP BY id_projet
        ORDER BY id_projet
        '''
        return self._execute_query(query)
    
    def _execute_query(self, query: str, params: Optional[List] = None) -> pd.DataFrame:
        """
        Exécute une requête SQL et retourne un DataFrame.
        
        Args:
            query (str): Requête SQL à exécuter
            params (Optional[List]): Paramètres pour la requête
        
        Returns:
            pd.DataFrame: Résultat de la requête
        """
        try:
            with self._get_connection() as conn:
                df = pd.read_sql_query(query, conn, params=params)
                self.logger.info(f"Requête exécutée avec succès. {len(df)} lignes récupérées.")
                return df
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            self.logger.error(f"Requête: {query}")
            raise
    
    def export_to_csv(self, filename: str, conditions: Optional[Dict[str, Any]] = None, id_projet: Optional[int] = None):
        """
        Exporte les données vers un fichier CSV pour un projet donné.
        
        Args:
            filename (str): Nom du fichier CSV
            conditions (Optional[Dict[str, Any]]): Conditions pour filtrer les données
            id_projet (Optional[int]): ID du projet. Si None, utilise la valeur par défaut
        """
        try:
            if conditions:
                df = self.get_data_by_conditions(conditions, id_projet)
            else:
                df = self.get_all_data(id_projet)
            
            df.to_csv(filename, index=False, encoding='utf-8')
            project_id = id_projet if id_projet is not None else self.default_id_projet
            self.logger.info(f"Données du projet {project_id} exportées vers {filename}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export CSV: {e}")
            raise

# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO)
    
    # Créer une instance du service avec id_projet par défaut = 1
    data_service = RootDataService("database.db", default_id_projet=1)
    
    try:
        # Afficher la liste des projets disponibles
        projects_df = data_service.get_projects_list()
        print("Projets disponibles:")
        print(projects_df)
        
        # Récupérer toutes les données du projet par défaut (1)
        df_all = data_service.get_all_data()
        print(f"\nTotal des données récupérées pour le projet par défaut: {len(df_all)} lignes")
        print(f"Colonnes: {list(df_all.columns)}")
        
        # Afficher les premières lignes
        print("\nPremières lignes:")
        print(df_all.head())
        
        # Récupérer des statistiques pour le projet par défaut
        stats = data_service.get_statistics()
        print(f"\nStatistiques de base pour le projet {stats.get('id_projet', 'N/A')}:")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Exemple de filtrage pour le projet par défaut
        filtered_df = data_service.get_data_by_conditions({
            "maison (1 = oui)": 1,
            "jardin (1 = oui)": 1
        })
        print(f"\nDonnées filtrées (maison + jardin) pour le projet par défaut: {len(filtered_df)} lignes")
        
        # Exemple avec un projet spécifique (si il existe)
        if len(projects_df) > 1:
            second_project_id = projects_df.iloc[1]['id_projet']
            df_project_2 = data_service.get_all_data(id_projet=second_project_id)
            print(f"\nDonnées pour le projet {second_project_id}: {len(df_project_2)} lignes")
        
    except Exception as e:
        print(f"Erreur: {e}")