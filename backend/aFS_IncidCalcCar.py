import pandas as pd
import sqlite3
from typing import Dict, Any, List

class AFS_IncidCalcCar:
    def __init__(self, project_id: int = 1, database_name: str = "database.db"):
        self.project_id = project_id
        self.database_name = database_name
        self.table_name = "afs_incid_calc_car"

    def build_dataframe(self) -> pd.DataFrame:
        """Génère le DataFrame avec la structure et les valeurs demandées."""
        data = {
            "Headcount ratio": [28.8, 32.6, 38.0],
            "CAR IBT": [48.3, 48.9, 52.3],
            "CAR TBSE": [28.8, 32.6, 38.0],
            "Delta CAR": [-19.4, -16.3, -14.3]
        }

        index = ["Ménages", "Individus", "Enfants"]

        df = pd.DataFrame(data, index=index)
        df.index.name = "Category"
        df.reset_index(inplace=True)

        # Ajout de la colonne ID_Projet
        df["id_projet"] = self.project_id

        # Réorganiser les colonnes
        df = df[["id_projet", "Category", "Headcount ratio", "CAR IBT", "CAR TBSE", "Delta CAR"]]

        return df

    def save_to_db(self) -> None:
        """Sauvegarde le DataFrame généré dans la base SQLite."""
        df = self.build_dataframe()
        with sqlite3.connect(self.database_name) as conn:
            df.to_sql(self.table_name, conn, if_exists='replace', index=False)

    def load_from_db(self) -> pd.DataFrame:
        """Charge les données de la table SQLite."""
        with sqlite3.connect(self.database_name) as conn:
            query = f"SELECT * FROM {self.table_name} WHERE id_projet = ?"
            df = pd.read_sql_query(query, conn, params=(self.project_id,))
        return df

    def to_dict(self) -> List[Dict[str, Any]]:
        """Retourne le DataFrame généré sous forme de liste de dictionnaires."""
        df = self.build_dataframe()
        return df.to_dict(orient='records')


if __name__ == "__main__":
    # Exemple d'utilisation directe
    calc = AFS_IncidCalcCar(project_id=1)
    
    print("🔷 DataFrame généré :")
    df = calc.build_dataframe()
    print(df)
    
    print("\n💾 Sauvegarde en base...")
    calc.save_to_db()
    print("✅ Sauvegarde terminée.")
    
    print("\n📂 Chargement depuis la base :")
    df_loaded = calc.load_from_db()
    print(df_loaded)
    
    print("\n🔍 Conversion en liste de dictionnaires :")
    data_dict = calc.to_dict()
    print(data_dict)
