import pandas as pd
import sqlite3

class AFSInequalCalcCar:
    def __init__(self):
        pass

    def creer_dataframe(self, id_projet):
        id_projet = int(id_projet)
        
        data = {
            'id_projet': [id_projet, id_projet],
            'Ensemble': ['Gini', 'Schutz'],
            'IBT': [82.7, 73.5],
            'TBSE': [70.6, 59.1]
        }
        df = pd.DataFrame(data)
        return df

    def creer_table_sqlite(self, table_name='AFSInequalCalcCar'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Supprimer la table si elle existe déjà
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

        # Créer la table
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_projet INTEGER,
                Ensemble TEXT,
                IBT REAL,
                TBSE REAL
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Table '{table_name}' créée avec succès.")

    def inserer_dataframe(self, df, table_name='AFSInequalCalcCar'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insertion manuelle des données ligne par ligne
        for _, row in df.iterrows():
            cursor.execute(f'''
                INSERT INTO {table_name} (id_projet, Ensemble, IBT, TBSE)
                VALUES (?, ?, ?, ?)
            ''', (row['id_projet'], row['Ensemble'], row['IBT'], row['TBSE']))
        
        conn.commit()
        conn.close()
        print(f"Données insérées dans la table '{table_name}' avec succès.")

    def get_data(self, id_projet, table_name='AFSInequalCalcCar'):
        conn = sqlite3.connect('database.db')
        query = f"SELECT id_projet, Ensemble, IBT, TBSE FROM {table_name} WHERE id_projet = ?"
        df = pd.read_sql_query(query, conn, params=(int(id_projet),))
        conn.close()
        return df


# Pour test local rapide (optionnel)
if __name__ == "__main__":
    afs = AFSInequalCalcCar()
    afs.creer_table_sqlite()
    df = afs.creer_dataframe(id_projet=1)
    afs.inserer_dataframe(df)
    print(afs.get_data(1))
