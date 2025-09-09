import sqlite3
import pandas as pd
import logging
import os

class PauvreteLevelAnalyzer:
    def __init__(self, db_path: str, seuil_pauvrete: float = 1200.0):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"La base de données {db_path} n'existe pas.")
        self.db_path = db_path
        self.seuil_pauvrete = seuil_pauvrete
        self.data = None
        self.id_projet = 1
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _get_query(self) -> str:
        return f"""
        SELECT
            {self.id_projet} AS id_projet,
            i_new AS menage,
            nbpers AS tailledelafamille,
            nenf AS nbreenfants,
            ("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)") AS nbreadultes,
            revenu AS revenunetmois,
            uc1 AS ucoxford,
            (1 + 0.5*(("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)")-1) + 0.3*nenf) AS ucocde,
            CASE WHEN uc1 > 0 THEN ROUND(revenu/uc1,2) ELSE NULL END AS niveaudevieoxford,
            CASE WHEN (1 + 0.5*(("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)")-1) + 0.3*nenf) > 0
                 THEN ROUND(revenu/(1 + 0.5*(("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)")-1) + 0.3*nenf),2)
                 ELSE NULL END AS niveaudevieocde,
            CASE WHEN uc1 > 0 AND (revenu/uc1) < {self.seuil_pauvrete} THEN 1 ELSE 0 END AS poor_oxford,
            CASE WHEN (1 + 0.5*(("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)")-1) + 0.3*nenf) > 0
                 AND (revenu/(1 + 0.5*(("naa (Nombre d'adultes actifs)" + "nana (Nombre d'adultes non actifs)")-1) + 0.3*nenf)) < {self.seuil_pauvrete} THEN 1 ELSE 0 END AS poor_ocde,
            "Assainissement Collectif (1 = oui)" AS assaini
        FROM la_reunion_data
        WHERE revenu IS NOT NULL AND uc1 IS NOT NULL AND nbpers > 0
        ORDER BY i_new
        """

    def load_data(self):
        try:
            self.logger.info(f"Connexion à la base de données : {self.db_path}")
            with sqlite3.connect(self.db_path) as conn:
                self.data = pd.read_sql_query(self._get_query(), conn)
            self.logger.info(f"Données chargées : {len(self.data)} lignes")
            return self.data
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des données : {e}")
            raise

    def prepare_data_for_varparmenage(self):
        if self.data is None:
            self.load_data()
        df = self.data.copy()
        # Ajouter toutes les colonnes manquantes du schéma avec NaN ou None
        cols_real = [
            'sep_t0_ibt_ep','sep_tmin_ibt_ep','sep_t_ibt_ep','sep_t_ibt_pp_ep',
            'sep_t0_tbse_ep','sep_tmin_tbse_ep','sep_t_tbse_ep','a_t0_ibt','a_tmin_ibt',
            'a_t_ibt','a_t_ibt_pp','a_t0_tbse','a_tmin_tbse','a_t_tbse','sepa_t0_ibt',
            'sepa_tmin_ibt','sepa_t_ibt','sepa_t_ibt_pp','sepa_t0_tbse','sepa_tmin_tbse',
            'sepa_t_tbse','par_ibt','par_tbse','exces_dep_0_inclus_ibt','exces_dep_0_inclus_tbse',
            'lz_ina_tbse_exces_dep_tbse','lz_ina_tbse_rg_normalise','lz_ina_tbse_alpha',
            'lz_ina_tbse_l_tbse','cc_ina_nv_tbse_nivvie_ocde','cc_ina_nv_tbse_rg_nivvie',
            'cc_ina_nv_tbse_rg_ina_tbse','cc_ina_nv_tbse_excdep_tbse','cc_ina_nv_tbse_alpha',
            'cc_ina_nv_tbse_c_tbse','lz_ina_ibt_exces_dep_ibt','lz_ina_ibt_rg_normalise_ibt',
            'lz_ina_ibt_alpha','lz_ina_ibt_l_ibt','cc_ina_nivvie_ibt_niveau_de_vie_ocde',
            'cc_ina_nivvie_ibt_rang_nor_niveau_de_vie','cc_ina_nivvie_ibt_rg_inab_ibt',
            'cc_ina_nivvie_ibt_exces_dep_ibt','cc_ina_nivvie_ibt_alpha','cc_ina_nivvie_ibt_c_ibt',
            'cc_gen_rang','cc_gen_cg_tbse','cc_gen_cg_ibt'
        ]
        cols_int = ['par_ibt_1','par_tbse_1','par_ibt_2','par_tbse_2','par_ibt_3','par_tbse_3','lz_ina_tbse_menage',
                    'cc_ina_nv_tbse_menage','lz_ina_ibt_menage','cc_ina_nivvie_ibt_menage']
        for col in cols_real:
            df[col] = None
        for col in cols_int:
            df[col] = None
        return df

    def insert_into_varparmenage(self, clear_existing=True):
        df = self.prepare_data_for_varparmenage()
        try:
            with sqlite3.connect(self.db_path) as conn:
                if clear_existing:
                    conn.execute("DELETE FROM VarParMenageResult WHERE id_projet=?", (self.id_projet,))
                df.to_sql('VarParMenageResult', conn, if_exists='append', index=False)
                count = conn.execute("SELECT COUNT(*) FROM VarParMenageResult WHERE id_projet=?", (self.id_projet,)).fetchone()[0]
            self.logger.info(f"Lignes insérées : {count}")
            return count
        except Exception as e:
            self.logger.error(f"Erreur insertion : {e}")
            raise

# -------------------- MAIN --------------------
if __name__ == "__main__":
    try:
        analyzer = PauvreteLevelAnalyzer("database.db", seuil_pauvrete=1200)
        analyzer.id_projet = 1
        analyzer.load_data()
        inserted = analyzer.insert_into_varparmenage()
        print(f"Lignes insérées dans VarParMenageResult : {inserted}")
    except Exception as e:
        print(f"Erreur : {e}")
