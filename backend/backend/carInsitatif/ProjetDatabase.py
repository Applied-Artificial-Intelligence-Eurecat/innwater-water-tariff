import sqlite3
from typing import Dict, Any, Optional, List

class CarincitatifGenSrv:
    def __init__(self, db_path: str = "database.db", column_name: str = "water_consumption_ibt"):
        """
        Initialise la classe avec le chemin de la base de données et le nom de la colonne
        
        Args:
            db_path (str): Chemin vers le fichier de base de données SQLite
            column_name (str): Nom de la colonne à analyser (défaut: "water_consumption_ibt")
        """
        self.db_path = db_path
        self.column_name = column_name
        self.connection = None
        
    def connect(self) -> None:
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        except sqlite3.Error as e:
            raise ConnectionError(f"Erreur de connexion à la base de données: {e}")
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def set_column_name(self, column_name: str) -> None:
        """
        Change le nom de la colonne à analyser
        
        Args:
            column_name (str): Nouveau nom de la colonne
        """
        self.column_name = column_name
    
    def _execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        """
        Méthode interne pour exécuter une requête SQL
        
        Args:
            query (str): Requête SQL à exécuter
            params (tuple): Paramètres pour la requête préparée
            
        Returns:
            Liste de dictionnaires contenant les résultats ou None si erreur
        """
        try:
            if not self.connection:
                self.connect()
                
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            
            if results:
                return [dict(row) for row in results]  # Convertit les lignes en dictionnaires
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None
    
    def get_statistics(self, id_projet: int = 1) -> Optional[Dict[str, Any]]:
        """
        Exécute la requête principale pour récupérer les statistiques de consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Dict contenant les résultats ou None si erreur
        """
        query = f"""
        WITH ordered_data AS (
            SELECT 
                {self.column_name},
                ROW_NUMBER() OVER (ORDER BY {self.column_name}) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ),
        median_calc AS (
            SELECT 
                AVG({self.column_name}) AS median_value
            FROM ordered_data
            WHERE row_num IN (
                (total_count + 1) / 2,
                (total_count + 2) / 2
            )
        )
        SELECT 
            ROUND(AVG(c.{self.column_name}), 2) AS moyenne,
            ROUND(MIN(c.{self.column_name}), 2) AS minimum,
            ROUND(MAX(c.{self.column_name}), 2) AS maximum,
            COUNT(*) AS nombre_menages,
            ROUND(m.median_value, 2) AS mediane
        FROM carInsitatifdataintermed c
        CROSS JOIN median_calc m
        WHERE c.id_projet = ?;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0] if results else None
    
    def get_mean_absolute_error(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule l'écart moyen absolu (MAE) entre les valeurs et la moyenne
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Écart moyen absolu ou None si erreur
        """
        query = f"""
        SELECT 
            ROUND(AVG(ABS({self.column_name} - moyenne)), 3) AS ecart_moyen
        FROM carInsitatifdataintermed
        CROSS JOIN (
            SELECT AVG({self.column_name}) AS moyenne 
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ) AS avg_calc
        WHERE id_projet = ?;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0]['ecart_moyen'] if results else None
    
    def get_mean_absolute_percentage_error(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule l'erreur absolue moyenne en pourcentage (MAPE)
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            MAPE en pourcentage ou None si erreur
        """
        query = f"""
        SELECT 
            ROUND(AVG(ABS(({self.column_name} - moyenne) / NULLIF({self.column_name}, 0)) * 100), 3) AS mape
        FROM carInsitatifdataintermed
        CROSS JOIN (
            SELECT AVG({self.column_name}) AS moyenne 
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ) AS avg_calc
        WHERE {self.column_name} > 0 AND id_projet = ?;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0]['mape'] if results else None
    
    def get_variance(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule la variance de l'échantillon de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Variance de l'échantillon ou None si erreur
        """
        query = f"""
        SELECT 
            ROUND(SUM(POWER({self.column_name} - moyenne, 2)) / (COUNT(*) - 1), 3) AS variance_echantillon
        FROM carInsitatifdataintermed
        CROSS JOIN (
            SELECT AVG({self.column_name}) AS moyenne 
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ) AS avg_calc
        WHERE id_projet = ?;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0]['variance_echantillon'] if results else None
    
    def get_standard_deviation(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule l'écart-type de l'échantillon de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Écart-type de l'échantillon ou None si erreur
        """
        query = f"""
        SELECT 
            ROUND(SQRT(SUM(POWER({self.column_name} - moyenne, 2)) / (COUNT(*) - 1)), 3) AS ecart_type_echantillon
        FROM carInsitatifdataintermed
        CROSS JOIN (
            SELECT AVG({self.column_name}) AS moyenne 
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ) AS avg_calc
        WHERE id_projet = ?;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0]['ecart_type_echantillon'] if results else None
    
    def get_standard_deviation_from_variance(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule l'écart-type à partir de la variance (méthode alternative)
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Écart-type de l'échantillon ou None si erreur
        """
        variance = self.get_variance(id_projet)
        if variance is not None:
            return round(variance ** 0.5, 3)
        return None
    
    def get_percentile_10(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule le 10ème percentile de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Valeur du percentile 10 ou None si erreur
        """
        query = f"""
        WITH ranked_data AS (
            SELECT 
                {self.column_name},
                ROW_NUMBER() OVER (ORDER BY {self.column_name}) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        )
        SELECT 
            {self.column_name} AS percentile_10
        FROM ranked_data
        WHERE row_num = CEIL(0.1 * total_count);
        """
        
        results = self._execute_query(query, (id_projet,))
        return results[0]['percentile_10'] if results else None
    
    def get_percentile_25(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule le 25ème percentile de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Valeur du percentile 25 ou None si erreur
        """
        query = f"""
        WITH ranked_data AS (
            SELECT 
                {self.column_name},
                ROW_NUMBER() OVER (ORDER BY {self.column_name}) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        )
        SELECT 
            {self.column_name} AS percentile_25
        FROM ranked_data
        WHERE row_num = CEIL(0.25 * total_count);
        """
        
        results = self._execute_query(query, (id_projet,))
        return results[0]['percentile_25'] if results else None
    
    def get_percentile_75(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule le 75ème percentile de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Valeur du percentile 75 arrondie à 2 décimales ou None si erreur
        """
        query = f"""
        WITH ranked_data AS (
            SELECT 
                {self.column_name},
                ROW_NUMBER() OVER (ORDER BY {self.column_name}) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        )
        SELECT 
            ROUND({self.column_name}, 2) AS percentile_75
        FROM ranked_data
        WHERE row_num = CEIL(0.75 * total_count);
        """
        
        results = self._execute_query(query, (id_projet,))
        return results[0]['percentile_75'] if results else None
    
    def get_percentile_90(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule le 90ème percentile de la consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Valeur du percentile 90 ou None si erreur
        """
        query = f"""
        WITH ranked_data AS (
            SELECT 
                {self.column_name},
                ROW_NUMBER() OVER (ORDER BY {self.column_name}) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        )
        SELECT 
            {self.column_name} AS percentile_90
        FROM ranked_data
        WHERE row_num = CEIL(0.9 * total_count);
        """
        
        results = self._execute_query(query, (id_projet,))
        return results[0]['percentile_90'] if results else None
    
    def get_average_percentile_rank(self, id_projet: int = 1) -> Optional[float]:
        """
        Calcule le rang percentile de la moyenne de consommation d'eau
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Pourcentage de ménages consommant moins ou égal à la moyenne, ou None si erreur
        """
        query = f"""
        WITH stats AS (
            SELECT 
                AVG({self.column_name}) AS moyenne_consommation,
                COUNT(*) AS total_count
            FROM carInsitatifdataintermed
            WHERE id_projet = ?
        ),
        below_avg_count AS (
            SELECT 
                COUNT(*) AS count_below_avg
            FROM carInsitatifdataintermed
            WHERE {self.column_name} <= (SELECT moyenne_consommation FROM stats) 
            AND id_projet = ?
        )
        SELECT 
            ROUND(100.0 * count_below_avg / total_count, 2) AS rang_percentile_moyenne
        FROM stats, below_avg_count;
        """
        
        results = self._execute_query(query, (id_projet, id_projet))
        return results[0]['rang_percentile_moyenne'] if results else None
    
    def get_all_indicators(self, id_projet: int = 1) -> Optional[Dict[str, Any]]:
        """
        Récupère tous les indicateurs statistiques en une seule fois
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Dict contenant toutes les statistiques ou None si erreur
        """
        # Récupère les statistiques de base
        stats = self.get_statistics(id_projet)
        if not stats:
            return None
        
        # Ajoute l'écart moyen absolu (MAE)
        mae = self.get_mean_absolute_error(id_projet)
        if mae is not None:
            stats['ecart_moyen_absolu'] = mae
        
        # Ajoute le MAPE
        mape = self.get_mean_absolute_percentage_error(id_projet)
        if mape is not None:
            stats['mape'] = mape
        
        # Ajoute la variance
        variance = self.get_variance(id_projet)
        if variance is not None:
            stats['variance'] = variance
        
        # Ajoute l'écart-type (méthode directe SQL)
        std_dev = self.get_standard_deviation(id_projet)
        if std_dev is not None:
            stats['ecart_type'] = std_dev
        
        # Ajoute le percentile 10
        percentile_10 = self.get_percentile_10(id_projet)
        if percentile_10 is not None:
            stats['percentile_10'] = round(percentile_10, 2)
        
        # Ajoute le percentile 25
        percentile_25 = self.get_percentile_25(id_projet)
        if percentile_25 is not None:
            stats['percentile_25'] = round(percentile_25, 2)
        
        # Ajoute le percentile 75
        percentile_75 = self.get_percentile_75(id_projet)
        if percentile_75 is not None:
            stats['percentile_75'] = percentile_75  # Déjà arrondi dans la requête
        
        # Ajoute le percentile 90
        percentile_90 = self.get_percentile_90(id_projet)
        if percentile_90 is not None:
            stats['percentile_90'] = round(percentile_90, 2)
        
        # Ajoute le rang percentile de la moyenne
        avg_percentile = self.get_average_percentile_rank(id_projet)
        if avg_percentile is not None:
            stats['rang_percentile_moyenne'] = avg_percentile
        
        return stats
    
    def get_all_percentiles(self, id_projet: int = 1) -> Optional[Dict[str, float]]:
        """
        Récupère tous les percentiles en une seule fois
        
        Args:
            id_projet (int): ID du projet à filtrer (défaut: 1)
            
        Returns:
            Dict contenant tous les percentiles ou None si erreur
        """
        percentiles = {}
        
        percentile_10 = self.get_percentile_10(id_projet)
        if percentile_10 is not None:
            percentiles['percentile_10'] = round(percentile_10, 2)
        
        percentile_25 = self.get_percentile_25(id_projet)
        if percentile_25 is not None:
            percentiles['percentile_25'] = round(percentile_25, 2)
        
        percentile_75 = self.get_percentile_75(id_projet)
        if percentile_75 is not None:
            percentiles['percentile_75'] = percentile_75
        
        percentile_90 = self.get_percentile_90(id_projet)
        if percentile_90 is not None:
            percentiles['percentile_90'] = round(percentile_90, 2)
        
        return percentiles if percentiles else None

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple 1: Utilisation avec la colonne par défaut
    print("=== Utilisation avec la colonne par défaut (water_consumption_ibt) ===")
    service = CarincitatifGenSrv("database.db")
    id_projet = 1
    
    stats = service.get_statistics(id_projet)
    if stats:
        print(f"Statistiques pour la colonne '{service.column_name}':")
        for key, value in stats.items():
            print(f"{key}: {value}")
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 2: Utilisation avec une colonne différente spécifiée à l'initialisation
    print("=== Utilisation avec une colonne spécifiée à l'initialisation ===")
    service_pp = CarincitatifGenSrv("database.db", "water_consumption_ibt_pp")
    
    stats_pp = service_pp.get_statistics(id_projet)
    if stats_pp:
        print(f"Statistiques pour la colonne '{service_pp.column_name}':")
        for key, value in stats_pp.items():
            print(f"{key}: {value}")
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 3: Changement de colonne en cours d'utilisation
    print("=== Changement de colonne en cours d'utilisation ===")
    service.set_column_name("water_consumption_ibt_pp")
    print(f"Nouvelle colonne définie: {service.column_name}")
    
    stats_changed = service.get_statistics(id_projet)
    if stats_changed:
        print(f"Statistiques pour la nouvelle colonne '{service.column_name}':")
        for key, value in stats_changed.items():
            print(f"{key}: {value}")
    
    print("\n" + "="*60 + "\n")
    
    # Exemple 4: Récupération de tous les indicateurs avec une colonne spécifique
    print("=== Tous les indicateurs avec colonne spécifique ===")
    service_custom = CarincitatifGenSrv("database.db", "water_consumption_ibt")
    all_indicators = service_custom.get_all_indicators(id_projet)
    if all_indicators:
        print(f"Tous les indicateurs pour la colonne '{service_custom.column_name}':")
        for key, value in all_indicators.items():
            print(f"{key}: {value}")
    
    # Fermeture des connexions
    service.disconnect()
    service_pp.disconnect()
    service_custom.disconnect()