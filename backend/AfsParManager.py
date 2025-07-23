import sqlite3

# Imports des classes, ajuster les chemins selon ton projet
from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW
from AFS_AffordabilityIndicatorDW import AFS_AffordabilityIndicatorDW
from AFS_IncidenceCalc import AFS_IncidenceCalc
from afs_Intensity import AFSIntensityCalc
from AFS_InequalityCalc import AFS_InequalityCalc
from aFSPopHhInDiff import AFSPopHHDiff


class AfsParManager:
    def __init__(self, project_id: int = 1, database_name: str = "database.db"):
        self.project_id = project_id
        self.database_name = database_name

        # Instanciation des modules avec project_id et db_path si nécessaire
        self.affordability_indicator_bw = AFS_AffordabilityIndicatorBW(project_id, database_name)
        self.affordability_indicator_dw = AFS_AffordabilityIndicatorDW(project_id)
        self.incidence_calc = AFS_IncidenceCalc(project_id)
        self.intensity_calc = AFSIntensityCalc(project_id)
        self.inequality_calc = AFS_InequalityCalc(project_id)
        self.pop_hh_diff = AFSPopHHDiff(project_id)

    def run_all(self):
        print(f"🔧 Initialisation du projet ID: {self.project_id}\n")

        # 0. Affordability Indicator BW (nouveau)
        print("▶️ AFS_AffordabilityIndicatorBW")
        self.affordability_indicator_bw.run()
        print("✅ AFS_AffordabilityIndicatorBW terminé.\n")

        # 1. Affordability Indicator DW
        print("▶️ AFS_AffordabilityIndicatorDW")
        df1 = self.affordability_indicator_dw.build_dataframe()
        print(df1)
        self.affordability_indicator_dw.create_sqlite_table()
        self.affordability_indicator_dw.insert_data()
        print("✅ AFS_AffordabilityIndicatorDW terminé.\n")

        # 2. Incidence Calc
        print("▶️ AFS_IncidenceCalc")
        df2 = self.incidence_calc.build_dataframe()
        print(df2)
        self.incidence_calc.create_sqlite_table()
        self.incidence_calc.insert_data()
        print("✅ AFS_IncidenceCalc terminé.\n")

        # 3. Intensity Calc
        print("▶️ AFSIntensityCalc")
        df3 = self.intensity_calc.build_dataframe()
        print(df3)
        self.intensity_calc.create_sqlite_table()
        self.intensity_calc.insert_data()
        print("✅ AFSIntensityCalc terminé.\n")

        # 4. Inequality Calc
        print("▶️ AFS_InequalityCalc")
        df4 = self.inequality_calc.build_dataframe()
        print(df4)
        self.inequality_calc.create_sqlite_table()
        self.inequality_calc.insert_data()
        print("✅ AFS_InequalityCalc terminé.\n")

        # 5. Pop HH in Difficulty
        print("▶️ AFSPopHHDiff")
        df5 = self.pop_hh_diff.build_dataframe()
        print(df5)
        self.pop_hh_diff.create_sqlite_table()
        self.pop_hh_diff.insert_data()
        print("✅ AFSPopHHDiff terminé.\n")

        print("🎯 Tous les modules ont été exécutés avec succès.")
        print(f"📂 Base SQLite : {self.database_name}")



if __name__ == "__main__":
    manager = AfsParManager(project_id=1, database_name="database.db")
    manager.run_all()
