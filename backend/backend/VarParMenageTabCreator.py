import sqlite3

class VarParMenageTabCreator:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Établir la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connexion à {self.db_name} établie avec succès")
        except sqlite3.Error as e:
            print(f"Erreur de connexion: {e}")
    
    def drop_table_if_exists(self):
        """Supprimer la table si elle existe"""
        drop_table_query = "DROP TABLE IF EXISTS VarParMenageResult"
        
        try:
            self.cursor.execute(drop_table_query)
            self.connection.commit()
            print("Table VarParMenageResult supprimée si elle existait")
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de la table: {e}")
    
    def create_table(self):
        """Créer la table avec la structure normalisée"""
        create_table_query = """
        CREATE TABLE VarParMenageResult (
            id_projet INTEGER,
            menage INTEGER,
            tailledelafamille INTEGER,
            nbreenfants INTEGER,
            nbreadultes INTEGER,
            revenunetmois REAL,
            ucoxford REAL,
            ucocde REAL,
            niveaudevieoxford REAL,
            niveaudevieocde REAL,
            poor_oxford INTEGER,
            poor_ocde INTEGER,
            assaini INTEGER,
            sep_t0_ibt_ep REAL,
            sep_tmin_ibt_ep REAL,
            sep_t_ibt_ep REAL,
            sep_t_ibt_pp_ep REAL,
            sep_t0_tbse_ep REAL,
            sep_tmin_tbse_ep REAL,
            sep_t_tbse_ep REAL,
            a_t0_ibt REAL,
            a_tmin_ibt REAL,
            a_t_ibt REAL,
            a_t_ibt_pp REAL,
            a_t0_tbse REAL,
            a_tmin_tbse REAL,
            a_t_tbse REAL,
            sepa_t0_ibt REAL,
            sepa_tmin_ibt REAL,
            sepa_t_ibt REAL,
            sepa_t_ibt_pp REAL,
            sepa_t0_tbse REAL,
            sepa_tmin_tbse REAL,
            sepa_t_tbse REAL,
            par_ibt REAL,
            par_tbse REAL,
            par_ibt_1 INTEGER,
            par_tbse_1 INTEGER,
            par_ibt_2 INTEGER,
            par_tbse_2 INTEGER,
            par_ibt_3 INTEGER,
            par_tbse_3 INTEGER,
            seuil_depenses_trim_par_pct_3_r REAL,
            exces_dep_0_inclus_ibt REAL,
            exces_dep_0_inclus_tbse REAL,
            lz_ina_tbse_menage INTEGER,
            lz_ina_tbse_exces_dep_tbse REAL,
            lz_ina_tbse_rg_normalise REAL,
            lz_ina_tbse_alpha REAL,
            lz_ina_tbse_l_tbse REAL,
            cc_ina_nv_tbse_menage INTEGER,
            cc_ina_nv_tbse_nivvie_ocde REAL,
            cc_ina_nv_tbse_rg_nivvie REAL,
            cc_ina_nv_tbse_rg_ina_tbse REAL,
            cc_ina_nv_tbse_excdep_tbse REAL,
            cc_ina_nv_tbse_alpha REAL,
            cc_ina_nv_tbse_c_tbse REAL,
            lz_ina_ibt_menage INTEGER,
            lz_ina_ibt_exces_dep_ibt REAL,
            lz_ina_ibt_rg_normalise_ibt REAL,
            lz_ina_ibt_alpha REAL,
            lz_ina_ibt_l_ibt REAL,
            cc_ina_nivvie_ibt_menage INTEGER,
            cc_ina_nivvie_ibt_niveau_de_vie_ocde REAL,
            cc_ina_nivvie_ibt_rang_nor_niveau_de_vie REAL,
            cc_ina_nivvie_ibt_rg_inab_ibt REAL,
            cc_ina_nivvie_ibt_exces_dep_ibt REAL,
            cc_ina_nivvie_ibt_alpha REAL,
            cc_ina_nivvie_ibt_c_ibt REAL,
            cc_gen_rang REAL,
            cc_gen_cg_tbse REAL,
            cc_gen_cg_ibt REAL
        )
        """
        
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table 'VarParMenageResult' créée avec succès avec les noms normalisés")
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table: {e}")
    
    def close_connection(self):
        """Fermer la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            print("Connexion fermée")
    
    def run(self, drop_existing=True):
        """
        Exécuter le processus complet de création de la table
        
        Args:
            drop_existing (bool): Si True, supprime la table existante avant de la recréer
        """
        self.connect()
        
        if drop_existing:
            self.drop_table_if_exists()
        
        self.create_table()
        self.close_connection()

# Utilisation de la classe
if __name__ == "__main__":
    # Créer une instance de la classe VarParMenageTabCreator
    db_creator = VarParMenageTabCreator("database.db")
    
    # Créer la table en supprimant l'ancienne si elle existe
    db_creator.run(drop_existing=True)
    
    print("Table VarParMenageResult créée avec succès avec la structure normalisée!")