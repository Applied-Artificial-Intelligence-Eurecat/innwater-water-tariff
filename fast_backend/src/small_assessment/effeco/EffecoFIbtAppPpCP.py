import pandas as pd
from Effeco_facture_ibt_approchee_pp import Effeco_facture_ibt_approchee_PP

class EffecoFIbtAppPp:
    def __init__(self, filepath: str = "Facture_IBT_approchee_PP_data.xls", sheet_name: int = 0):
        """
        Initialise la classe avec les paramètres de tarification et charge les données de base.
        
        :param filepath: chemin vers le fichier Excel des données PP
        :param sheet_name: index ou nom de la feuille à lire
        """
        # Initialisation du lecteur de données
        self.data_reader = Effeco_facture_ibt_approchee_PP(filepath, sheet_name)
        self.df_base = None  # DataFrame avec les données de base (menage, assaini, c_m3_trim)
        self.df_calcul = None  # DataFrame avec tous les calculs
        
        # Seuils
        self.t_ep_seuil_max_1 = 15
        self.t_ep_seuil_max_2 = 30
        self.t_ep_seuil_max_3 = 60
        
        # Prix HT Opérations
        self.p_HT_Op_1 = 18.69
        self.p_HT_Op_2 = 0.878
        self.p_HT_Op_3 = 1.839
        self.p_HT_Op_4 = 2.768
        self.p_HT_Op_5 = 4.38
        
        # Redevances
        self.tarif_ep_redevances = 0
        self.redevances_accise_euro_m3 = 0.12
        self.redevances_abonnement = 0
        self.redevances_accise_eur_m3_a = 0.04  # ⚠️ différent de redevances_accise_euro_m3
        
        # Montants TVA par unité
        self.mnt_tva_unite_1 = 0.39249
        self.mnt_tva_unite_2 = 0.020958
        self.mnt_tva_unite_3 = 0.041139
        self.mnt_tva_unite_4 = 0.060648
        self.mnt_tva_unite_5 = 0.0945
        
        # Prix HT + TVA
        self.prix_h_tva_1 = 15.545
        self.prix_h_tva_2 = 1.3
        self.prix_h_tva_3 = 2.12
        self.prix_h_tva_4 = 2.21
        self.prix_h_tva_5 = 2.5
        
        # Montants TVA
        self.montant_tva_1 = 1.5545
        self.montant_tva_2 = 0.134
        self.montant_tva_3 = 0.216
        self.montant_tva_4 = 0.225
        self.montant_tva_5 = 0.254
    
    def load_base_data(self):
        """
        Charge les données de base depuis le fichier Excel en utilisant Effeco_facture_ibt_approchee_PP
        """
        try:
            # Lecture des données depuis le fichier Excel
            self.data_reader.read_excel()
            self.df_base = self.data_reader.get_dataframe()
            
            print(f"Données de base chargées : {len(self.df_base)} lignes")
            print(f"Colonnes disponibles : {list(self.df_base.columns)}")
            
            return self.df_base
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement des données de base : {e}")
    
    def create_dataframe(self):
        """
        Crée un DataFrame avec la structure complète en utilisant les données de base chargées
        """
        # Si les données de base ne sont pas encore chargées, les charger
        if self.df_base is None:
            self.load_base_data()
        
        # Colonnes calculées à ajouter aux colonnes de base
        colonnes_calcul = [
            "q_01", "calcul_c_t3", "q_02", "calcul_c_t4", "q_03", "q_04",
            "ep_ab", "ep_t1", "ep_t2", "ep_t3", "ep_t4", "ep_tot",
            "ep_taxe_forf", "ep_taxe_t1", "ep_taxe_t2", "ep_taxe_t3", "ep_taxe_t4", "ep_taxe_tot",
            "ep_ab_ht", "ep_ab_ht_t1", "ep_ab_ht_t2", "ep_ab_ht_t3", "ep_ab_ht_t4", "ep_ab_ht_tot",
            "ep_ab_ttc", "ep_T1", "ep_T2", "ep_T3", "ep_T4", "ep_tot_dep_ttc_hors_ab", "ep_mnt_F_ttc",
            "a_ab", "a_t1", "a_t2", "a_t3", "a_t4", "a_tot",
            "a_taxe_forf", "a_taxe_t1", "a_taxe_t2", "a_taxe_t3", "a_taxe_t4", "a_taxe_tot",
            "a_ab_ht", "a_ab_ht_t1", "a_ab_ht_t2", "a_ab_ht_t3", "a_ab_ht_t4", "a_ab_ht_tot",
            "a_ab_ttc", "a_T1", "a_T2", "a_T3", "a_T4", "a_tot_dep_ttc_hors_ab", "a_mnt_F_ttc",
            "epa_ab", "epa_t1", "epa_t2", "epa_t3", "epa_t4", "epa_tot",
            "epa_taxe_forf", "epa_taxe_t1", "epa_taxe_t2", "epa_taxe_t3", "epa_taxe_t4", "epa_taxe_tot",
            "epa_ab_ht", "epa_ab_ht_t1", "epa_ab_ht_t2", "epa_ab_ht_t3", "epa_ab_ht_t4", "epa_ab_ht_tot",
            "epa_ab_ttc", "epa_T1", "epa_T2", "epa_T3", "epa_T4", "epa_tot_dep_ttc_hors_ab", "epa_mnt_F_ttc"
        ]
        
        # Créer une copie du DataFrame de base
        self.df_calcul = self.df_base.copy()
        
        # Ajouter les colonnes calculées avec des valeurs par défaut (NaN)
        for col in colonnes_calcul:
            self.df_calcul[col] = None
        
        print(f"DataFrame créé avec {len(self.df_calcul)} lignes et {len(self.df_calcul.columns)} colonnes")
        print(f"Colonnes de base : {list(self.df_base.columns)}")
        print(f"Colonnes ajoutées : {len(colonnes_calcul)}")
        
        return self.df_calcul
    
    def get_base_dataframe(self):
        """
        Retourne le DataFrame de base (menage, assaini, c_m3_trim)
        """
        if self.df_base is None:
            raise ValueError("Les données de base ne sont pas encore chargées. Utilisez load_base_data() d'abord.")
        return self.df_base
    
    def get_calcul_dataframe(self):
        """
        Retourne le DataFrame complet avec toutes les colonnes
        """
        if self.df_calcul is None:
            raise ValueError("Le DataFrame de calcul n'est pas encore créé. Utilisez create_dataframe() d'abord.")
        return self.df_calcul
    
    def get_base_info(self):
        """
        Retourne des informations sur les données de base
        """
        if self.df_base is None:
            return {"error": "Données de base non chargées"}
        
        return self.data_reader.get_info()
    
    def get_unique_menages(self):
        """
        Retourne la liste des ménages uniques
        """
        if self.df_base is None:
            raise ValueError("Les données de base ne sont pas encore chargées.")
        
        return self.data_reader.get_unique_menages()
    
    def filter_by_menage(self, menage_id):
        """
        Filtre les données par ID de ménage
        """
        if self.df_calcul is None:
            raise ValueError("Le DataFrame de calcul n'est pas encore créé.")
        
        return self.df_calcul[self.df_calcul['menage'] == menage_id]
    
    def calculate_all_columns(self):
        """
        Applique toutes les règles de calcul pour remplir les colonnes du DataFrame
        """
        if self.df_calcul is None:
            raise ValueError("Le DataFrame de calcul n'est pas encore créé. Utilisez create_dataframe() d'abord.")
        
        print("Application des règles de calcul...")
        
        # === ÉTAPE 1: Calculs de base des quantités ===
        self.df_calcul['q_01'] = self.df_calcul['c_m3_trim'].apply(lambda x: min(x, self.t_ep_seuil_max_1))
        self.df_calcul['calcul_c_t3'] = self.df_calcul['c_m3_trim'].apply(lambda x: max(x - self.t_ep_seuil_max_1, 0))
        self.df_calcul['q_02'] = self.df_calcul['calcul_c_t3'].apply(lambda x: min(x, self.t_ep_seuil_max_2 - self.t_ep_seuil_max_1))
        self.df_calcul['calcul_c_t4'] = self.df_calcul['c_m3_trim'].apply(lambda x: max(x - self.t_ep_seuil_max_2, 0))
        self.df_calcul['q_03'] = self.df_calcul['calcul_c_t4'].apply(lambda x: min(x, self.t_ep_seuil_max_3 - self.t_ep_seuil_max_2))
        self.df_calcul['q_04'] = self.df_calcul['c_m3_trim'].apply(lambda x: max(x - self.t_ep_seuil_max_3, 0))
        
        # === ÉTAPE 2: Calculs EP (Eau Potable) ===
        self.df_calcul['ep_ab'] = self.p_HT_Op_1
        self.df_calcul['ep_t1'] = self.df_calcul['q_01'] * self.p_HT_Op_2
        self.df_calcul['ep_t2'] = self.df_calcul['q_02'] * self.p_HT_Op_3
        self.df_calcul['ep_t3'] = self.df_calcul['q_03'] * self.p_HT_Op_4
        self.df_calcul['ep_t4'] = self.df_calcul['q_04'] * self.p_HT_Op_5
        self.df_calcul['ep_tot'] = (self.df_calcul['ep_ab'] + self.df_calcul['ep_t1'] + 
                                   self.df_calcul['ep_t2'] + self.df_calcul['ep_t3'] + self.df_calcul['ep_t4'])
        
        # === ÉTAPE 3: Calculs EP taxes ===
        self.df_calcul['ep_taxe_forf'] = self.tarif_ep_redevances
        self.df_calcul['ep_taxe_t1'] = self.redevances_accise_euro_m3 * self.df_calcul['q_01']
        self.df_calcul['ep_taxe_t2'] = self.redevances_accise_euro_m3 * self.df_calcul['q_02']
        self.df_calcul['ep_taxe_t3'] = self.redevances_accise_euro_m3 * self.df_calcul['q_03']
        self.df_calcul['ep_taxe_t4'] = self.redevances_accise_euro_m3 * self.df_calcul['q_04']
        self.df_calcul['ep_taxe_tot'] = (self.df_calcul['ep_taxe_forf'] + self.df_calcul['ep_taxe_t1'] + 
                                        self.df_calcul['ep_taxe_t2'] + self.df_calcul['ep_taxe_t3'] + self.df_calcul['ep_taxe_t4'])
        
        # === ÉTAPE 4: Calculs EP HT ===
        self.df_calcul['ep_ab_ht'] = self.mnt_tva_unite_1
        self.df_calcul['ep_ab_ht_t1'] = self.mnt_tva_unite_2 * self.df_calcul['q_01']
        self.df_calcul['ep_ab_ht_t2'] = self.mnt_tva_unite_3 * self.df_calcul['q_02']
        self.df_calcul['ep_ab_ht_t3'] = self.mnt_tva_unite_4 * self.df_calcul['q_03']
        self.df_calcul['ep_ab_ht_t4'] = self.mnt_tva_unite_5 * self.df_calcul['q_04']
        self.df_calcul['ep_ab_ht_tot'] = (self.df_calcul['ep_ab_ht'] + self.df_calcul['ep_ab_ht_t1'] + 
                                         self.df_calcul['ep_ab_ht_t2'] + self.df_calcul['ep_ab_ht_t3'] + self.df_calcul['ep_ab_ht_t4'])
        
        # === ÉTAPE 5: Calculs EP TTC ===
        self.df_calcul['ep_ab_ttc'] = self.df_calcul['ep_ab'] + self.df_calcul['ep_taxe_forf'] + self.df_calcul['ep_ab_ht']
        self.df_calcul['ep_T1'] = self.df_calcul['ep_t1'] + self.df_calcul['ep_taxe_t1'] + self.df_calcul['ep_ab_ht_t1']
        self.df_calcul['ep_T2'] = self.df_calcul['ep_t2'] + self.df_calcul['ep_taxe_t2'] + self.df_calcul['ep_ab_ht_t2']
        self.df_calcul['ep_T3'] = self.df_calcul['ep_t3'] + self.df_calcul['ep_taxe_t3'] + self.df_calcul['ep_ab_ht_t3']
        self.df_calcul['ep_T4'] = self.df_calcul['ep_t4'] + self.df_calcul['ep_taxe_t4'] + self.df_calcul['ep_ab_ht_t4']
        self.df_calcul['ep_tot_dep_ttc_hors_ab'] = (self.df_calcul['ep_t4'] + self.df_calcul['ep_t3'] + 
                                                   self.df_calcul['ep_t2'] + self.df_calcul['ep_t1'])
        self.df_calcul['ep_mnt_F_ttc'] = self.df_calcul['ep_tot_dep_ttc_hors_ab'] + self.df_calcul['ep_ab_ttc']
        
        # === ÉTAPE 6: Calculs A (Assainissement) ===
        self.df_calcul['a_ab'] = self.df_calcul['assaini'] * self.prix_h_tva_1
        self.df_calcul['a_t1'] = self.df_calcul['assaini'] * self.df_calcul['q_01'] * self.prix_h_tva_2
        self.df_calcul['a_t2'] = self.df_calcul['assaini'] * self.df_calcul['q_02'] * self.prix_h_tva_3
        self.df_calcul['a_t3'] = self.df_calcul['assaini'] * self.df_calcul['q_03'] * self.prix_h_tva_4
        self.df_calcul['a_t4'] = self.df_calcul['assaini'] * self.df_calcul['q_04'] * self.prix_h_tva_5
        self.df_calcul['a_tot'] = (self.df_calcul['a_ab'] + self.df_calcul['a_t1'] + 
                                  self.df_calcul['a_t2'] + self.df_calcul['a_t3'] + self.df_calcul['a_t4'])
        
        # === ÉTAPE 7: Calculs A taxes ===
        self.df_calcul['a_taxe_forf'] = self.df_calcul['assaini'] * self.redevances_abonnement
        self.df_calcul['a_taxe_t1'] = self.df_calcul['assaini'] * self.redevances_accise_eur_m3_a * self.df_calcul['q_01']
        self.df_calcul['a_taxe_t2'] = self.df_calcul['assaini'] * self.redevances_accise_eur_m3_a * self.df_calcul['q_02']
        self.df_calcul['a_taxe_t3'] = self.df_calcul['assaini'] * self.redevances_accise_eur_m3_a * self.df_calcul['q_03']
        self.df_calcul['a_taxe_t4'] = self.df_calcul['assaini'] * self.redevances_accise_eur_m3_a * self.df_calcul['q_04']
        self.df_calcul['a_taxe_tot'] = (self.df_calcul['a_taxe_forf'] + self.df_calcul['a_taxe_t1'] + 
                                       self.df_calcul['a_taxe_t2'] + self.df_calcul['a_taxe_t3'] + self.df_calcul['a_taxe_t4'])
        
        # === ÉTAPE 8: Calculs A HT ===
        self.df_calcul['a_ab_ht'] = self.df_calcul['assaini'] * self.montant_tva_1
        self.df_calcul['a_ab_ht_t1'] = self.df_calcul['assaini'] * self.montant_tva_2 * self.df_calcul['q_01']
        self.df_calcul['a_ab_ht_t2'] = self.df_calcul['assaini'] * self.montant_tva_3 * self.df_calcul['q_02']
        self.df_calcul['a_ab_ht_t3'] = self.df_calcul['assaini'] * self.montant_tva_4 * self.df_calcul['q_03']
        self.df_calcul['a_ab_ht_t4'] = self.df_calcul['assaini'] * self.montant_tva_5 * self.df_calcul['q_04']
        self.df_calcul['a_ab_ht_tot'] = (self.df_calcul['a_ab_ht'] + self.df_calcul['a_ab_ht_t1'] + 
                                        self.df_calcul['a_ab_ht_t2'] + self.df_calcul['a_ab_ht_t3'] + self.df_calcul['a_ab_ht_t4'])
        
        # === ÉTAPE 9: Calculs A TTC ===
        self.df_calcul['a_ab_ttc'] = self.df_calcul['a_ab'] + self.df_calcul['a_taxe_forf'] + self.df_calcul['a_ab_ht']
        self.df_calcul['a_T1'] = self.df_calcul['a_t1'] + self.df_calcul['a_taxe_t1'] + self.df_calcul['a_ab_ht_t1']
        self.df_calcul['a_T2'] = self.df_calcul['a_t2'] + self.df_calcul['a_taxe_t2'] + self.df_calcul['a_ab_ht_t2']
        self.df_calcul['a_T3'] = self.df_calcul['a_t3'] + self.df_calcul['a_taxe_t3'] + self.df_calcul['a_ab_ht_t3']
        self.df_calcul['a_T4'] = self.df_calcul['a_t4'] + self.df_calcul['a_taxe_t4'] + self.df_calcul['a_ab_ht_t4']
        self.df_calcul['a_tot_dep_ttc_hors_ab'] = (self.df_calcul['a_t4'] + self.df_calcul['a_t3'] + 
                                                  self.df_calcul['a_t2'] + self.df_calcul['a_t1'])
        self.df_calcul['a_mnt_F_ttc'] = self.df_calcul['a_tot_dep_ttc_hors_ab'] + self.df_calcul['a_ab_ttc']
        
        # === ÉTAPE 10: Calculs EPA (Eau Potable + Assainissement) ===
        self.df_calcul['epa_ab'] = self.df_calcul['ep_ab'] + self.df_calcul['a_ab']
        self.df_calcul['epa_t1'] = self.df_calcul['ep_t1'] + self.df_calcul['a_t1']
        self.df_calcul['epa_t2'] = self.df_calcul['ep_t2'] + self.df_calcul['a_t2']
        self.df_calcul['epa_t3'] = self.df_calcul['ep_t3'] + self.df_calcul['a_t3']
        self.df_calcul['epa_t4'] = self.df_calcul['ep_t4'] + self.df_calcul['a_t4']
        self.df_calcul['epa_tot'] = self.df_calcul['ep_tot'] + self.df_calcul['a_tot']
        
        # === ÉTAPE 11: Calculs EPA taxes ===
        self.df_calcul['epa_taxe_forf'] = self.df_calcul['ep_taxe_forf'] + self.df_calcul['a_taxe_forf']
        self.df_calcul['epa_taxe_t1'] = self.df_calcul['ep_taxe_t1'] + self.df_calcul['a_taxe_t1']
        self.df_calcul['epa_taxe_t2'] = self.df_calcul['ep_taxe_t2'] + self.df_calcul['a_taxe_t2']
        self.df_calcul['epa_taxe_t3'] = self.df_calcul['ep_taxe_t3'] + self.df_calcul['a_taxe_t3']
        self.df_calcul['epa_taxe_t4'] = self.df_calcul['ep_taxe_t4'] + self.df_calcul['a_taxe_t4']
        self.df_calcul['epa_taxe_tot'] = self.df_calcul['ep_taxe_tot'] + self.df_calcul['a_taxe_tot']
        
        # === ÉTAPE 12: Calculs EPA HT ===
        self.df_calcul['epa_ab_ht'] = self.df_calcul['ep_ab_ht'] + self.df_calcul['a_ab_ht']
        self.df_calcul['epa_ab_ht_t1'] = self.df_calcul['ep_ab_ht_t1'] + self.df_calcul['a_ab_ht_t1']
        self.df_calcul['epa_ab_ht_t2'] = self.df_calcul['ep_ab_ht_t2'] + self.df_calcul['a_ab_ht_t2']
        self.df_calcul['epa_ab_ht_t3'] = self.df_calcul['ep_ab_ht_t3'] + self.df_calcul['a_ab_ht_t3']
        self.df_calcul['epa_ab_ht_t4'] = self.df_calcul['ep_ab_ht_t4'] + self.df_calcul['a_ab_ht_t4']
        self.df_calcul['epa_ab_ht_tot'] = self.df_calcul['ep_ab_ht_tot'] + self.df_calcul['a_ab_ht_tot']
        
        # === ÉTAPE 13: Calculs EPA TTC finaux ===
        self.df_calcul['epa_ab_ttc'] = self.df_calcul['ep_ab_ttc'] + self.df_calcul['a_ab_ttc']
        self.df_calcul['epa_T1'] = self.df_calcul['ep_T1'] + self.df_calcul['a_T1']
        self.df_calcul['epa_T2'] = self.df_calcul['ep_T2'] + self.df_calcul['a_T2']
        self.df_calcul['epa_T3'] = self.df_calcul['ep_T3'] + self.df_calcul['a_T3']
        self.df_calcul['epa_T4'] = self.df_calcul['ep_T4'] + self.df_calcul['a_T4']
        self.df_calcul['epa_tot_dep_ttc_hors_ab'] = self.df_calcul['ep_tot_dep_ttc_hors_ab'] + self.df_calcul['a_tot_dep_ttc_hors_ab']
        self.df_calcul['epa_mnt_F_ttc'] = self.df_calcul['ep_mnt_F_ttc'] + self.df_calcul['a_mnt_F_ttc']
        
        print("Calculs terminés avec succès !")
        return self.df_calcul

    def export_to_excel(self, output_path: str = "effeco_fibt_app_pp_result.xlsx"):
        """
        Exporte le DataFrame complet vers un fichier Excel
        """
        if self.df_calcul is None:
            raise ValueError("Le DataFrame de calcul n'est pas encore créé.")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Feuille avec les données complètes
            self.df_calcul.to_excel(writer, sheet_name='Donnees_Completes', index=False)
            
            # Feuille avec uniquement les données de base
            if self.df_base is not None:
                self.df_base.to_excel(writer, sheet_name='Donnees_Base', index=False)
        
        print(f"Données exportées vers : {output_path}")
    
    def __repr__(self):
        base_loaded = "chargées" if self.df_base is not None else "non chargées"
        calcul_created = "créé" if self.df_calcul is not None else "non créé"
        return f"EffecoFIbtAppPp(Données de base: {base_loaded}, DataFrame de calcul: {calcul_created})"


# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Création de l'instance
        effeco = EffecoFIbtAppPp()
        
        print("=== CHARGEMENT DES DONNÉES DE BASE ===")
        # Chargement des données de base
        df_base = effeco.load_base_data()
        print(df_base.head())
        
        print("\n=== INFORMATIONS SUR LES DONNÉES DE BASE ===")
        info = effeco.get_base_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        print("\n=== CRÉATION DU DATAFRAME COMPLET ===")
        # Création du DataFrame complet
        df_complet = effeco.create_dataframe()
        print(f"DataFrame créé avec {len(df_complet.columns)} colonnes")
        
        print("\n=== APPLICATION DES CALCULS ===")
        # Application de tous les calculs
        df_avec_calculs = effeco.calculate_all_columns()
        print(f"Calculs appliqués sur {len(df_avec_calculs)} lignes")
        
        # Affichage d'un échantillon des résultats
        print("\n=== ÉCHANTILLON DES RÉSULTATS ===")
        colonnes_echantillon = ['menage', 'assaini', 'c_m3_trim', 'q_01', 'ep_mnt_F_ttc', 'a_mnt_F_ttc', 'epa_mnt_F_ttc']
        print(df_avec_calculs[colonnes_echantillon].head())
        
        print("\n=== MÉNAGES UNIQUES ===")
        menages = effeco.get_unique_menages()
        print(f"Nombre de ménages uniques : {len(menages)}")
        print(f"Premiers ménages : {menages[:5] if len(menages) > 5 else menages}")
        
        print(f"\n=== ÉTAT DE L'OBJET ===")
        print(effeco)
        
    except Exception as e:
        print(f"Erreur : {e}")