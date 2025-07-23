import pandas as pd
import sqlite3

class aFSPopHhDiffCar:
    def __init__(self, id_projet=1):
        """
        Classe pour construire un DataFrame avec les indicateurs de distribution des revenus.
        
        :param id_projet: entier représentant l'identifiant du projet à ajouter à chaque ligne.
        """
        self.id_projet = id_projet
        self.df = None

    def construire_dataframe(self):
        """
        Construit et retourne un DataFrame disposant de la structure suivante :
        
                        indicateur	        IBT	    TBSE    id_projet
        0	            Gini 	            39.8	39.0    1
        1	            Schutz	            29.2	29.6    1
        2	            Ratio interdéciles	10.6	12.3    1
        3	            Ratio interdécimes	27.9	25.7    1
        4	            Ratio S80 / S20	    12.0	13.1    1
        """
        data = {
            "IBT": [39.8, 29.2, 10.6, 27.9, 12.0],
            "TBSE": [39.0, 29.6, 12.3, 25.7, 13.1],
            "id_projet": [self.id_projet] * 5
        }
        index = ["Gini", "Schutz", "Ratio interdéciles", "Ratio interdécimes", "Ratio S80 / S20"]

        self.df = pd.DataFrame(data, index=index)
        self.df.reset_index(inplace=True)
        self.df.rename(columns={"index": "indicateur"}, inplace=True)
        return self.df

    def creer_table_sqlite(self, nom_table="pop_hh_diff_car", db_name="database.db"):
        """
        Crée une table SQLite et y insère le DataFrame en remplaçant la table existante.
        
        :param nom_table: nom de la table à créer dans la base.
        :param db_name: nom du fichier de base de données SQLite.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été construit. Appelez d'abord construire_dataframe().")

        conn = sqlite3.connect(db_name)
        self.df.to_sql(nom_table, conn, if_exists="replace", index=False)
        conn.close()

        print(f"✅ Table '{nom_table}' créée et remplie dans la base '{db_name}'.")

    def inserer_donnees_sqlite(self, nom_table="pop_hh_diff_car", db_name="database.db"):
        """
        Insère les données du DataFrame dans la table SQLite en mode append (sans remplacer la table).
        
        :param nom_table: nom de la table cible.
        :param db_name: nom du fichier de base de données SQLite.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été construit. Appelez d'abord construire_dataframe().")

        conn = sqlite3.connect(db_name)
        self.df.to_sql(nom_table, conn, if_exists="append", index=False)
        conn.close()

        print(f"✅ Données insérées dans la table '{nom_table}' de la base '{db_name}'.")

# Exemple d'utilisation
if __name__ == "__main__":
    obj = aFSPopHhDiffCar(id_projet=1)
    df = obj.construire_dataframe()
    print(df)

    # Création de la table (avec remplacement)
    obj.creer_table_sqlite()

    # Insertion supplémentaire (append)
    obj.inserer_donnees_sqlite()
