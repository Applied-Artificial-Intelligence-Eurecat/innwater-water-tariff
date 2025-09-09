import sqlite3

class C_et_F_TBSECreateSrv:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # Supprimer la table si elle existe déjà
        cur.execute("DROP TABLE IF EXISTS C_et_F_TBSE")

        # Création de la nouvelle table
        cur.execute("""
        CREATE TABLE C_et_F_TBSE (
            id_projet INTEGER PRIMARY KEY AUTOINCREMENT,
            cons_menage REAL,
            cons_ln_part_captive REAL,
            cons_m3_jour REAL,
            cons_m3_trim REAL,
            cons_assaini REAL,
            c_var_revenu REAL,
            c_var_revenuJour REAL,
            c_var_abTTC REAL,
            c_var_abTTCJour REAL,
            c_var_revMoinsF3 REAL,
            c_var_revMoinsFJour REAL,
            c_var_b1LnP REAL,
            c_var_b2LnRF REAL,
            cons_tbse_somme_ln REAL,
            cons_tbse_m3_jour REAL,
            cons_tbse_m3_trim REAL,
            f_tbse_part_op REAL,
            f_tbse_part_agence REAL,
            f_tbse_part_etat REAL,
            f_tbse_total REAL,
            f_ep_epa_ep_f_p_op REAL,
            f_ep_epa_ep_f_p_ag REAL,
            f_ep_epa_ep_f_p_etat REAL,
            f_ep_epa_ep_f_total_pf REAL,
            f_ep_epa_ep_var_p_op REAL,
            f_ep_epa_ep_var_p_ag REAL,
            f_ep_epa_ep_var_p_etat REAL,
            f_ep_epa_ep_var_total_pv REAL,
            f_ep_epa_ep_fndVar_p_op REAL,
            f_ep_epa_ep_fndVar_p_ag REAL,
            f_ep_epa_ep_fndVar_p_etat REAL,
            f_ep_epa_ep_fndVar_f_ep_ttc REAL,
            f_ep_epa_ep_fndVar_f_ep_ttc_verif REAL,
            f_ep_epa_a_f_p_op REAL,
            f_ep_epa_a_f_p_ag REAL,
            f_ep_epa_a_f_p_etat REAL,
            f_ep_epa_a_f_total_pf REAL,
            f_ep_epa_a_var_p_op REAL,
            f_ep_epa_a_var_p_ag REAL,
            f_ep_epa_a_var_p_etat REAL,
            f_ep_epa_a_var_totalPV REAL,
            f_ep_epa_a_fndVar_p_op REAL,
            f_ep_epa_a_fndVar_p_ag REAL,
            f_ep_epa_a_fndVar_p_etat REAL,
            f_ep_epa_a_fndVar_f_A_TTC REAL,
            f_ep_epa_a_fndVar_f_A_TTC_Verif REAL,
            f_ep_epaep_afp_op REAL,
            f_ep_epaep_afp_ag REAL,
            f_ep_epaep_afp_etat REAL,
            f_ep_epaep_aftotalPF REAL,
            f_ep_epa_ep_a_var_p_op REAL,
            f_ep_epa_ep_a_var_p_ag REAL,
            f_ep_epa_ep_a_var_p_etat REAL,
            f_ep_epa_ep_a_var_totalPV REAL,
            f_ep_epa_ep_a_fndVar_p_op REAL,
            f_ep_epa_ep_a_fndVar_p_ag REAL,
            f_ep_epa_ep_a_fndVar_p_etat REAL,
            f_ep_epa_ep_a_fndVar_f_EP_APA_TTC REAL,
            f_ep_epa_ep_a_fndVar_f_EP_APA_TTC_Verif REAL,
            verifvs REAL
        )
        """)

        conn.commit()
        conn.close()
        print("Table 'C_et_F_TBSE' créée avec succès !")


if __name__ == "__main__":
    db_creator = C_et_F_TBSECreateSrv()
    db_creator.create_table()
