import sqlite3

class SurplusAgregeTrmt:
    """
    Classe pour gérer la mise à jour de la table surplus_agrege
    dans une base de données SQLite.
    """

    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def update_diff_quantile(self, id_projet):
        """
        Met à jour la colonne diff_quantile_ref pour un projet donné.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = """
                    UPDATE surplus_agrege 
                    SET diff_quantile_ref = (c_tbse_a_ttc_qb_m3_trim - consommation_eau_m3_trimestre)
                    WHERE id_projet = ?
                """
                cur.execute(sql, (id_projet,))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"[surplus_agrege] diff_quantile_ref mis à jour pour id_projet {id_projet}.")
                    return True
                else:
                    print(f"[surplus_agrege] Aucune ligne modifiée pour id_projet {id_projet}.")
                    return False
        except sqlite3.Error as error:
            print(f"Erreur update diff_quantile: {error}")
            return False

    def update_c_ibt(self, id_projet):
        """
        Met à jour la colonne c_ibt_a_ttc_d_ibt_a pour un projet donné.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = """
                    UPDATE surplus_agrege
                    SET c_ibt_a_ttc_d_ibt_a = c_ibt_a_ttc_c_surpercept - consommation_eau_m3_trimestre
                    WHERE id_projet = ?
                """
                cur.execute(sql, (id_projet,))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"[surplus_agrege] c_ibt_a_ttc_d_ibt_a mis à jour pour id_projet {id_projet}.")
                    return True
                else:
                    print(f"[surplus_agrege] Aucune ligne modifiée pour id_projet {id_projet}.")
                    return False
        except sqlite3.Error as error:
            print(f"Erreur update c_ibt: {error}")
            return False

    def verify_update(self, id_projet):
        """
        Vérifie les valeurs mises à jour pour un projet donné.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = """
                    SELECT id_projet, 
                           c_tbse_a_ttc_qb_m3_trim, 
                           consommation_eau_m3_trimestre, 
                           diff_quantile_ref,
                           c_ibt_a_ttc_c_surpercept,
                           c_ibt_a_ttc_d_ibt_a
                    FROM surplus_agrege 
                    WHERE id_projet = ?
                """
                cur.execute(sql, (id_projet,))
                result = cur.fetchone()
                if result:
                    print(f"--- Vérification id_projet {result[0]} ---")
                    print(f"c_tbse_a_ttc_qb_m3_trim: {result[1]}")
                    print(f"consommation_eau_m3_trimestre: {result[2]}")
                    print(f"diff_quantile_ref: {result[3]} (attendu: {result[1] - result[2]})")
                    print(f"c_ibt_a_ttc_c_surpercept: {result[4]}")
                    print(f"c_ibt_a_ttc_d_ibt_a: {result[5]} (attendu: {result[4] - result[2]})")
                    return result
                else:
                    print(f"Aucun résultat trouvé pour id_projet {id_projet}")
                    return None
        except sqlite3.Error as error:
            print(f"Erreur vérification: {error}")
            return None

    def get_all_projects(self):
        """
        Récupère tous les id_projet distincts.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = "SELECT DISTINCT id_projet FROM surplus_agrege ORDER BY id_projet"
                cur.execute(sql)
                results = cur.fetchall()
                return [row[0] for row in results] if results else []
        except sqlite3.Error as error:
            print(f"Erreur récupération projets: {error}")
            return []


if __name__ == "__main__":
    traitement = SurplusAgregeTrmt('database.db')

    id_projet_test = 1

    # Exemple 1 : mise à jour du diff_quantile_ref
    if traitement.update_diff_quantile(id_projet_test):
        traitement.verify_update(id_projet_test)

    # Exemple 2 : mise à jour du c_ibt_a_ttc_d_ibt_a
    if traitement.update_c_ibt(id_projet_test):
        traitement.verify_update(id_projet_test)

    # Exemple 3 : liste de tous les projets
    projets = traitement.get_all_projects()
    print("Projets disponibles:", projets)
