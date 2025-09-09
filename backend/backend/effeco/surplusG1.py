import pandas as pd
import sqlite3
from typing import Optional, List, Dict, Any
import logging
import os

class MenageAssaini:
    """
    Classe pour gérer une table de données de ménages assainis
    avec des informations sur la consommation d'eau et les tarifs
    """
    
    def __init__(self, db_path: str = "database.db", dev_mode: bool = None):
        self.db_path = db_path
        self.table_name = "surplusG1TBSE"
        
        # Déterminer le mode développement
        if dev_mode is not None:
            self.dev_mode = dev_mode
        else:
            self.dev_mode = os.getenv('DEV', '0') == '1'
        
        # Schéma de la table
        self.schema = {
            'id_projet': 'INTEGER',   # corrigé
            'menage': 'INTEGER',
            'assaini': 'INTEGER',
            'revenu_net_mois': 'REAL',
            'c_m3_trim_1': 'REAL',
            'c_m3_trim_2': 'REAL',
            'c_ibt': 'REAL',
            'c_ibt_pp': 'REAL',
            'c_tbse': 'REAL',
            'consom_nordin_trim': 'REAL',
            'consom_taylor_trim': 'REAL',
            'c_captive_jour': 'REAL',
            'c_nordin_jour': 'REAL',
            'c_taylor_jour': 'REAL',
            'ln_c_captive_jour': 'REAL',
            'ln_c_nordin_jour': 'REAL',
            'ln_c_taylor_jour': 'REAL',
            'sur_consommation_pct': 'REAL',
            'ai_m3_jour': 'REAL',
            'qstar_m3_jour': 'REAL',
            'conso_qstar_cout_complet_m3_trim': 'REAL',
            'demande_inverse_bi': 'REAL',
            'tbse_conso_app_ln_qb': 'REAL',
            'tbse_conso_app_qb_m3_jour': 'REAL',
            'tbse_conso_app_qb_m3_trim': 'REAL',
            'tbse_ht_i1': 'REAL',
            'tbse_ht_i2': 'REAL',
            'tbse_ht_t1': 'REAL',
            'tbse_ht_t2': 'REAL',
            'tbse_ht_t1_t2_euro_jour': 'REAL',
            'tbse_ht_trim_i1': 'REAL',
            'tbse_ht_trim_i2': 'REAL',
            'tbse_ht_trim_t1': 'REAL',
            'tbse_ht_trim_t2': 'REAL',
            'tbse_ht_t1_t2_trim_euro_jour': 'REAL',
            'diff_qb_app_conso_tbse_pct': 'REAL',
            'ln_qb_avec_redev': 'REAL',
            'tbse_redev_qb_m3_jour': 'REAL',
            'qb_avec_redev_sans_tva': 'REAL',
            'tbse_redev_i1': 'REAL',
            'tbse_redev_i2': 'REAL',
            'tbse_redev_t1': 'REAL',
            'tbse_redev_t2': 'REAL',
            'tbse_redev_t1_t2_euro_jour': 'REAL',
            'tbse_redev_trim_i1': 'REAL',
            'tbse_redev_trim_i2': 'REAL',
            'tbse_redev_trim_t1': 'REAL',
            'tbse_redev_trim_t2': 'REAL',
            'tbse_redev_trim_t1_t2_euro': 'REAL',
            'diff_qb_redev_tbse': 'REAL',
            'n_qb_ttc': 'REAL',
            'tbse_ttc_qb_m3_jour': 'REAL',
            'qb_ttc': 'REAL',
            'tbse_ttc_i1': 'REAL',
            'tbse_ttc_i2': 'REAL',
            'tbse_ttc_t1': 'REAL',
            'tbse_ttc_t2': 'REAL',
            'tbse_ttc_t1_t2_euro_jour': 'REAL',
            'tbse_ttc_trim_i1': 'REAL',
            'tbse_ttc_trim_i2': 'REAL',
            'tbse_ttc_trim_t1': 'REAL',
            'tbse_ttc_trim_t2': 'REAL',
            'tbse_ttc_trim_t1_t2_euro': 'REAL',
            'gap_qb_tbse_pct': 'REAL'
        }
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        mode_str = "DÉVELOPPEMENT" if self.dev_mode else "PRODUCTION"
        self.logger.info(f"Mode {mode_str} activé (DEV={'1' if self.dev_mode else '0'})")
        
        self.create_table()
    
    def create_table(self, force_drop: bool = False) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                drop_table = self.dev_mode or force_drop
                if drop_table:
                    conn.execute(f"DROP TABLE IF EXISTS {self.table_name}")
                    reason = "mode DEV" if self.dev_mode else "force_drop=True"
                    self.logger.info(f"Table {self.table_name} supprimée ({reason})")
                
                columns = [f"{col_name} {col_type}" for col_name, col_type in self.schema.items()]
                create_query = f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    {', '.join(columns)}
                )
                """
                conn.execute(create_query)
                conn.commit()
                self.logger.info(f"Table {self.table_name} recréée/créée avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la table: {e}")
            raise
    
    def insert_data(self, data: Dict[str, Any]) -> None:
        try:
            invalid_keys = set(data.keys()) - set(self.schema.keys())
            if invalid_keys:
                raise ValueError(f"Colonnes invalides: {invalid_keys}")
            
            with sqlite3.connect(self.db_path) as conn:
                columns = list(data.keys())
                placeholders = ', '.join(['?' for _ in columns])
                values = list(data.values())
                query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                conn.execute(query, values)
                conn.commit()
                self.logger.info("Données insérées avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'insertion: {e}")
            raise
    
    def insert_bulk_data(self, data_list: List[Dict[str, Any]]) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                for data in data_list:
                    invalid_keys = set(data.keys()) - set(self.schema.keys())
                    if invalid_keys:
                        raise ValueError(f"Colonnes invalides: {invalid_keys}")
                    columns = list(data.keys())
                    placeholders = ', '.join(['?' for _ in columns])
                    values = list(data.values())
                    query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    conn.execute(query, values)
                conn.commit()
                self.logger.info(f"{len(data_list)} lignes insérées avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'insertion en lot: {e}")
            raise
    
    def query_data(self, where_clause: str = "", params: tuple = ()) -> pd.DataFrame:
        try:
            query = f"SELECT * FROM {self.table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn, params=params)
                return df
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête: {e}")
            raise
    
    def transfer_from_menage_data(self) -> pd.DataFrame:
        """
        Transfère les données de 'menage_data' vers 'surplusG1TBSE' en utilisant le mapping.
        Retourne le DataFrame source utilisé pour l'insertion.
        """
        COLUMN_MAPPING = {col: col for col in self.schema.keys()}  # simple mapping identique
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                source_df = pd.read_sql_query("SELECT * FROM menage_data", conn)

            mapped_data = []
            for _, row in source_df.iterrows():
                mapped_row = {dest_col: row[src_col] if src_col in row else None
                              for src_col, dest_col in COLUMN_MAPPING.items()}
                mapped_data.append(mapped_row)

            self.insert_bulk_data(mapped_data)
            self.logger.info(f"{len(mapped_data)} lignes transférées de menage_data vers {self.table_name}")
            return pd.DataFrame(mapped_data)

        except Exception as e:
            self.logger.error(f"Erreur lors du transfert: {e}")
            raise


# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    menage_db = MenageAssaini(dev_mode=1)

    # Exemple de transfert de données depuis menage_data
    try:
        df_source = menage_db.transfer_from_menage_data()
        print(f"DataFrame source créé avec {len(df_source)} lignes pour la table {menage_db.table_name}")
        print(df_source.head())
    except Exception as e:
        print(f"Erreur lors du transfert: {e}")
