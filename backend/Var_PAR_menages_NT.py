import pandas as pd
import sqlite3


class VarParMenageNT:
    def __init__(self, db_path: str, excel_path: str):
        """
        Classe pour charger et mettre à jour les données des ménages à partir d'un Excel et d'une base SQLite.
        
        :param db_path: Chemin vers la base SQLite
        :param excel_path: Chemin vers le fichier Excel
        """
        self.db_path = db_path
        self.excel_path = excel_path
        self.df = None

    def read_excel(self):
        """
        Lecture du fichier Excel sans préciser de feuille (prend la seule feuille disponible).
        """
        try:
            print("=== Lecture d'un fichier Excel ===")
            self.df = pd.read_excel(self.excel_path)  # pas besoin de sheet_name si 1 seule feuille
            print(f"Nombre de lignes lues : {len(self.df)}")
            return self.df
        except Exception as e:
            print(f"Erreur lors du traitement : Erreur lors de la lecture du fichier: {e}")
            raise

    def save_to_db(self, table_name: str):
        """
        Sauvegarde du DataFrame dans une table SQLite.
        :param table_name: Nom de la table cible
        """
        if self.df is None:
            raise ValueError("Le DataFrame est vide. Veuillez d'abord lire le fichier Excel.")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                self.df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Les données ont été sauvegardées dans la table '{table_name}'.")
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base : {e}")
            raise

    def update_results_in_db(self, table_name: str = "VarParMenageResult"):
        """
        Met à jour la table VarParMenageResult avec les données du DataFrame,
        en utilisant (id_projet, menage) comme clés de rapprochement.
        """
        if self.df is None:
            raise ValueError("Le DataFrame est vide. Veuillez d'abord lire le fichier Excel.")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for _, row in self.df.iterrows():
                    # Préparer les colonnes et valeurs pour l'UPDATE
                    columns = [col for col in row.index if col not in ["id_projet", "menage"]]
                    set_clause = ", ".join([f"{col} = ?" for col in columns])
                    values = [row[col] for col in columns]

                    # Ajouter les clés de rapprochement à la fin
                    values.extend([row["id_projet"], row["menage"]])

                    sql = f"""
                        UPDATE {table_name}
                        SET {set_clause}
                        WHERE id_projet = ? AND menage = ?
                    """
                    cursor.execute(sql, values)

                conn.commit()
            print(f"Table '{table_name}' mise à jour avec succès.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la table : {e}")
            raise


if __name__ == "__main__":
    # 🔧 Chemins à adapter
    db_path = "database.db"                    # ta base SQLite
    excel_path = "Var_PAR_menages_NT.xls"  # ton fichier Excel

    try:
        var_menages = VarParMenageNT(db_path, excel_path)

        # Lecture du fichier Excel
        var_menages.read_excel()

        # Sauvegarde brute dans une table temporaire
        var_menages.save_to_db("VarParMenageExcel")

        # Mise à jour de la table des résultats
        var_menages.update_results_in_db("VarParMenageResult")

    except Exception as e:
        print(f"Erreur globale : {e}")
