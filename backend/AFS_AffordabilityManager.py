from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW
from AFS_AffordabilityIndicatorDW import AFS_AffordabilityIndicatorDW
from AFS_IncidenceCalc import AFS_IncidenceCalc
from afs_Intensity import AFSIntensityCalc
from AFS_InequalityCalc import AFS_InequalityCalc
from AFS_pop_hh_in_difficulty import AFS_pop_hh_in_difficulty

class AFS_AffordabilityManager:
    def __init__(self, project_id):
        self.project_id = project_id
        self.indicators = {
            'affordability_bw': None,
            'affordability_dw': None,
            'incidence': None,
            'intensity': None,
            'inequality': None,
            'pop_hh_difficulty': None
        }
    
    def initialize_components(self):
        """Initialise toutes les composantes avec le project_id"""
        self.indicators['affordability_bw'] = AFS_AffordabilityIndicatorBW(self.project_id)
        self.indicators['affordability_dw'] = AFS_AffordabilityIndicatorDW(self.project_id)
        self.indicators['incidence'] = AFS_IncidenceCalc(self.project_id)
        self.indicators['intensity'] = AFSIntensityCalc(self.project_id)
        self.indicators['inequality'] = AFS_InequalityCalc(self.project_id)
        self.indicators['pop_hh_difficulty'] = AFS_pop_hh_in_difficulty(self.project_id)
    
    def build_all_dataframes(self):
        """Construit tous les DataFrames"""
        results = {}
        for name, indicator in self.indicators.items():
            if hasattr(indicator, 'build_dataframe'):
                results[name] = indicator.build_dataframe()
                print(f"DataFrame généré pour {name}:")
                print(results[name])
                print("\n")
        return results
    
    def create_all_tables(self):
        """Crée toutes les tables SQLite"""
        for indicator in self.indicators.values():
            if hasattr(indicator, 'create_sqlite_table'):
                indicator.create_sqlite_table()
            elif hasattr(indicator, 'create_database_table'):
                indicator.create_database_table()
    
    def insert_all_data(self):
        """Insère toutes les données dans les tables SQLite"""
        for indicator in self.indicators.values():
            if hasattr(indicator, 'insert_data'):
                indicator.insert_data()
    
    def run_all(self):
        """Exécute toutes les opérations dans l'ordre"""
        self.initialize_components()
        self.build_all_dataframes()
        self.create_all_tables()
        self.insert_all_data()
        print("Toutes les opérations ont été exécutées avec succès.")


# Exemple d'utilisation
if __name__ == "__main__":
    # Création du manager avec un ID de projet
    manager = AFS_AffordabilityManager(project_id=1)
    
    # Exécution complète
    manager.run_all()
    
    # Vous pouvez aussi exécuter les composantes séparément si besoin
    # manager.initialize_components()
    # manager.build_all_dataframes()
    # etc.