import pandas as pd
from common_param.CommonTBSETable import CommonTBSETable
from common_param.commonAbSrvCreate import c_Ab_srvCreate

from common_param.CommoAbsrvinsert import CommoAbsrvinsert
from common_param.CommonTarifTBSE import CommonTarifTBSEModel
from common_param.CommonTarifTBSESrv import CommonTarifTBSESrv
from common_param.ComonTarifTableInsertSrv import ComonTarifTableInsert
from common_param.ComonTvaRedTBSEInsertSrv import ComonTvaRedTBSEInsertSrv
from common_param.ComonTvaRedevanceInsertSrv import ComonTavaRedevanceInsertSrv
from common_param.commonAbDataframe import CommonAbDataframe
from common_param.comonNordinInsertSrv import comonNordinInsert


class DatabaseInsertParameterP:
    """
    Gestionnaire centralisé pour l'instanciation et la création de toutes les tables.
    Gère les différents patterns utilisés dans vos classes.
    """

    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.results = {}
        self.errors = {}

    def run_all_insertions(self):
        """Exécute toutes les insertions de données dans la base."""

        print("🗂️  GESTIONNAIRE DE TABLES DE BASE DE DONNÉES")
        print("=" * 50)

        # --- Abonnement ---
        try:
            projet_df = CommonAbDataframe()
            df_ab = projet_df.create_dataframe()
            print("✅ DataFrame généré :")
            print(df_ab)

            inserter = CommoAbsrvinsert(self.db_name)
            inserter.insert_dataframe(df_ab)
            inserter.close()
            print("✅ Insertion terminée dans la table 'commonAb'\n")
        except Exception as e:
            print(f"Erreur lors de l'insertion Abonnement : {e}")
            self.errors['commonAb'] = str(e)

        # --- TBSE Tarif ---
        try:
            df_tarifs = CommonTarifTBSEModel.create_default_dataframe(id_projet_default=1)
            print("2. DataFrame avec données par défaut et id_projet = 1 :")
            print(df_tarifs)
            print()

            service = CommonTarifTBSESrv(self.db_name)
            inserted_ids = service.persist_default_dataframe(id_projet_default=1)
            print(f"Tarifs insérés avec les IDs : {inserted_ids}\n")
        except Exception as e:
            print(f"Erreur lors de l'insertion TBSE Tarif : {e}")
            self.errors['tbse_tarif'] = str(e)

        # --- Nordin ---
        try:
            data_nordin = {
                "id_projet": [1]*11,
                "type_nordin": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP", "EP"],
                "num_tranche": ["T1", "T2", "T3", "T1", "T2", "T3", "T4", "T1", "T2", "T3", "T4"],
                "d_nordin_op": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
                "d_nordin_redevances_ht": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
                "d_nordin_ttc": ["0", "28,247715", "59,672985", "0", "13,53", "16,5", "35,64", "0", "14,717715", "43,172985", "141,924105"],
            }
            df_nordin = pd.DataFrame(data_nordin)

            inserter = comonNordinInsert(self.db_name)
            inserter.insert_dataframe(df_nordin)
            result = inserter.fetch_all()
            print("✅ Insertion Nordin terminée :")
            print(result)
        except Exception as e:
            print(f"Erreur lors de l'insertion Nordin : {e}")
            self.errors['nordin'] = str(e)

        # --- Tarif ---
        try:
            data_tarif = {
                "id_projet": [1]*10,
                "type_tarif": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP"],
                "indice": ["k0", "k1", "k2", "k0", "k1", "k2", "k3", "k0", "k1", "k2"],
                "bornes": [0, 15, 30, 0, 15, 30, 60, 0, 15, 30],
                "prix_ht_op": [2.178, 3.959, 4.978, 1.3, 2.12, 2.21, 2.5, 0.878, 1.839, 2.768],
                "redevances": [0.16, 0.16, 0.16, 0.04, 0.04, 0.04, 0.04, 0.12, 0.12, 0.12],
                "prix_htva": [2.338, 4.119, 5.138, 1.34, 2.16, 2.25, 2.54, 0.998, 1.959, 2.888],
                "montant_tva_unite_service": [0.154958, 0.257139, 0.285648, 0.134, 0.216, 0.225, 0.254, 0.020958, 0.041139, 0.060648],
                "prix_ttc": [2.492958, 4.376139, 5.423648, 1.474, 2.376, 2.475, 2.794, 1.018958, 2.000139, 2.948648]
            }
            df_tarif = pd.DataFrame(data_tarif)

            service = ComonTarifTableInsert(self.db_name)
            service.create_table()
            service.insert_dataframe(df_tarif)
            print("✅ Données insérées avec succès dans la table comon_tarif.\n")
        except Exception as e:
            print(f"Erreur lors de l'insertion Tarif : {e}")
            self.errors['tarif'] = str(e)

        # --- TVA et Redevance ---
        try:
            data_tva = {
                'id_projet': [1, 1, 1],
                'type_taxe': ['EPA', 'A', 'EP'],
                'taux_tva_pourcent': [0, 10, 2.1],
                'redevances_accise_euro_m3': [0.16, 0.04, 0.12]
            }
            df_tva = pd.DataFrame(data_tva)

            inserter = ComonTavaRedevanceInsertSrv()
            inserter.insert_from_dataframe(df_tva)
            print("✅ Insertion TVA et redevance terminée avec succès !\n")
        except Exception as e:
            print(f"Erreur lors de l'insertion TVA et redevance : {e}")
            self.errors['tva_redevance'] = str(e)

        # --- TVA et redevance TBSE ---
        try:
            df_tva_tbse = pd.DataFrame({
                'id_projet': [1, 1, 1],
                'type_tva': ['EPA', 'A', 'EPA'],
                'taux_tva_pct': [0, 10, 2.1],
                'redevances_accise_eur_m3': [0.16, 0.04, 0.12]
            })

            inserter = ComonTvaRedTBSEInsertSrv(self.db_name)
            inserter.insert_dataframe(df_tva_tbse)
            inserter.close()
            print("✅ Insertion TVA et redevance TBSE terminée.\n")
        except Exception as e:
            print(f"Erreur lors de l'insertion TVA et redevance TBSE : {e}")
            self.errors['tva_tbse'] = str(e)


if __name__ == "__main__":
    manager = DatabaseInsertParameterP("database.db")
    manager.run_all_insertions()
