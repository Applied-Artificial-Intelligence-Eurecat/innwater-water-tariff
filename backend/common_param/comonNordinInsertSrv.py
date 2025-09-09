import sqlite3
import pandas as pd

class comonNordinInsert:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

    def insert_dataframe(self, df: pd.DataFrame):
        # Conversion des colonnes numériques qui utilisent des virgules
        for col in ["d_nordin_op", "d_nordin_redevances_ht", "d_nordin_ttc"]:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

        # Supprimer les anciennes lignes des projets présents dans le DataFrame
        projets = df['id_projet'].unique()
        for projet in projets:
            self.conn.execute("DELETE FROM comonNordin WHERE id_projet=?", (projet,))
        self.conn.commit()

        # Insertion des nouvelles données
        df.to_sql("comonNordin", self.conn, if_exists='append', index=False)

    def fetch_all(self) -> pd.DataFrame:
        return pd.read_sql_query("SELECT * FROM comonNordin", self.conn)


def main():
    # Construction du DataFrame directement
    data = {
        "id_projet": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "type_nordin": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP", "EP"],
        "num_tranche": ["T1", "T2", "T3", "T1", "T2", "T3", "T4", "T1", "T2", "T3", "T4"],
        "d_nordin_op": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
        "d_nordin_redevances_ht": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
        "d_nordin_ttc": ["0", "28,247715", "59,672985", "0", "13,53", "16,5", "35,64", "0", "14,717715", "43,172985", "141,924105"],
    }

    df = pd.DataFrame(data)

    inserter = comonNordinInsert("database.db")
    inserter.insert_dataframe(df)

    # Affichage du contenu de la table
    result = inserter.fetch_all()
    print(result)


if __name__ == "__main__":
    main()
