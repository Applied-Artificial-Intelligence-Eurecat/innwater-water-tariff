import sqlite3
import pandas as pd

class ComonTavaRedevanceInsertSrv:
    def __init__(self, db_path='database.db'):
        """
        Initialise le service avec le chemin de la base de données.
        """
        self.db_path = db_path
  
    
    
    
    def insert_from_dataframe(self, df: pd.DataFrame):
        """
        Insère les données d'un DataFrame dans la table comoTva_redevance.
        """
        required_columns = [
            'id_projet',
            'type_taxe',
            'taux_tva_pourcent',
            'redevances_accise_euro_m3'
        ]
       
        # Vérifie que toutes les colonnes sont présentes
        if not all(col in df.columns for col in required_columns):
            missing = list(set(required_columns) - set(df.columns))
            raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing}")
       
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO comoTva_redevance (
                        id_projet, type_taxe, taux_tva_pourcent, redevances_accise_euro_m3
                    ) VALUES (?, ?, ?, ?)
                """, (
                    int(row['id_projet']),
                    str(row['type_taxe']),
                    float(row['taux_tva_pourcent']),
                    float(row['redevances_accise_euro_m3'])
                ))
            conn.commit()
    
    def clear_project_data(self, id_projet):
        """
        Supprime toutes les données d'un projet spécifique.
        Utile pour réinsérer des données mises à jour.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM comoTva_redevance WHERE id_projet = ?", (id_projet,))
            conn.commit()
    
    def fetch_all(self):
        """
        Récupère tous les enregistrements de la table.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comoTva_redevance")
            return cursor.fetchall()
    
    def fetch_by_project(self, id_projet):
        """
        Récupère tous les enregistrements d'un projet spécifique.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comoTva_redevance WHERE id_projet = ?", (id_projet,))
            return cursor.fetchall()

# Exemple d'utilisation
if __name__ == "__main__":

    
    # Maintenant utiliser le service d'insertion
    data = {
        'id_projet': [1, 1, 1],
        'type_taxe': ['EPA', 'A', 'EP'],
        'taux_tva_pourcent': [0, 10, 2.1],
        'redevances_accise_euro_m3': [0.16, 0.04, 0.12]
    }
    df = pd.DataFrame(data)
    
    inserter = ComonTavaRedevanceInsertSrv()
    
    # Optionnel : nettoyer les données existantes du projet 1
    # inserter.clear_project_data(1)
    
    inserter.insert_from_dataframe(df)
    print("Insertion terminée avec succès !")
    
    # Vérification
    all_records = inserter.fetch_all()
    print(f"\nNombre total d'enregistrements : {len(all_records)}")
    for record in all_records:
        print(record)
    
    project_1_records = inserter.fetch_by_project(1)
    print(f"\nEnregistrements pour le projet 1 : {len(project_1_records)}")
    for record in project_1_records:
        print(record)