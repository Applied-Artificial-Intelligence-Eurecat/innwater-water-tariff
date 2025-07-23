import sqlite3
from typing import Dict, List, Union

class AFS_AffordabilityIndicatorBW:
    """Classe sans PRIMARY KEY et sans colonne created_at"""

    def __init__(self, project_id: int, db_path: str):
        self.project_id = project_id
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create_sqlite_table(self):
        """Crée la table si elle n'existe pas (sans PRIMARY KEY ni created_at)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS affordability_stats (
                    id_projet INTEGER,
                    metric TEXT,
                    par_ibt REAL,
                    par_tbse REAL,
                    delta_par REAL
                )
            """)
            self.conn.commit()
            print(f"✅ Table affordability_stats vérifiée/créée.")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite lors de la création de table: {str(e)}")

    def insert_data(self):
        """Insère des données factices dans la table"""
        try:
            cursor = self.conn.cursor()
            data = [
                (self.project_id, 'Moyenne', 1.1, 3.2, -2.1),
                (self.project_id, 'Médiane', 0.7, 2.0, -1.3)
            ]
            cursor.executemany(
                "INSERT INTO affordability_stats (id_projet, metric, par_ibt, par_tbse, delta_par) VALUES (?, ?, ?, ?, ?)",
                data
            )
            self.conn.commit()
            print(f"✅ Données insérées dans affordability_stats.")
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite lors de l'insertion: {str(e)}")

    def get_project_stats(self) -> Dict[str, Union[List[Dict], Dict]]:
        """Récupère uniquement Moyenne et Médiane pour PAR IBT, PAR TBSE et Delta PAR"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT metric, par_ibt, par_tbse, delta_par 
                FROM affordability_stats 
                WHERE id_projet = ? AND metric IN ('Moyenne', 'Médiane')
            """, (self.project_id,))
            rows = cursor.fetchall()

            stats = [{
                "metric": row["metric"],
                "PAR IBT": row["par_ibt"],
                "PAR TBSE": row["par_tbse"],
                "Delta PAR": row["delta_par"]
            } for row in rows]

            metadata = {
                "project_id": self.project_id,
                "stats_count": len(stats),
                "requested_metrics": ["Moyenne", "Médiane"]
            }

            print(f"✔ Données récupérées avec succès (trouvé {len(stats)} indicateurs)")
            return {"stats": stats, "metadata": metadata}

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite: {str(e)}")
            return {"stats": [], "metadata": {}}
        except Exception as e:
            print(f"❌ Erreur inattendue: {str(e)}")
            return {"stats": [], "metadata": {}}

    def run(self):
        """Pipeline complet pour compatibilité avec AfsParManager"""
        print(f"▶️ Exécution AFS_AffordabilityIndicatorBW pour project_id {self.project_id}")
        with self:
            self.create_sqlite_table()
            self.insert_data()
            result = self.get_project_stats()
            print(f"📊 Résultat final : {result}")
        print("✅ run() terminé.")

    @staticmethod
    def project_exists(project_id, db_path):
        """Vérifie si le projet existe dans la base de données"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM affordability_stats WHERE id_projet = ?", (project_id,))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except sqlite3.Error:
            return False

# ==============================
# Main de test
# ==============================
if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE = os.path.join(BASE_DIR, 'database.db')
    project_id = 1

    ai_bw = AFS_AffordabilityIndicatorBW(project_id, DATABASE)
    ai_bw.run()

    print("\n=== Fin du test ===")