import pandas as pd
import sqlite3
from typing import Dict, List, Optional, Union

class AFSAffIndicDWCar:
    def __init__(self):
        """Initialise les données CAR avec un projet par défaut"""
        self._projects: Dict[int, Dict[str, List]] = {
            1: {
                'metric': ['Min', 'Max', 'Q1', 'Q3', 'D1', 'D9', 'F (Moyenne)', 'Variance',
                          'Ecart-type', 'MAPE', 'Coeff de Variation', 'Etendue Interquantiles',
                          'Etendue Interdéciles', 'Coefficients de Yule'],
                'car_ibt': [0.3, 12.6, 1.0, 3.3, 0.6, 5.4, 63.0, 4.24, 2.06, 1.5, 0.822, 2.3, 4.8, 0.23],
                'car_tbse': [0.3, 23.6, 1.4, 5.0, 0.8, 9.6, 68.1, 15.73, 3.97, 2.9, 0.972, 3.6, 8.8, 0.18]
            }
        }
        self._default_db_path = "database.db"
        self._current_project_id = 1

    # ==================== GESTION DES PROJETS ====================
    def add_project(self, project_id: int, metrics: List[str], 
                   car_ibt: List[float], car_tbse: List[float]) -> bool:
        """Ajoute un nouveau projet avec ses données CAR"""
        if project_id in self._projects:
            return False
        
        self._projects[project_id] = {
            'metric': metrics,
            'car_ibt': car_ibt,
            'car_tbse': car_tbse
        }
        return True

    def remove_project(self, project_id: int) -> bool:
        """Supprime un projet existant"""
        if project_id not in self._projects or project_id == 1:
            return False
        del self._projects[project_id]
        return True

    # ==================== ACCÈS AUX DONNÉES ====================
    def get_project_data(self, project_id: int) -> Optional[Dict[str, List]]:
        """Récupère toutes les données d'un projet spécifique"""
        return self._projects.get(project_id)

    def get_metric_values(self, project_id: int, metric_name: str) -> Optional[Dict[str, float]]:
        """Récupère les valeurs CAR pour une métrique spécifique"""
        project_data = self.get_project_data(project_id)
        if not project_data:
            return None

        try:
            index = project_data['metric'].index(metric_name)
            return {
                'car_ibt': project_data['car_ibt'][index],
                'car_tbse': project_data['car_tbse'][index]
            }
        except ValueError:
            return None

    # ==================== PERSISTANCE DES DONNÉES ====================
    def save_to_sqlite(self, project_id: int, db_path: str = None) -> bool:
        """Sauvegarde les données dans une base SQLite"""
        db_path = db_path or self._default_db_path
        project_data = self.get_project_data(project_id)
        
        if not project_data:
            return False

        try:
            df = pd.DataFrame(project_data)
            with sqlite3.connect(db_path) as conn:
                df.to_sql(f'project_{project_id}', conn, if_exists='replace', index=False)
            return True
        except Exception as e:
            print(f"Erreur sauvegarde SQLite: {e}")
            return False

    def load_from_sqlite(self, project_id: int, db_path: str = None) -> bool:
        """Charge les données depuis SQLite"""
        db_path = db_path or self._default_db_path
        
        try:
            with sqlite3.connect(db_path) as conn:
                df = pd.read_sql(f'SELECT * FROM project_{project_id}', conn)
                self._projects[project_id] = df.to_dict('list')
            return True
        except Exception as e:
            print(f"Erreur chargement SQLite: {e}")
            return False

    # ==================== UTILITAIRES ====================
    def to_dataframe(self, project_id: int) -> Optional[pd.DataFrame]:
        """Convertit les données en DataFrame pandas"""
        project_data = self.get_project_data(project_id)
        if not project_data:
            return None
        return pd.DataFrame(project_data)

    def get_stats_summary(self, project_id: int) -> Optional[Dict[str, Dict[str, float]]]:
        """Calcule des statistiques sommaires"""
        df = self.to_dataframe(project_id)
        if df is None:
            return None

        return {
            'car_ibt': {
                'mean': df['car_ibt'].mean(),
                'std': df['car_ibt'].std(),
                'min': df['car_ibt'].min(),
                'max': df['car_ibt'].max()
            },
            'car_tbse': {
                'mean': df['car_tbse'].mean(),
                'std': df['car_tbse'].std(),
                'min': df['car_tbse'].min(),
                'max': df['car_tbse'].max()
            }
        }

    # ==================== PROPRIÉTÉS ====================
    @property
    def available_projects(self) -> List[int]:
        """Liste des IDs de projets disponibles"""
        return list(self._projects.keys())

    @property
    def current_project_id(self) -> int:
        return self._current_project_id

    @current_project_id.setter
    def current_project_id(self, value: int):
        if value in self._projects:
            self._current_project_id = value