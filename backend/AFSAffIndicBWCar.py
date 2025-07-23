import sqlite3
from datetime import datetime
from typing import Dict, List, Union
import os

class AFSAffIndicBWCar:
    """Classe pour gérer les indicateurs CAR (Capital Adequacy Ratio) avec database.db"""
    
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.db_path = "database.db"
        self.conn = None
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    @classmethod
    def initialize_database(cls):
        """Initialise la base de données avec les tables nécessaires"""
        try:
            with sqlite3.connect("database.db") as conn:
                # Création de la table car_indicators
                conn.execute("""
                CREATE TABLE IF NOT EXISTS car_indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    metric TEXT NOT NULL,
                    car_ibt REAL NOT NULL,
                    car_tbse REAL NOT NULL,
                    delta_car REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                # Table projets
                conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )
                """)
                
                print("✔ Base de données initialisée avec succès")
        except sqlite3.Error as e:
            print(f"❌ Erreur d'initialisation: {str(e)}")

    @classmethod
    def project_exists(cls, project_id: int) -> bool:
        """Vérifie si le projet existe dans la base"""
        try:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM projects WHERE id = ? LIMIT 1", (project_id,))
                return cursor.fetchone() is not None
        except sqlite3.Error:
            return False
    
    def get_indicators(self) -> Dict[str, Union[List[Dict], Dict]]:
        """
        Récupère les indicateurs CAR formatés
        Retourne: {'indicators': [données], 'metadata': {infos}}
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute(
                """SELECT metric, car_ibt, car_tbse, delta_car 
                FROM car_indicators 
                WHERE project_id = ? AND metric IN ('Moyenne', 'Médiane')
                ORDER BY metric""",
                (self.project_id,)
            )
            rows = cursor.fetchall()
            
            indicators = [dict(row) for row in rows]
            
            metadata = {
                "project_id": self.project_id,
                "retrieved_at": datetime.now().isoformat(),
                "metrics_count": len(indicators)
            }
            
            return {
                "indicators": indicators,
                "metadata": metadata
            }
            
        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite: {str(e)}")
            return {"indicators": [], "metadata": {}}

    def save_indicators(self, indicators_data: Dict[str, Dict]):
        """
        Sauvegarde les indicateurs CAR
        Format attendu: {
            'Moyenne': {'car_ibt': 2.5, 'car_tbse': 4.1, 'delta_car': -1.57},
            'Médiane': {'car_ibt': 1.9, 'car_tbse': 2.9, 'delta_car': -0.99}
        }
        """
        try:
            cursor = self.conn.cursor()
            
            # Suppression des anciennes entrées
            cursor.execute("DELETE FROM car_indicators WHERE project_id = ?", (self.project_id,))
            
            # Insertion des nouvelles données
            for metric, values in indicators_data.items():
                cursor.execute(
                    """INSERT INTO car_indicators 
                    (project_id, metric, car_ibt, car_tbse, delta_car)
                    VALUES (?, ?, ?, ?, ?)""",
                    (self.project_id, metric, 
                     values['car_ibt'], 
                     values['car_tbse'], 
                     values['delta_car'])
                )
            
            self.conn.commit()
            print(f"✔ Indicateurs CAR sauvegardés (projet {self.project_id})")
            
        except sqlite3.Error as e:
            print(f"❌ Erreur de sauvegarde: {str(e)}")
            self.conn.rollback()

def main():
    """Exemple d'utilisation complet"""
    print("\n=== GESTION DES INDICATEURS CAR (AFS) ===")
    
    # Initialisation
    AFSAffIndicBWCar.initialize_database()
    
    # Configuration
    PROJECT_ID = 1
    SAMPLE_DATA = {
        'Moyenne': {
            'car_ibt': 2.5,
            'car_tbse': 4.1,
            'delta_car': -1.57
        },
        'Médiane': {
            'car_ibt': 1.9,
            'car_tbse': 2.9,
            'delta_car': -0.99
        }
    }
    
    # Création d'un projet test
    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT OR IGNORE INTO projects (id, name) VALUES (?, ?)", 
                        (PROJECT_ID, "Projet Test AFS CAR"))
            conn.commit()
    except sqlite3.Error as e:
        print(f"⚠ Attention: {str(e)}")
    
    # Utilisation de la classe
    with AFSAffIndicBWCar(PROJECT_ID) as car_indic:
        # Sauvegarde des données
        car_indic.save_indicators(SAMPLE_DATA)
        
        # Récupération des données
        result = car_indic.get_indicators()
        
        # Affichage des résultats
        print("\nRÉSULTATS OBTENUS:")
        print(f"- Projet ID: {result['metadata']['project_id']}")
        print(f"- Metrics trouvées: {result['metadata']['metrics_count']}")
        
        print("\nDÉTAIL DES INDICATEURS:")
        for indicator in result['indicators']:
            print(f"\n{indicator['metric']}:")
            print(f"  CAR IBT: {indicator['car_ibt']}")
            print(f"  CAR TBSE: {indicator['car_tbse']}")
            print(f"  Delta CAR: {indicator['delta_car']}")
    
    print("\n=== OPERATION TERMINEE ===")

if __name__ == "__main__":
    main()