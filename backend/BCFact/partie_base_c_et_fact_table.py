import sqlite3
import os

class PartieBaseCEtFactTable:
    """
    Classe pour gérer la création et les opérations sur la base de données SQLite.
    """
    
    def __init__(self, db_name="database.db"):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_name (str): Nom du fichier de base de données
        """
        self.db_name = db_name
        self.connection = None
    
    def connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Connexion établie avec {self.db_name}")
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion : {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            self.connection.close()
            print("Connexion fermée")
    
    def create_table_partie_base_c_et_fact_table(self):
        """
        Crée la table partie_base_c_et_fact_table avec le schéma spécifié.
        Toutes les colonnes sont de type REAL pour stocker des valeurs numériques.
        """
        
        # Définition du schéma de la table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS partie_base_c_et_fact_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Colonnes vexp_cc
            vexp_cc_men REAL,
            vexp_cc_ass REAL,
            vexp_cc_const REAL,
            vexp_cc_tfam REAL,
            vexp_cc_snwa REAL,
            vexp_cc_swim REAL,
            vexp_cc_gwt REAL,
            
            -- Colonnes c_cb
            c_cb_const REAL,
            c_cb_tfam REAL,
            c_cb_snwa REAL,
            c_cb_r_swim REAL,
            c_cb_r_gwt REAL,
            c_cb_tot REAL,
            c_cb_c_m3_j REAL,
            c_cb_c_m3_t REAL,
            
            -- Colonnes d_cb_t
            d_cb_t_q01 REAL,
            d_cb_t_c_ct3 REAL,
            d_cb_t_q02 REAL,
            d_cb_t_c_ct4 REAL,
            d_cb_t_q03 REAL,
            d_cb_t_q04 REAL,
            
            -- Colonnes r_ep_cb (première série)
            r_ep_cbp_opeab REAL,
            r_ep_cbabt1 REAL,
            r_ep_cbt1t2_1 REAL,
            r_ep_cbt2t3_1 REAL,
            r_ep_cbt3t4_1 REAL,
            r_ep_cbt4total_1 REAL,
            r_ep_cbp_aet_f REAL,
            r_ep_cbt_ft1 REAL,
            r_ep_cbt1t2_2 REAL,
            r_ep_cbt2t3_2 REAL,
            r_ep_cbt3t4_2 REAL,
            r_ep_cbt4total_2 REAL,
            r_ep_cbp_etatab REAL,
            r_ep_cbabt1_2 REAL,
            r_ep_cbt1t2_3 REAL,
            r_ep_cbt2t3_3 REAL,
            r_ep_cbt3t4_3 REAL,
            r_ep_cbt4total_3 REAL,
            r_ep_cbt_da_ttcAbo_TTC REAL,
            r_ep_cbAbo_TTCt1 REAL,
            r_ep_cbt1t2_4 REAL,
            r_ep_cbt2t3_4 REAL,
            r_ep_cbt3t4_4 REAL,
            r_ep_cbt4_t_hors_ab_ttc REAL,
            r_ep_cb_t_hors_ab_ttcfa_t_ttc REAL,
            
            -- Colonnes r_a_cb_ep
            r_a_cb_epp_opeab REAL,
            r_a_cb_epabt1 REAL,
            r_a_cb_ept1t2_1 REAL,
            r_a_cb_ept2t3_1 REAL,
            r_a_cb_ept3t4_1 REAL,
            r_a_cb_ept4total_1 REAL,
            r_a_cb_epp_aet_f REAL,
            r_a_cb_ept_ft1 REAL,
            r_a_cb_ept1t2_2 REAL,
            r_a_cb_ept2t3_2 REAL,
            r_a_cb_ept3t4_2 REAL,
            r_a_cb_ept4total_2 REAL,
            r_a_cb_ep_p_etatab REAL,
            r_a_cb_ep_p_etatt1 REAL,
            r_a_cb_ep_p_etatt2 REAL,
            r_a_cb_ep_p_etatt3 REAL,
            r_a_cb_ep_p_etatt4 REAL,
            r_a_cb_ep_p_etattotal REAL,
            r_a_cb_ep_t_da_ttcAbo_TTC REAL,
            r_a_cb_ep_t_da_ttct1 REAL,
            r_a_cb_ep_t_da_ttct2 REAL,
            r_a_cb_ep_t_da_ttct3 REAL,
            r_a_cb_ep_t_da_ttct4 REAL,
            r_a_cb_ep_t_da_ttc_t_hors_ab_ttc REAL,
            r_a_cb_ep_t_da_ttcfa_t_ttc REAL,
            
            -- Colonnes r_cb_epa_p
            r_cb_epa_p_opeab REAL,
            r_cb_epa_p_opet1 REAL,
            r_cb_epa_p_opet2 REAL,
            r_cb_epa_p_opet3 REAL,
            r_cb_epa_p_opet4 REAL,
            r_cb_epa_p_opetotal REAL,
            r_cb_epa_p_aet_f REAL,
            r_cb_epa_p_aet1 REAL,
            r_cb_epa_p_aet2 REAL,
            r_cb_epa_p_aet3 REAL,
            r_cb_epa_p_aet4 REAL,
            r_cb_epa_p_aetotal REAL,
            r_cb_epa_p_etatab REAL,
            r_cb_epa_p_etatt1 REAL,
            r_cb_epa_p_etatt2 REAL,
            r_cb_epa_p_etatt3 REAL,
            r_cb_epa_p_etatt4 REAL,
            r_cb_epa_p_etattotal REAL,
            r_cb_epa_t_da_ttcAbo_TTC REAL,
            r_cb_epa_t_da_ttct1 REAL,
            r_cb_epa_t_da_ttct2 REAL,
            r_cb_epa_t_da_ttct3 REAL,
            r_cb_epa_t_da_ttct4 REAL,
            r_cb_epa_t_da_ttc_t_hors_ab_ttc REAL,
            r_cb_epa_t_da_ttcfa_t_ttc REAL,
            
            -- Colonnes epot_p
            epot_p_fpart_op REAL,
            epot_p_fpart_agence REAL,
            epot_p_fpart_etat REAL,
            epot_p_ftotal_pf REAL,
            epot_p_vpart_op REAL,
            epot_p_vpart_agence REAL,
            epot_p_vpart_etat REAL,
            epot_p_vtotal_pf REAL,
            
            -- Colonnes epot_f_nd
            epot_f_nd_vpart_op REAL,
            epot_f_nd_vpart_agence REAL,
            epot_f_nd_vpart_etat REAL,
            epot_f_nd_vf_ep_ttc REAL,
            epot_f_nd_vv_f_ep REAL,
            
            -- Colonnes ass_p
            ass_p_f_part_op REAL,
            ass_p_f_part_agence REAL,
            ass_p_f_part_etat REAL,
            ass_p_f_total_pf REAL,
            ass_p_v_part_op REAL,
            ass_p_v_part_agence REAL,
            ass_p_v_part_etat REAL,
            ass_p_v_total_pf REAL,
            
            -- Colonnes ass_f_nd
            ass_f_nd_v_part_op REAL,
            ass_f_nd_v_part_agence REAL,
            ass_f_nd_v_part_etat REAL,
            ass_f_nd_v_f_ep_ttc REAL,
            ass_f_nd_v_v_f_ep REAL,
            
            -- Colonnes s_epa_p
            s_epa_p_f_part_op REAL,
            s_epa_p_f_part_agence REAL,
            s_epa_p_f_part_etat REAL,
            s_epa_p_f_total_pf REAL,
            s_epa_p_v_part_op REAL,
            s_epa_p_v_part_agence REAL,
            s_epa_p_v_part_etat REAL,
            s_epa_p_v_total_pf REAL,
            
            -- Colonnes s_epa_f_nd
            s_epa_f_nd_v_part_op REAL,
            s_epa_f_nd_v_part_agence REAL,
            s_epa_f_nd_v_part_etat REAL,
            s_epa_f_nd_v_f_ep_ttc REAL,
            s_epa_f_nd_v_v_f_ep REAL,
            
            -- Horodatage
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            if not self.connection:
                print("Aucune connexion active. Tentative de connexion...")
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            print("Table partie_base_c_et_fact_table créée avec succès!")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table : {e}")
            return False
    
    def get_table_info(self, table_name="partie_base_c_et_fact_table"):
        """
        Récupère les informations sur la structure de la table.
        
        Args:
            table_name (str): Nom de la table
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"\nStructure de la table {table_name}:")
            print("=" * 50)
            for column in columns:
                print(f"Colonne: {column[1]}, Type: {column[2]}, Null: {'Non' if column[3] else 'Oui'}")
            
            return columns
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des informations : {e}")
            return None
    
    def insert_sample_data(self):
        """Insère quelques données d'exemple dans la table partie_base_c_et_fact_table."""
        try:
            cursor = self.connection.cursor()
            
            # Exemple d'insertion avec quelques colonnes
            sample_data = {
                'vexp_cc_men': 1000.50,
                'vexp_cc_ass': 250.75,
                'c_cb_const': 500.25,
                'epot_p_fpart_op': 750.00
            }
            
            columns = ', '.join(sample_data.keys())
            placeholders = ', '.join(['?' for _ in sample_data])
            values = list(sample_data.values())
            
            sql = f"INSERT INTO partie_base_c_et_fact_table ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            self.connection.commit()
            
            print("Données d'exemple insérées avec succès!")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion : {e}")
            return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une instance du gestionnaire de base de données
    db_manager = PartieBaseCEtFactTable("database.db")
    
    # Se connecter à la base de données
    if db_manager.connect():
        
        # Créer la table partie_base_c_et_fact_table
        if db_manager.create_table_partie_base_c_et_fact_table():
            
            # Afficher les informations sur la table
            db_manager.get_table_info("partie_base_c_et_fact_table")
            
            # Insérer des données d'exemple
            db_manager.insert_sample_data()
            
        # Fermer la connexion
        db_manager.disconnect()
    
    else:
        print("Impossible de se connecter à la base de données")