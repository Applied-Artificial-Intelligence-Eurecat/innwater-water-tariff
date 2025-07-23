# afscarManager.py

import sqlite3
import pandas as pd

from AFSAffIndicBWCar import AFSAffIndicBWCar
from AFSAffIndicDWCar import AFSAffIndicDWCar
from aFS_IncidCalcCar import AFS_IncidCalcCar
from aFSIntensCalcCar import aFSIntensCalcCar
from aFSIntensCalcCarDa import aFSIntensCalcCarDa
from AFSInequalCalcCar import AFSInequalCalcCar
from aFSPopHhDiffCar import aFSPopHhDiffCar

class AfscarManager:
    def __init__(self, id_projet=1, db_path='database.db'):
        self.id_projet = id_projet
        self.db_path = db_path

        # Instanciation des 7 modules dans l'ordre spécifié
        self.aff_bw = AFSAffIndicBWCar(project_id=self.id_projet)
        self.aff_dw = AFSAffIndicDWCar()  # pas de paramètre project_id selon ta déclaration
        self.incid_calc = AFS_IncidCalcCar(project_id=self.id_projet, database_name=self.db_path)
        self.intens_calc = aFSIntensCalcCar(db_path=self.db_path)
        self.intens_calc_da = aFSIntensCalcCarDa(id_projet=self.id_projet, db_path=self.db_path)
        self.inequal_calc = AFSInequalCalcCar()
        self.pop_diff_car = aFSPopHhDiffCar(id_projet=self.id_projet)

    def create_all_tables(self):
        """Crée toutes les tables des modules dans la base SQLite."""
        print("🔧 Création de toutes les tables...")

        # Vérifie si tes classes aff_bw et aff_dw ont bien ces méthodes avant d’appeler
        # self.aff_bw.create_table()
        # self.aff_dw.create_table()

        self.incid_calc.save_to_db()
        self.intens_calc.create_table_in_db()
        self.intens_calc_da.create_table()
        self.inequal_calc.creer_table_sqlite()
        self.pop_diff_car.construire_dataframe()
        self.pop_diff_car.creer_table_sqlite()

        print("✅ Toutes les tables ont été créées avec succès.")

    def insert_all(self):
        """Insère les données dans toutes les tables (si applicable)."""
        print("📥 Insertion de toutes les données...")

        # Vérifie si tes classes aff_bw et aff_dw ont bien ces méthodes avant d’appeler
        # self.aff_bw.insert_data()
        # self.aff_dw.insert_data()

        # AFS_IncidCalcCar utilise save_to_db déjà appelé dans create_all_tables

        self.intens_calc.insert_data(id_projet=self.id_projet)
        self.intens_calc_da.insert_data()
        
        df_ineq = self.inequal_calc.creer_dataframe(self.id_projet)
        self.inequal_calc.inserer_dataframe(df_ineq)

        self.pop_diff_car.inserer_donnees_sqlite()

        print("✅ Toutes les données ont été insérées avec succès.")

    def load_all(self):
        """Charge les données de toutes les tables et les retourne sous forme de dictionnaires de DataFrames."""
        print("📂 Chargement de toutes les données...")

        results = {}

        # Vérifie si tes classes aff_bw et aff_dw ont bien ces méthodes avant d’appeler
        # results['aff_bw'] = self.aff_bw.load_data()
        # results['aff_dw'] = self.aff_dw.load_data()

        results['incid_calc'] = self.incid_calc.load_from_db()

        conn = sqlite3.connect(self.db_path)
        results['intens_calc'] = pd.read_sql_query("SELECT * FROM aFSIntensCalcCar", conn)
        results['intens_calc_da'] = pd.read_sql_query("SELECT * FROM aFSIntensCalcCarDa", conn)
        results['inequal_calc'] = self.inequal_calc.get_data(self.id_projet)
        results['pop_diff_car'] = pd.read_sql_query("SELECT * FROM pop_hh_diff_car", conn)
        conn.close()

        print("✅ Toutes les données ont été chargées avec succès.")
        return results


if __name__ == "__main__":
    manager = AfscarManager(id_projet=1, db_path='database.db')
    
    manager.create_all_tables()
    manager.insert_all()
    dataframes = manager.load_all()
    
    for key, df in dataframes.items():
        print(f"\n🔷 Données pour '{key}' :")
        print(df)
