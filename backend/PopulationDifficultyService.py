import pandas as pd
import sqlite3
class PopulationDifficultyService:
    
   # Nouvelle version modifiée
    @staticmethod
    def get_data(project_id):
        conn = sqlite3.connect('database.db')
        query = """
        SELECT 
            indicateur AS "indicateur",
            ibt AS "IBT",
            tbse AS "TBSE",
            id_projet AS "ID_Projet"
        FROM 
            AFS_pop_hh_in_difficulty 
        WHERE 
            id_projet = ?
        """
        df = pd.read_sql(query, conn, params=(project_id,))
        conn.close()
        return df