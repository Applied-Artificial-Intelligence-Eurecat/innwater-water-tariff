import pandas as pd
import sqlite3
from typing import Optional

class AFSPopHHDiff:
    def __init__(self, id_projet: int = 1):
        self.id_projet = id_projet
        self.df: Optional[pd.DataFrame] = None

    def build_dataframe(self) -> pd.DataFrame:
        """Génère le DataFrame avec la structure demandée"""
        data = {
            'IBT': [44.1, 31.8, 17.8, 38.8, 19.1],
            'TBSE': [36.8, 28.3, 9.3, 23.1, 10.1]
        }
        
        index = [
            'Gini',
            'Schutz',
            'Ratio interdéciles',
            'Ratio interdécimes',
            'Ratio S80 / S20'
        ]
        
        self.df = pd.DataFrame(data, index=index)
        self.df.index.name = 'indicateur'
        self.df.reset_index(inplace=True)
        self.df['ID_Projet'] = self.id_projet
        
        return self.df

    def initialize_database(self, db_name: str = 'database.db') -> None:
        """Initialise la base de données avec la table et les données"""
        self.create_sqlite_table(db_name)
        self.insert_data(db_name)

    def create_sqlite_table(self, db_name: str = 'database.db') -> None:
        """Crée ou écrase la table dans la base SQLite"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS AFS_pop_hh_in_difficulty (
            indicateur TEXT,
            ibt REAL,
            tbse REAL,
            id_projet INTEGER
        )
        """
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS AFS_pop_hh_in_difficulty")
            cursor.execute(create_table_query)
            conn.commit()

    def insert_data(self, db_name: str = 'database.db') -> None:
        """Insère les données du DataFrame dans la table SQLite"""
        if self.df is None:
            self.build_dataframe()
        
        insert_query = """
        INSERT INTO AFS_pop_hh_in_difficulty 
        (indicateur, ibt, tbse, id_projet) 
        VALUES (?, ?, ?, ?)
        """
        
        data_to_insert = [
            (row['indicateur'], row['IBT'], row['TBSE'], row['ID_Projet'])
            for _, row in self.df.iterrows()
        ]
        
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()

    def get_data(self, db_name: str = 'database.db') -> pd.DataFrame:
        """Récupère les données depuis la base SQLite pour l'ID projet"""
        query = """
        SELECT indicateur, ibt, tbse 
        FROM AFS_pop_hh_in_difficulty 
        WHERE id_projet = ?
        """
        
        with sqlite3.connect(db_name) as conn:
            df = pd.read_sql(query, conn, params=(self.id_projet,))
        
        return df