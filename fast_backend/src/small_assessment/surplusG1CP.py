import pandas as pd
import numpy as np


class surplusG1CP:
    def __init__(self, dfsource : pd.DataFrame):
        # Élasticités
        self.elasticite_prix_marginal = -0.31
        self.elasticite_revenu_virtuel = 0.25

        # Prix et coûts
        self.Prix_pi = 1.3
        self.cout_marginal_complet_cme = 5.9
        self.redevances_accise_euro_m3 = 0.16

        # Prix hors taxe opérateur (abonnement et tranches EP)
        self.prix_ht_op_a_EP_ab = 18.69
        
        self.prix_ht_op_T_EP_K0 = 0.878
        self.prix_ht_op_T_EP_K1 = 1.839
        self.prix_ht_op_T_EP_K2 = 2.768
        self.prix_ht_op_T_EP_K3 = 4.38

        # Seuils de tranches EP
        self.seuil_T_EP_K1 = 15
        self.seuil_T_EP_K2 = 30
        self.seuil_T_EP_K3 = 60
        self.seuil_T_EP_K1_bis = 15
        self.seuil_T_EP_K2_bis = 30
        self.seuil_T_EP_K3_bis = 60

        # Prix HTVA EPA et tranches
        self.prix_htva_ab_EPA = 18.69
        
        self.prix_htva_t_EP_T1 = 0.998
        self.prix_htva_t_EP_T2 = 1.959
        self.prix_htva_t_EP_T3 = 2.888
        self.prix_htva_t_EP_T4 = 4.5

        # Redevances et coûts environnementaux
        self.redevances_tarif_ep = 0.12
        self.redevances_tarif_a = 0.04
        self.cout_environnemental_ce = 5

        # Montants TVA
        self.montant_tva_k0 = 1.018958
        self.montant_tva_k1 = 2.000139
        self.montant_tva_k2 = 2.948648
        self.montant_tva_k3 = 4.5945

        # TVA, prix TTC et redevances
        self.taux_tva_ep = 2.1
        self.prix_TTC_ab = 19.08249
        self.redevances_K0 = 0.12

        # === Création du DataFrame vide avec toutes les colonnes ===

        self.dfsource = dfsource.copy()

        # Initialisation du DataFrame complet avec toutes les colonnes
        self.df = self.dfsource.reindex(columns=self._get_all_columns())
        #self.df = pd.DataFrame(columns=self._get_all_columns())
        

    def _get_all_columns(self):
        """Retourne la liste complète des colonnes du DataFrame."""
        combined_columns = [
    # éléments de la seconde liste (92 colonnes)
    "menage","assaini","revenu_net_mois","c_m3_trim","c_m3_trim_2",
    "c_ibt","c_ibt_pp","c_tbse","consom_nordin_trim","consom_taylor_trim",
    "c_captive_jour","c_nordin_jour","c_taylor_jour","ln_c_captive_jour",
    "ln_c_nordin_jour","ln_c_taylor_j","sur_conso_pct","ai_m3_jour",
    "q_m3_jour","conso_q_cout_complet_m3_trim","Bi","ln_qb","qb_m3_jour",
    "qb_m3_trim","i1","i2","t1","t2","t1_t2_eur_jour","i1_1","i2_1",
    "t1_1","t2_1","t1_t2_eur_trim","diff_qb_tbse_pct","ln_qb_redev",
    "qb_m3_jour_1","qb_redev_sans_tva","i1_2","i2_2","t1_2","t2_2",
    "t1_t2_eur_jour_1","i1_3","i2_3","t1_3","t2_3","t1_t2_eur_trim_1",
    "diff_qb_redev_tbse_pct","ln_qb_ttc","qb_m3_jour_2","qb_ttc","i1_4",
    "i2_4","t1_4","t2_4","t1_t2_eur_jour_2","i1_5","i2_5","t1_5","t2_5",
    "t1_t2_eur_trim_2","diff_qb_ttc_tbse_pct","abonnement_ht",
    "abonnement_ht_jour","prix_ht_t1","prix_ht_t2","prix_ht_t3","prix_ht_t4",
    "terme_prix_1","terme_ln_ai_1","pv_1_somme","terme_prix_2",
    "terme_ln_ai_2","pv_2_somme","terme_prix_3","terme_ln_ai_3","pv_3_somme",
    "terme_prix_4","terme_ln_ai_4","pv_4_somme","m3_jour_1","m3_trim_1",
    "m3_jour_2","m3_trim_2","m3_jour_3","m3_trim_3","m3_jour_4","m3_trim_4",
    "si_1","sc_1","si_2","sc_2","si_3","sc_3","si_4","conso_hrt_m3_trim",
    "conso_hrt_m3_trim_val","sur_conso_1","conso_mauvaise_percep_m3_trim",
    "diff_ibt_ht_pct","conso_hrt_m3j_pp","conso_hrt_m3j_mp",
    "var_conso_hrt_optq","var_conso_hrt_mp_optq","dummy_1_a_conso_moins",
    "dummy_1_b_conso_plus","dummy_1_c_conso_eq","dummy_1_d_conso_moins",
    "dummy_1_e_conso_plus","dummy_1_f_conso_eq","sur_conso_2","surconso",

    # éléments de la première liste qui n’étaient pas déjà dans la seconde
    "i1_6","i2_6","t1_6","t2_6","t1_t2_eur_jour_3","i1_7","i2_7","t1_7","t2_7",
    "t1_t2_eur_trim_3","i1_8","i2_8","t1_8","t2_8","t1_t2_eur_jour_4","i1_9",
    "i2_9","t1_9","t2_9","t1_t2_eur_trim_4","abonnement_redev","abonnement_redev_jour",
    "prix_redev_t1","prix_redev_t2","prix_redev_t3","prix_redev_t4","terme_prix_1_1",
    "terme_ln_ai_1_1","pv_1_somme_1","terme_prix_2_1","terme_ln_ai_2_1",
    "pv_2_somme_1","terme_prix_3_1","terme_ln_ai_3_1","pv_3_somme_1",
    "terme_prix_4_1","terme_ln_ai_4_1","pv_4_somme_1","m3_jour_1_1","m3_trim_1_1",
    "m3_jour_2_1","m3_trim_2_1","m3_jour_3_1","m3_trim_3_1","m3_jour_4_1",
    "m3_trim_4_1","si_1_1","sc_1_1","si_2_1","sc_2_1","si_3_1","sc_3_1","si_4_1",
    "conso_sans_tva","conso_sans_tva_val","conso_mauvaise_percep","diff_ibt_redev_pct",
    "conso_redev_m3j_pp","conso_redev_m3j_mp","var_conso_redev_optq",
    "var_conso_redev_mp_optq","dummy_1_a_conso_moins_1","dummy_1_b_conso_plus_1",
    "dummy_1_c_conso_eq_1","dummy_1_d_conso_moins_1","dummy_1_e_conso_plus_1",
    "dummy_1_f_conso_eq_1","i1_10","i2_10","t1_10","t2_10","t1_t2_eur_jour_5",
    "i1_11","i2_11","t1_11","t2_11","t1_t2_eur_trim_5","i1_12","i2_12","t1_12",
    "t2_12","t1_t2_eur_jour_6","i1_13","i2_13","t1_13","t2_13","t1_t2_eur_trim_6",
    "abonnement_ttc","abonnement_ttc_jour","prix_ttc_t1","prix_ttc_t2",
    "prix_ttc_t3","prix_ttc_t4","prix_1","ln_ai_1","pv_1","prix_2","ln_ai_2",
    "pv_2","prix_3","ln_ai_3","pv_3","prix_4","ln_ai_4","pv_4","m3_jour_1_2",
    "m3_trim_1_2","m3_jour_2_2","m3_trim_2_2","m3_jour_3_2","m3_trim_3_2",
    "m3_jour_4_2","m3_trim_4_2","si_1_2","sc_1_2","si_2_2","sc_2_2","si_3_2",
    "sc_3_2","si_4_2","conso_tva","conso_tva_val","variation_conso_hrt_q_star",
    "variation_conso_hrt_mp_q_star","variation_conso_ttc_mp_optimum_q_star",
    "variation_conso_ttc_optimum_q_star","effet_redevance","effet_tva",
    "dummy_1_a_menage_inf_optimum","dummy_1_b_menage_sup_optimum",
    "dummy_1_c_conso_egale_optimum","effet_redevance_1","effet_tva_1",
    "dummy_1_d_menage_inf_optimum","dummy_1_e_menage_sup_optimum",
    "dummy_1_f_conso_egale_optimum","i1_14","i2_14","t1_14","t2_14",
    "t1_t2_euro_jour","i1_15","i2_15","t1_15","t2_15","t1_t2_euro_trim",
    "i1_16","i2_16","t1_16","t2_16","t1_t2_euro_jour_1","i1_17","i2_17",
    "t1_17","t2_17","t1_t2_euro_trim_1"
    ]
        return combined_columns
        
    def compute_daily_and_logs(self):
        """
        Calcule les colonnes suivantes :
        - c_captive_jour = c_m3_trim / 90
        - c_nordin_jour = consom_nordin_trim / 90
        - c_taylor_jour = consom_taylor_trim / 90
        - ln_c_captive_jour = ln(c_m3_trim)
        - ln_c_nordin_jour = ln(c_nordin_jour)
        - ln_c_taylor_j = ln(c_taylor_jour)
        - sur_conso_pct = 100 * (ln_c_taylor_j - ln_c_nordin_jour)
        """
        # Vérifier que les colonnes sources existent
        required_cols = ["c_m3_trim", "consom_nordin_trim", "consom_taylor_trim"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame.")

        # Calcul des colonnes journalières
        self.df["c_captive_jour"] = self.df["c_m3_trim"] / 90
        self.df["c_nordin_jour"] = self.df["consom_nordin_trim"] / 90
        self.df["c_taylor_jour"] = self.df["consom_taylor_trim"] / 90

        # Calcul des logarithmes
        self.df["ln_c_captive_jour"] = np.log(self.df["c_m3_trim"].replace(0, np.nan))
        self.df["ln_c_nordin_jour"] = np.log(self.df["c_nordin_jour"].replace(0, np.nan))
        self.df["ln_c_taylor_j"] = np.log(self.df["c_taylor_jour"].replace(0, np.nan))

        # Calcul de sur_conso_pct
        self.df["sur_conso_pct"] = 100 * (self.df["ln_c_taylor_j"] - self.df["ln_c_nordin_jour"])

        print("✅ Colonnes journalières et logarithmes calculés avec succès.")
        return self.df
    
    def compute_ai_and_q(self):
        """
        Calcule les colonnes suivantes :
        - ai_m3_jour = (c_m3_trim / 90) * ((revenu_net_mois / 30) ^ elasticite_revenu_virtuel)
        - q_m3_jour = ai_m3_jour / (Prix_pi ^ abs(elasticite_prix_marginal))
        - conso_q_cout_complet_m3_trim = q_m3_jour * 90
        """
        # Vérification des colonnes nécessaires
        required_cols = ["c_m3_trim", "revenu_net_mois"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame.")

        # Calcul ai_m3_jour
        self.df["ai_m3_jour"] = (self.df["c_m3_trim"] / 90) * (
            (self.df["revenu_net_mois"] / 30) ** self.elasticite_revenu_virtuel
        )

        # Calcul q_m3_jour
        self.df["q_m3_jour"] = self.df["ai_m3_jour"] / (self.Prix_pi ** abs(self.elasticite_prix_marginal))

        # Calcul conso_q_cout_complet_m3_trim
        self.df["conso_q_cout_complet_m3_trim"] = self.df["q_m3_jour"] * 90

        print("✅ Colonnes ai_m3_jour, q_m3_jour et conso_q_cout_complet_m3_trim calculées avec succès.")
        return self.df
    
    def compute_Bi(self):
        """
        Calcule la colonne Bi selon la formule :
        Bi = ai_m3_jour ^ (1 / abs(elasticite_prix_marginal))
        """
        # Vérification que ai_m3_jour existe
        if "ai_m3_jour" not in self.df.columns:
            raise ValueError("La colonne 'ai_m3_jour' est manquante. Exécutez d'abord compute_ai_and_q().")

        # Calcul de Bi
        self.df["Bi"] = self.df["ai_m3_jour"] ** (1 / abs(self.elasticite_prix_marginal))

        print("✅ Colonne Bi calculée avec succès.")
        return self.df
    
    def compute_qb_and_costs(self):
        """
        Calcule les colonnes suivantes :
        - ln_qb = ln(c_m3_trim/90) + (elasticite_revenu_virtuel * ln(revenu_net_mois/30)) - (abs(elasticite_prix_marginal) * ln(Prix_pi))
        - qb_m3_jour = exp(ln_qb)
        - qb_m3_trim = qb_m3_jour * 90
        - i1 = (abs(elasticite_prix_marginal) * Bi) / (1 - abs(elasticite_prix_marginal)) * ((q_m3_jour ^ -((1 - abs(elasticite_prix_marginal)) / abs(elasticite_prix_marginal))) - (qb_m3_jour ^ -((1 - abs(elasticite_prix_marginal)) / abs(elasticite_prix_marginal))))
        - i2 = cout_marginal_complet_cme * (qb_m3_jour - q_m3_jour)
        - t1 = i1
        - t2 = -i2
        - t1_t2_eur_jour = t1 + t2
        """
        # Vérification des colonnes nécessaires
        required_cols = ["c_m3_trim", "revenu_net_mois", "q_m3_jour", "Bi"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame. Exécutez les méthodes précédentes si nécessaire.")

        # ln_qb
        self.df["ln_qb"] = np.log(self.df["c_m3_trim"].replace(0, np.nan)/90) + \
                           self.elasticite_revenu_virtuel * np.log((self.df["revenu_net_mois"].replace(0, np.nan)/30)) - \
                           abs(self.elasticite_prix_marginal) * np.log(self.Prix_pi)

        # qb_m3_jour et qb_m3_trim
        self.df["qb_m3_jour"] = np.exp(self.df["ln_qb"])
        self.df["qb_m3_trim"] = self.df["qb_m3_jour"] * 90

        # i1
        alpha = abs(self.elasticite_prix_marginal)
        beta = (1 - alpha) / alpha
        self.df["i1"] = (alpha * self.df["Bi"] / (1 - alpha)) * (
            self.df["q_m3_jour"] ** -beta - self.df["qb_m3_jour"] ** -beta
        )

        # i2
        self.df["i2"] = self.cout_marginal_complet_cme * (self.df["qb_m3_jour"] - self.df["q_m3_jour"])

        # t1, t2 et t1_t2_eur_jour
        self.df["t1"] = self.df["i1"]
        self.df["t2"] = -self.df["i2"]
        self.df["t1_t2_eur_jour"] = self.df["t1"] + self.df["t2"]

        print("✅ Colonnes ln_qb, qb_m3_jour, qb_m3_trim, i1, i2, t1, t2 et t1_t2_eur_jour calculées avec succès.")
        return self.df
    
    def compute_trim_values(self):
        """
        Calcule les colonnes suivantes :
        - i1_1 = i1 * 90
        - i2_1 = i2 * 90
        - t1_1 = i1_1
        - t2_1 = -i2_1
        - t1_t2_eur_trim = t1_1 + t2_1
        - diff_qb_tbse_pct = ((qb_m3_trim - c_tbse) / c_tbse) * 100
        """
        required_cols = ["i1", "i2", "qb_m3_trim", "c_tbse"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame. Assurez-vous d'exécuter les méthodes précédentes.")

        # Calcul des valeurs trimestrielles
        self.df["i1_1"] = self.df["i1"] * 90
        self.df["i2_1"] = self.df["i2"] * 90
        self.df["t1_1"] = self.df["i1_1"]
        self.df["t2_1"] = -self.df["i2_1"]
        self.df["t1_t2_eur_trim"] = self.df["t1_1"] + self.df["t2_1"]

        # Calcul de la différence en pourcentage par rapport à TBSE
        self.df["diff_qb_tbse_pct"] = ((self.df["qb_m3_trim"] - self.df["c_tbse"]) / self.df["c_tbse"]) * 100

        print("✅ Colonnes i1_1, i2_1, t1_1, t2_1, t1_t2_eur_trim et diff_qb_tbse_pct calculées avec succès.")
        return self.df
    
    def compute_redevance_values(self):
        """
        Calcule les colonnes liées à la redevance :
        - ln_qb_redev = ln(c_m3_trim/90) + (elasticite_revenu_virtuel*ln(revenu_net_mois/30)) - (abs(elasticite_prix_marginal) * ln(Prix_pi + redevances_accise_euro_m3))
        - qb_m3_jour_1 = exp(ln_qb_redev)
        - qb_redev_sans_tva = qb_m3_jour_1 * 90
        - i1_2 = (abs(elasticite_prix_marginal)*Bi)/(1-abs(elasticite_prix_marginal)) * ((q_m3_jour^-((1-abs(elasticite_prix_marginal))/abs(elasticite_prix_marginal))) - (qb_m3_jour_1^-((1-abs(elasticite_prix_marginal))/abs(elasticite_prix_marginal))))
        - i2_2 = cout_marginal_complet_cme * (qb_m3_jour_1 - q_m3_jour)
        - t1_2 = i1_2
        - t2_2 = -i2_2
        - t1_t2_eur_jour_1 = t1_2 + t2_2
        """
        required_cols = ["c_m3_trim", "revenu_net_mois", "q_m3_jour", "Bi"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame. Exécutez les méthodes précédentes si nécessaire.")

        # ln_qb_redev
        self.df["ln_qb_redev"] = np.log(self.df["c_m3_trim"].replace(0, np.nan)/90) + \
                                 self.elasticite_revenu_virtuel * np.log((self.df["revenu_net_mois"].replace(0, np.nan)/30)) - \
                                 abs(self.elasticite_prix_marginal) * np.log(self.Prix_pi + self.redevances_accise_euro_m3)

        # qb_m3_jour_1 et qb_redev_sans_tva
        self.df["qb_m3_jour_1"] = np.exp(self.df["ln_qb_redev"])
        self.df["qb_redev_sans_tva"] = self.df["qb_m3_jour_1"] * 90

        # i1_2
        alpha = abs(self.elasticite_prix_marginal)
        beta = (1 - alpha) / alpha
        self.df["i1_2"] = (alpha * self.df["Bi"] / (1 - alpha)) * (
            self.df["q_m3_jour"] ** -beta - self.df["qb_m3_jour_1"] ** -beta
        )

        # i2_2
        self.df["i2_2"] = self.cout_marginal_complet_cme * (self.df["qb_m3_jour_1"] - self.df["q_m3_jour"])

        # t1_2, t2_2 et t1_t2_eur_jour_1
        self.df["t1_2"] = self.df["i1_2"]
        self.df["t2_2"] = -self.df["i2_2"]
        self.df["t1_t2_eur_jour_1"] = self.df["t1_2"] + self.df["t2_2"]

        print("✅ Colonnes ln_qb_redev, qb_m3_jour_1, qb_redev_sans_tva, i1_2, i2_2, t1_2, t2_2 et t1_t2_eur_jour_1 calculées avec succès.")
        return self.df
    

    def compute_redevance_trim(self):
        """
            Calcule les colonnes liées à la redevance pour le trimestre :
            - i1_3 = i1_2 * 90
            - i2_3 = i2_2 * 90
            - t1_3 = i1_3
            - t2_3 = -i2_3
            - t1_t2_eur_trim_1 = t1_3 + t2_3
            - diff_qb_redev_tbse_pct = ((qb_redev_sans_tva - c_tbse)/c_tbse) * 100
            """

        required_cols = ["i1_2", "i2_2", "qb_redev_sans_tva", "c_tbse"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame. Exécutez les méthodes précédentes si nécessaire.")

        self.df["i1_3"] = self.df["i1_2"] * 90
        self.df["i2_3"] = self.df["i2_2"] * 90
        self.df["t1_3"] = self.df["i1_3"]
        self.df["t2_3"] = -self.df["i2_3"]
        self.df["t1_t2_eur_trim_1"] = self.df["t1_3"] + self.df["t2_3"]
        self.df["diff_qb_redev_tbse_pct"] = ((self.df["qb_redev_sans_tva"] - self.df["c_tbse"]) / self.df["c_tbse"]) * 100

        print("✅ Colonnes i1_3, i2_3, t1_3, t2_3, t1_t2_eur_trim_1 et diff_qb_redev_tbse_pct calculées.")
        return self.df
    
    def compute_ttc_values(self):
        """
        Calcule les colonnes liées au scénario TTC :
        - ln_qb_ttc
        - qb_m3_jour_2
        - qb_ttc
        - i1_4
        - i2_4
        - t1_4
        - t2_4
        - t1_t2_eur_jour_2
        """

        import numpy as np

        required_cols = ["c_m3_trim", "revenu_net_mois", "q_m3_jour", "Bi"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans le DataFrame. Exécutez les méthodes précédentes si nécessaire.")

        # ln_qb_ttc
        self.df["ln_qb_ttc"] = (
            np.log(self.df["c_m3_trim"] / 90) +
            self.elasticite_revenu_virtuel * np.log(self.df["revenu_net_mois"] / 30) -
            abs(self.elasticite_prix_marginal) * np.log((self.Prix_pi + self.redevances_accise_euro_m3) * (1 + self.taux_tva_ep / 100))
        )

        # qb_m3_jour_2 et qb_ttc
        self.df["qb_m3_jour_2"] = np.exp(self.df["ln_qb_ttc"])
        self.df["qb_ttc"] = self.df["qb_m3_jour_2"] * 90

        # i1_4 et i2_4
        alpha = abs(self.elasticite_prix_marginal)
        beta = (1 - alpha) / alpha
        self.df["i1_4"] = (alpha * self.df["Bi"] / (1 - alpha)) * ((self.df["q_m3_jour"] ** -beta) - (self.df["qb_m3_jour_2"] ** -beta))
        self.df["i2_4"] = self.cout_marginal_complet_cme * (self.df["qb_m3_jour_2"] - self.df["q_m3_jour"])

        # t1_4, t2_4 et t1_t2_eur_jour_2
        self.df["t1_4"] = self.df["i1_4"]
        self.df["t2_4"] = -self.df["i2_4"]
        self.df["t1_t2_eur_jour_2"] = self.df["t1_4"] + self.df["t2_4"]

        print("✅ Colonnes ln_qb_ttc, qb_m3_jour_2, qb_ttc, i1_4, i2_4, t1_4, t2_4, t1_t2_eur_jour_2 calculées.")
        return self.df
    
    def compute_ttc_trim(self):
        """
        Met à jour les colonnes trimestrielles basées sur les valeurs TTC :
        i1_5, i2_5, t1_5, t2_5, t1_t2_eur_trim_2 et diff_qb_ttc_tbse_pct.
        Retourne le DataFrame mis à jour.
        """
        # i1_5 = i1_4 * 90
        self.df["i1_5"] = self.df["i1_4"] * 90

        # i2_5 = i2_4 * 90
        self.df["i2_5"] = self.df["i2_4"] * 90

        # t1_5 = i1_5
        self.df["t1_5"] = self.df["i1_5"]

        # t2_5 = -i2_5
        self.df["t2_5"] = -self.df["i2_5"]

        # t1_t2_eur_trim_2 = t1_5 + t2_5
        self.df["t1_t2_eur_trim_2"] = self.df["t1_5"] + self.df["t2_5"]

        # diff_qb_ttc_tbse_pct = ((qb_ttc - c_tbse) / c_tbse) * 100
        self.df["diff_qb_ttc_tbse_pct"] = ((self.df["qb_ttc"] - self.df["c_tbse"]) / self.df["c_tbse"]) * 100

        print("✅ Colonnes TTC trimestrielles calculées : i1_5, i2_5, t1_5, t2_5, t1_t2_eur_trim_2, diff_qb_ttc_tbse_pct")
        return self.df
    
    def compute_abonnement_ht(self):
        """
        Met à jour les colonnes liées à l'abonnement HT :
        - abonnement_ht
        - abonnement_ht_jour
        Retourne le DataFrame mis à jour.
        """
        # abonnement_ht = prix_ht_op_a_EP_ab
        self.df["abonnement_ht"] = self.prix_ht_op_a_EP_ab

        # abonnement_ht_jour = abonnement_ht / 90
        self.df["abonnement_ht_jour"] = self.df["abonnement_ht"] / 90

        print("✅ Colonnes d'abonnement HT mises à jour : abonnement_ht, abonnement_ht_jour")
        return self.df
    
    def compute_prix_ht_and_terme(self):
        """
        Met à jour les colonnes suivantes :
        - prix_ht_t1, prix_ht_t2, prix_ht_t3, prix_ht_t4
        - terme_prix_1 = elasticite_prix_marginal * LN(prix_ht_t1)
        
        Retourne le DataFrame mis à jour.
        """
        import numpy as np

        # Prix HT pour chaque tranche
        self.df["prix_ht_t1"] = self.prix_ht_op_T_EP_K0
        self.df["prix_ht_t2"] = self.prix_ht_op_T_EP_K1
        self.df["prix_ht_t3"] = self.prix_ht_op_T_EP_K2
        self.df["prix_ht_t4"] = self.prix_ht_op_T_EP_K3

        # Terme prix 1
        self.df["terme_prix_1"] = self.elasticite_prix_marginal * np.log(self.df["prix_ht_t1"])

        print("✅ Colonnes mises à jour : prix_ht_t1 à prix_ht_t4, terme_prix_1")
        return self.df
    
    def compute_termes_and_pv(self):
        """
        Met à jour les colonnes suivantes :
        - terme_prix_1 à terme_prix_4
        - terme_ln_ai_1 à terme_ln_ai_4
        - pv_1_somme à pv_4_somme
        
        Retourne le DataFrame mis à jour.
        """
        import numpy as np

        # Termes prix
        self.df["terme_prix_1"] = self.elasticite_prix_marginal * np.log(self.df["prix_ht_t1"])
        self.df["terme_prix_2"] = self.elasticite_prix_marginal * np.log(self.df["prix_ht_t2"])
        self.df["terme_prix_3"] = self.elasticite_prix_marginal * np.log(self.df["prix_ht_t3"])
        self.df["terme_prix_4"] = self.elasticite_prix_marginal * np.log(self.df["prix_ht_t4"])

        # Termes ln(ai_m3_jour)
        self.df["terme_ln_ai_1"] = np.log(self.df["ai_m3_jour"])
        self.df["terme_ln_ai_2"] = np.log(self.df["ai_m3_jour"])
        self.df["terme_ln_ai_3"] = np.log(self.df["ai_m3_jour"])
        self.df["terme_ln_ai_4"] = np.log(self.df["ai_m3_jour"])

        # Somme des termes
        self.df["pv_1_somme"] = self.df["terme_prix_1"] + self.df["terme_ln_ai_1"]
        self.df["pv_2_somme"] = self.df["terme_prix_2"] + self.df["terme_ln_ai_2"]
        self.df["pv_3_somme"] = self.df["terme_prix_3"] + self.df["terme_ln_ai_3"]
        self.df["pv_4_somme"] = self.df["terme_prix_4"] + self.df["terme_ln_ai_4"]

        print("✅ Colonnes mises à jour : terme_prix_1 à terme_prix_4, terme_ln_ai_1 à terme_ln_ai_4, pv_1_somme à pv_4_somme")
        return self.df
    
    def compute_m3_jour_trim(self):
        """
        Met à jour les colonnes m3_jour_1 à m3_trim_4 selon :
        m3_jour_i = EXP(pv_i_somme)
        m3_trim_i = m3_jour_i * 90
        
        Retourne le DataFrame mis à jour.
        """
        import numpy as np

        # Calcul des m3_jour et m3_trim
        for i in range(1, 5):
            self.df[f"m3_jour_{i}"] = np.exp(self.df[f"pv_{i}_somme"])
            self.df[f"m3_trim_{i}"] = self.df[f"m3_jour_{i}"] * 90

        print("✅ Colonnes mises à jour : m3_jour_1 à m3_trim_4")
        return self.df
    

    def compute_si_sc_conso(self):
        """
        Met à jour les colonnes si_1 à diff_ibt_ht_pct selon les règles fournies.
        Retourne le DataFrame mis à jour.
        """
        import numpy as np

        df = self.df

        # SI et SC
        df["si_1"] = np.where(df["m3_trim_1"] < self.seuil_T_EP_K1_bis, 1, 0)
        df["sc_1"] = np.where(
            (df["m3_trim_2"] < self.seuil_T_EP_K1_bis) & (df["m3_trim_1"] > self.seuil_T_EP_K1_bis),
            1,
            0
        ) * (1 - df["si_1"])

        df["si_2"] = np.where(
            (df["m3_trim_2"] > self.seuil_T_EP_K1_bis) & (df["m3_trim_2"] < self.seuil_T_EP_K2_bis),
            1,
            0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"])

        df["sc_2"] = np.where(
            (df["m3_trim_2"] > self.seuil_T_EP_K2_bis) & (df["m3_trim_3"] < self.seuil_T_EP_K2_bis),
            1,
            0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"])

        df["si_3"] = np.where(
            (df["m3_trim_3"] > self.seuil_T_EP_K2_bis) & (df["m3_trim_3"] < self.seuil_T_EP_K3_bis),
            1,
            0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"])

        df["sc_3"] = np.where(
            (df["m3_trim_3"] > self.seuil_T_EP_K3_bis) & (df["m3_trim_4"] < self.seuil_T_EP_K3_bis),
            1,
            0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"]) * (1 - df["si_3"]) * (1 - df["sc_2"])

        df["si_4"] = np.where(
            df["m3_trim_4"] > self.seuil_T_EP_K3_bis,
            1,
            0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"]) * (1 - df["si_3"]) * (1 - df["sc_3"])

        # Consommation HRT
        df["conso_hrt_m3_trim"] = 0
        df["conso_hrt_m3_trim_val"] = (
            df["si_1"] * df["m3_trim_1"] +
            df["sc_1"] * self.seuil_T_EP_K1_bis +
            df["si_2"] * df["m3_trim_2"] +
            df["sc_2"] * self.seuil_T_EP_K2_bis +
            df["si_3"] * df["m3_trim_3"] +
            df["sc_3"] * self.seuil_T_EP_K3_bis +
            df["si_4"] * df["m3_trim_4"]
        )

        df["conso_mauvaise_percep_m3_trim"] = df["conso_hrt_m3_trim_val"] + df["sur_conso_1"]
        df["diff_ibt_ht_pct"] = ((df["conso_mauvaise_percep_m3_trim"] - df["c_ibt_pp"]) / df["c_ibt_pp"]) * 100

        print("✅ Colonnes mises à jour : si_1 à diff_ibt_ht_pct")
        return df
    

    def compute_conso_hrt_pp_mp(self):
        """
        Met à jour les colonnes conso_hrt_m3j_pp et conso_hrt_m3j_mp
        à partir de conso_hrt_m3_trim_val et conso_mauvaise_percep_m3_trim.
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        df["conso_hrt_m3j_pp"] = df["conso_hrt_m3_trim_val"] / 90
        df["conso_hrt_m3j_mp"] = df["conso_mauvaise_percep_m3_trim"] / 90

        print("✅ Colonnes mises à jour : conso_hrt_m3j_pp et conso_hrt_m3j_mp")
        return df
    

    def compute_var_conso_and_dummies(self):
        """
        Met à jour les colonnes de variations de consommation et les dummies correspondants.
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        # Variations de consommation
        df["var_conso_hrt_optq"] = df["conso_hrt_m3_trim_val"] - df["conso_q_cout_complet_m3_trim"]
        df["var_conso_hrt_mp_optq"] = df["conso_mauvaise_percep_m3_trim"] - df["conso_q_cout_complet_m3_trim"]

        # Dummies pour var_conso_hrt_optq
        df["dummy_1_a_conso_moins"] = (df["var_conso_hrt_optq"] < 0).astype(int)
        df["dummy_1_b_conso_plus"] = (df["var_conso_hrt_optq"] > 0).astype(int)
        df["dummy_1_c_conso_eq"] = (df["var_conso_hrt_optq"] == 0).astype(int)

        # Dummies pour var_conso_hrt_mp_optq
        df["dummy_1_d_conso_moins"] = (df["var_conso_hrt_mp_optq"] < 0).astype(int)
        df["dummy_1_e_conso_plus"] = (df["var_conso_hrt_mp_optq"] > 0).astype(int)
        df["dummy_1_f_conso_eq"] = (df["var_conso_hrt_mp_optq"] == 0).astype(int)

        print("✅ Colonnes mises à jour : var_conso_hrt_optq, var_conso_hrt_mp_optq et dummies")
        return df

    def compute_i1_i2_t1_t2_6(self):
        """
        Met à jour les colonnes i1_6, i2_6, t1_6, t2_6 et t1_t2_eur_jour_3
        selon les formules définies.
        Retourne le DataFrame mis à jour.
        """
        df = self.df
        abs_ep = abs(self.elasticite_prix_marginal)

        # Calcul i1_6
        df["i1_6"] = (abs_ep * df["Bi"]) / (1 - abs_ep) * (
            df["q_m3_jour"] ** (-((1 - abs_ep) / abs_ep)) -
            df["conso_hrt_m3j_pp"] ** (-((1 - abs_ep) / abs_ep))
        )

        # Calcul i2_6
        df["i2_6"] = self.cout_marginal_complet_cme * (df["conso_hrt_m3j_pp"] - df["q_m3_jour"])

        # Calcul t1_6 et t2_6
        df["t1_6"] = df["i1_6"]
        df["t2_6"] = -df["i2_6"]

        # Somme t1_t2_eur_jour_3
        df["t1_t2_eur_jour_3"] = df["t1_6"] + df["t2_6"]

        print("✅ Colonnes mises à jour : i1_6, i2_6, t1_6, t2_6, t1_t2_eur_jour_3")
        return df
    
    def compute_i1_i2_t1_t2_7(self):
        """
        Met à jour les colonnes i1_7, i2_7, t1_7, t2_7 et t1_t2_eur_trim_3
        selon les formules définies.
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        # Calcul i1_7 et i2_7
        df["i1_7"] = df["i1_6"] * 90
        df["i2_7"] = df["i2_6"] * 90

        # Calcul t1_7 et t2_7
        df["t1_7"] = df["i1_7"]
        df["t2_7"] = -df["i2_7"]

        # Somme t1_t2_eur_trim_3
        df["t1_t2_eur_trim_3"] = df["t1_7"] + df["t2_7"]

        print("✅ Colonnes mises à jour : i1_7, i2_7, t1_7, t2_7, t1_t2_eur_trim_3")
        return df


    def compute_i1_i2_t1_t2_8(self):
        """
        Met à jour les colonnes i1_8, i2_8, t1_8, t2_8 et t1_t2_eur_jour_4
        selon les formules définies.
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        # Calcul i1_8 et i2_8
        df["i1_8"] = (abs(self.elasticite_prix_marginal) * df["Bi"]) / (1 - abs(self.elasticite_prix_marginal)) * (
            (df["q_m3_jour"] ** (-((1 - abs(self.elasticite_prix_marginal)) / abs(self.elasticite_prix_marginal)))) -
            (df["conso_hrt_m3j_mp"] ** (-((1 - abs(self.elasticite_prix_marginal)) / abs(self.elasticite_prix_marginal))))
        )
        df["i2_8"] = self.cout_marginal_complet_cme * (df["conso_hrt_m3j_mp"] - df["q_m3_jour"])

        # Calcul t1_8 et t2_8
        df["t1_8"] = df["i1_8"]
        df["t2_8"] = -df["i2_8"]

        # Somme t1_t2_eur_jour_4
        df["t1_t2_eur_jour_4"] = df["t1_8"] + df["t2_8"]

        print("✅ Colonnes mises à jour : i1_8, i2_8, t1_8, t2_8, t1_t2_eur_jour_4")
        return df
    

    def compute_i1_i2_t1_t2_9(self):
        """
        Met à jour les colonnes i1_9, i2_9, t1_9, t2_9 et t1_t2_eur_trim_4
        selon les formules définies.
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        # Calcul i1_9 et i2_9
        df["i1_9"] = df["i1_8"] * 90
        df["i2_9"] = df["i2_8"] * 90

        # Calcul t1_9 et t2_9
        df["t1_9"] = df["i1_9"]
        df["t2_9"] = -df["i2_9"]

        # Somme t1_t2_eur_trim_4
        df["t1_t2_eur_trim_4"] = df["t1_9"] + df["t2_9"]

        print("✅ Colonnes mises à jour : i1_9, i2_9, t1_9, t2_9, t1_t2_eur_trim_4")
        return df
    
    def compute_abonnement_redev(self):
        """
        Met à jour les colonnes abonnement_redev et abonnement_redev_jour.
        abonnement_redev = prix_htva_t_EP_T1
        abonnement_redev_jour = abonnement_redev / 90
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        # Mise à jour des colonnes
        df["abonnement_redev"] = self.prix_htva_t_EP_T1
        df["abonnement_redev_jour"] = df["abonnement_redev"] / 90

        print("✅ Colonnes mises à jour : abonnement_redev, abonnement_redev_jour")
        return df
    
    def compute_prix_redev(self):
        """
        Met à jour les colonnes de prix de redevance :
        prix_redev_t1 = prix_htva_t_EP_T1
        prix_redev_t2 = prix_htva_t_EP_T2
        prix_redev_t3 = prix_htva_t_EP_T3
        prix_redev_t4 = prix_htva_t_EP_T4
        Retourne le DataFrame mis à jour.
        """
        df = self.df

        df["prix_redev_t1"] = self.prix_htva_t_EP_T1
        df["prix_redev_t2"] = self.prix_htva_t_EP_T2
        df["prix_redev_t3"] = self.prix_htva_t_EP_T3
        df["prix_redev_t4"] = self.prix_htva_t_EP_T4

        print("✅ Colonnes mises à jour : prix_redev_t1 à prix_redev_t4")
        return df
    
    def compute_pv_redev(self):
        """
        Met à jour les colonnes de calcul pour les redevances :
        - terme_prix_1_1 à terme_prix_4_1 : elasticite_prix_marginal * LN(prix_redev_tX)
        - terme_ln_ai_1_1 à terme_ln_ai_4_1 : LN(ai_m3_jour)
        - pv_1_somme_1 à pv_4_somme_1 : somme des termes correspondants
        Retourne le DataFrame mis à jour.
        """
        import numpy as np

        df = self.df

        for i in range(1, 5):
            df[f"terme_prix_{i}_1"] = self.elasticite_prix_marginal * np.log(df[f"prix_redev_t{i}"])
            df[f"terme_ln_ai_{i}_1"] = np.log(df["ai_m3_jour"])
            df[f"pv_{i}_somme_1"] = df[f"terme_prix_{i}_1"] + df[f"terme_ln_ai_{i}_1"]

        print("✅ Colonnes mises à jour : terme_prix_1_1 → pv_4_somme_1")
        return df
    
    def compute_m3_trim_redev(self):
        """
        Met à jour les colonnes m3_jour_1_1 → m3_trim_4_1 à partir de pv_1_somme_1 → pv_4_somme_1.
        Calcul :
            m3_jour_X_1 = EXP(pv_X_somme_1)
            m3_trim_X_1 = m3_jour_X_1 * 90
        Retourne le DataFrame mis à jour.
        """
        import numpy as np
        df = self.df

        for i in range(1, 5):
            df[f"m3_jour_{i}_1"] = np.exp(df[f"pv_{i}_somme_1"])
            df[f"m3_trim_{i}_1"] = df[f"m3_jour_{i}_1"] * 90

        print("✅ Colonnes mises à jour : m3_jour_1_1 → m3_trim_4_1")
        return df
    

    def compute_conso_redev_indicateurs(self):
        """
        Met à jour les colonnes logiques et de consommation redevance :
        si_1_1, sc_1_1, si_2_1, sc_2_1, si_3_1, sc_3_1, si_4_1,
        conso_sans_tva, conso_sans_tva_val, conso_mauvaise_percep, diff_ibt_redev_pct.
        """
        import numpy as np

        df = self.df

        # Raccourcis des seuils
        k1 = self.seuil_T_EP_K1_bis
        k2 = self.seuil_T_EP_K2_bis
        k3 = self.seuil_T_EP_K3_bis

        # Conditions SI / SC
        df["si_1_1"] = np.where(df["m3_trim_1_1"] < k1, 1, 0)

        df["sc_1_1"] = np.where(
            (df["m3_trim_2_1"] < k1) & (df["m3_trim_1_1"] > k1), 1, 0
        ) * (1 - df["si_1_1"])

        df["si_2_1"] = np.where(
            (df["m3_trim_2_1"] > k1) & (df["m3_trim_2_1"] < k2), 1, 0
        ) * (1 - df["si_1_1"]) * (1 - df["sc_1_1"])

        df["sc_2_1"] = np.where(
            (df["m3_trim_2_1"] > k2) & (df["m3_trim_3_1"] < k2), 1, 0
        ) * (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"])

        df["si_3_1"] = np.where(
            (df["m3_trim_3_1"] > k2) & (df["m3_trim_3_1"] < k3), 1, 0
        ) * (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"]) * (1 - df["sc_2_1"])

        df["sc_3_1"] = np.where(
            (df["m3_trim_3_1"] > k3) & (df["m3_trim_4_1"] < k3), 1, 0
        ) * (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"]) * (1 - df["sc_2_1"]) * (1 - df["si_3_1"])

        df["si_4_1"] = np.where(df["m3_trim_4_1"] > k3, 1, 0) * (
            (1 - df["si_1_1"])
            * (1 - df["sc_1_1"])
            * (1 - df["si_2_1"])
            * (1 - df["sc_2_1"])
            * (1 - df["si_3_1"])
            * (1 - df["sc_3_1"])
        )

        # conso_sans_tva (fixe à 0 dans ton modèle)
        df["conso_sans_tva"] = 0

        # conso_sans_tva_val
        df["conso_sans_tva_val"] = (
            df["si_1_1"] * df["m3_trim_1_1"]
            + df["sc_1_1"] * self.seuil_T_EP_K1
            + df["si_2_1"] * df["m3_trim_2_1"]
            + df["sc_2_1"] * self.seuil_T_EP_K2
            + df["si_3_1"] * df["m3_trim_3_1"]
            + df["sc_3_1"] * self.seuil_T_EP_K3
            + df["si_4_1"] * df["m3_trim_4_1"]
        )

        # conso_mauvaise_percep
        df["conso_mauvaise_percep"] = df["conso_sans_tva_val"] + df["sur_conso_2"]

        # diff_ibt_redev_pct
        df["diff_ibt_redev_pct"] = ((df["conso_mauvaise_percep"] - df["c_ibt"]) / df["c_ibt"]) * 100

        print("✅ Colonnes mises à jour : si_1_1, sc_1_1, si_2_1, sc_2_1, si_3_1, sc_3_1, si_4_1, conso_sans_tva_val, conso_mauvaise_percep, diff_ibt_redev_pct")
        return df
    

    def defragment_dataframe(self):
        """
        Défragmente le DataFrame pour améliorer les performances.
        À appeler après plusieurs opérations d'ajout de colonnes.
        """
        self.df = self.df.copy()
        print("✅ DataFrame défragmenté")
        return self.df

   
    def compute_conso_redev_m3j(self):
        """
        Met à jour les colonnes :
        - conso_redev_m3j_pp = conso_sans_tva_val / 90
        - conso_redev_m3j_mp = conso_mauvaise_percep / 90
        """
        self.df["conso_redev_m3j_pp"] = self.df["conso_sans_tva_val"] / 90
        self.df["conso_redev_m3j_mp"] = self.df["conso_mauvaise_percep"] / 90
        return self.df

   

    def compute_var_conso_redev(self):
        """
        Met à jour les colonnes liées à la variation de consommation redevances :
        - var_conso_redev_optq = conso_sans_tva_val - conso_q_cout_complet_m3_trim
        - var_conso_redev_mp_optq = conso_mauvaise_percep - conso_q_cout_complet_m3_trim
        - dummy_1_a_conso_moins_1 = 1 si var_conso_redev_optq < 0 sinon 0
        - dummy_1_b_conso_plus_1  = 1 si var_conso_redev_optq > 0 sinon 0
        - dummy_1_c_conso_eq_1    = 1 si var_conso_redev_optq == 0 sinon 0
        - dummy_1_d_conso_moins_1 = 1 si var_conso_redev_mp_optq < 0 sinon 0
        - dummy_1_e_conso_plus_1  = 1 si var_conso_redev_mp_optq > 0 sinon 0
        - dummy_1_f_conso_eq_1    = 1 si var_conso_redev_mp_optq == 0 sinon 0
        """
        self.df["var_conso_redev_optq"] = (
            self.df["conso_sans_tva_val"] - self.df["conso_q_cout_complet_m3_trim"]
        )
        self.df["var_conso_redev_mp_optq"] = (
            self.df["conso_mauvaise_percep"] - self.df["conso_q_cout_complet_m3_trim"]
        )

        # Dummies pour var_conso_redev_optq
        self.df["dummy_1_a_conso_moins_1"] = (self.df["var_conso_redev_optq"] < 0).astype(int)
        self.df["dummy_1_b_conso_plus_1"] = (self.df["var_conso_redev_optq"] > 0).astype(int)
        self.df["dummy_1_c_conso_eq_1"] = (self.df["var_conso_redev_optq"] == 0).astype(int)

        # Dummies pour var_conso_redev_mp_optq
        self.df["dummy_1_d_conso_moins_1"] = (self.df["var_conso_redev_mp_optq"] < 0).astype(int)
        self.df["dummy_1_e_conso_plus_1"] = (self.df["var_conso_redev_mp_optq"] > 0).astype(int)
        self.df["dummy_1_f_conso_eq_1"] = (self.df["var_conso_redev_mp_optq"] == 0).astype(int)

        return self.df
    
    def compute_i1_i2_10(self):
        # Utilisation de l'élasticité stockée en attribut
        abs_eps = np.abs(self.elasticite_prix_marginal)
        expo = -(1 - abs_eps) / abs_eps

        # Calcul i1_10
        self.df["i1_10"] = (
            (abs_eps * self.df["Bi"]) / (1 - abs_eps)
            * (
                (self.df["q_m3_jour"] ** expo)
                - (self.df["conso_redev_m3j_pp"] ** expo)
            )
        )

        # Calcul i2_10
        self.df["i2_10"] = self.cout_marginal_complet_cme * (
            self.df["conso_redev_m3j_pp"] - self.df["q_m3_jour"]
        )

        # Dépendances
        self.df["t1_10"] = self.df["i1_10"]
        self.df["t2_10"] = -self.df["i2_10"]
        self.df["t1_t2_eur_jour_5"] = self.df["t1_10"] + self.df["t2_10"]

        return self.df


    def compute_i1_i2_11(self):
        # Passage du jour au trimestre (x90)
        self.df["i1_11"] = self.df["i1_10"] * 90
        self.df["i2_11"] = self.df["i2_10"] * 90

        # Dépendances
        self.df["t1_11"] = self.df["i1_11"]
        self.df["t2_11"] = -self.df["i2_11"]

        # Somme
        self.df["t1_t2_eur_trim_5"] = self.df["t1_11"] + self.df["t2_11"]

        return self.df
    

    #i1_12, i2_12, t1_12, t2_12, t1_t2_eur_jour_6
    def compute_i1_i2_12(self):
        """
        Calcule et met à jour :
        - i1_12, i2_12, t1_12, t2_12, t1_t2_eur_jour_6
        en utilisant les colonnes du DataFrame (q_m3_jour, Bi, conso_redev_m3j_mp)
        et les paramètres self.elasticite_prix_marginal et self.cout_marginal_complet_cme.
        Retourne self.df.
        """
        import numpy as np

        # Vérifier colonnes nécessaires
        required = ["q_m3_jour", "Bi", "conso_redev_m3j_mp"]
        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise KeyError(f"Colonnes manquantes pour compute_i1_i2_12: {missing}")

        # Élasticité (scalaire stockée dans la classe)
        abs_eps = abs(self.elasticite_prix_marginal)
        if abs_eps == 0:
            raise ValueError("elasticite_prix_marginal ne peut pas être zéro.")
        if abs_eps >= 1:
            # avertissement : formule suppose 0<abs_eps<1 ; laisse l'utilisateur décider
            pass

        # exposant négatif utilisé dans la formule
        exp_val = - (1 - abs_eps) / abs_eps

        # Séries (éviter 0 pour puissances négatives)
        q = self.df["q_m3_jour"].replace(0, np.nan).astype(float)
        q_redev_mp = self.df["conso_redev_m3j_mp"].replace(0, np.nan).astype(float)
        Bi = self.df["Bi"].astype(float)

        alpha = abs_eps

        # i1_12
        self.df["i1_12"] = (alpha * Bi) / (1 - alpha) * (q ** exp_val - q_redev_mp ** exp_val)

        # i2_12 : ici cout_marginal_complet_cme est un attribut scalaire de la classe
        self.df["i2_12"] = self.cout_marginal_complet_cme * (q_redev_mp - q)

        # t1_12, t2_12, somme
        self.df["t1_12"] = self.df["i1_12"]
        self.df["t2_12"] = -self.df["i2_12"]
        self.df["t1_t2_eur_jour_6"] = self.df["t1_12"] + self.df["t2_12"]

        return self.df
    
    def compute_i1_i2_13(self):
        """
        Calcule et met à jour les champs :
        - i1_13 = i1_12 * 90
        - i2_13 = i2_12 * 90
        - t1_13 = i1_13
        - t2_13 = -i2_13
        - t1_t2_eur_trim_6 = t1_13 + t2_13
        Retourne self.df
        """

        # Vérifier que les colonnes préalables existent
        required = ["i1_12", "i2_12"]
        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise KeyError(f"Colonnes manquantes pour compute_i1_i2_13: {missing}")

        # Calculs
        self.df["i1_13"] = self.df["i1_12"] * 90
        self.df["i2_13"] = self.df["i2_12"] * 90
        self.df["t1_13"] = self.df["i1_13"]
        self.df["t2_13"] = -self.df["i2_13"]
        self.df["t1_t2_eur_trim_6"] = self.df["t1_13"] + self.df["t2_13"]

        return self.df
    
    def compute_abonnement(self):
        """
        Met à jour les champs liés à l'abonnement en utilisant l'attribut self.prix_TTC_ab :
        - abonnement_ttc = self.prix_TTC_ab
        - abonnement_ttc_jour = abonnement_ttc / 90
        Retourne self.df
        """

        if not hasattr(self, "prix_TTC_ab"):
            raise AttributeError("L'attribut 'prix_TTC_ab' est manquant dans la classe.")

        # On applique la même valeur à toutes les lignes du DataFrame
        self.df["abonnement_ttc"] = self.prix_TTC_ab
        self.df["abonnement_ttc_jour"] = self.df["abonnement_ttc"] / 90

        return self.df
    
    def compute_prix_ttc(self):
        """
        Calcule les colonnes prix_ttc_t1..t4 à partir
        des colonnes montant_tva_k0..k3.
        """
        # required_cols = ["montant_tva_k0", "montant_tva_k1", "montant_tva_k2", "montant_tva_k3"]
        # for col in required_cols:
        #     if col not in self.df.columns:
        #         raise ValueError(f"La colonne {col} est manquante dans self.df.")

        # Copie des colonnes TVA vers les colonnes prix TTC
        self.df["prix_ttc_t1"] = self.montant_tva_k0
        self.df["prix_ttc_t2"] = self.montant_tva_k1
        self.df["prix_ttc_t3"] = self.montant_tva_k2
        self.df["prix_ttc_t4"] = self.montant_tva_k3

        print("✅ Colonnes prix_ttc_t1..t4 calculées avec succès.")
        return self.df
    

    def compute_prix_ln_pv(self):
        """
        Calcule les colonnes prix_i, ln_ai_i et pv_i pour i=1 à 4, sans boucle :
        prix_i = elasticite_prix_marginal * LN(prix_ttc_ti)
        ln_ai_i = LN(ai_m3_jour)
        pv_i = prix_i + ln_ai_i
        """
        import numpy as np

        # Vérification des colonnes nécessaires
        required_cols = ["ai_m3_jour", "prix_ttc_t1", "prix_ttc_t2", "prix_ttc_t3", "prix_ttc_t4"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante. Assurez-vous d'avoir exécuté les méthodes préalables.")

        # Calcul direct, sans boucle
        self.df["prix_1"] = self.elasticite_prix_marginal * np.log(self.df["prix_ttc_t1"])
        self.df["prix_2"] = self.elasticite_prix_marginal * np.log(self.df["prix_ttc_t2"])
        self.df["prix_3"] = self.elasticite_prix_marginal * np.log(self.df["prix_ttc_t3"])
        self.df["prix_4"] = self.elasticite_prix_marginal * np.log(self.df["prix_ttc_t4"])

        self.df["ln_ai_1"] = np.log(self.df["ai_m3_jour"])
        self.df["ln_ai_2"] = np.log(self.df["ai_m3_jour"])
        self.df["ln_ai_3"] = np.log(self.df["ai_m3_jour"])
        self.df["ln_ai_4"] = np.log(self.df["ai_m3_jour"])

        self.df["pv_1"] = self.df["prix_1"] + self.df["ln_ai_1"]
        self.df["pv_2"] = self.df["prix_2"] + self.df["ln_ai_2"]
        self.df["pv_3"] = self.df["prix_3"] + self.df["ln_ai_3"]
        self.df["pv_4"] = self.df["prix_4"] + self.df["ln_ai_4"]

        print("✅ Colonnes prix_i, ln_ai_i et pv_i calculées avec succès (i=1 à 4, sans boucle).")
        return self.df
    
    def compute_m3_from_pv(self):
        """
        Calcule les colonnes m3_jour_i_2 et m3_trim_i_2 à partir des colonnes pv_i :
        m3_jour_i_2 = EXP(pv_i)
        m3_trim_i_2 = m3_jour_i_2 * 90
        """
        import numpy as np

        required_cols = ["pv_1", "pv_2", "pv_3", "pv_4"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante. Assurez-vous d'avoir exécuté compute_prix_ln_pv() avant.")

        # Calcul direct
        self.df["m3_jour_1_2"] = np.exp(self.df["pv_1"])
        self.df["m3_trim_1_2"] = self.df["m3_jour_1_2"] * 90

        self.df["m3_jour_2_2"] = np.exp(self.df["pv_2"])
        self.df["m3_trim_2_2"] = self.df["m3_jour_2_2"] * 90

        self.df["m3_jour_3_2"] = np.exp(self.df["pv_3"])
        self.df["m3_trim_3_2"] = self.df["m3_jour_3_2"] * 90

        self.df["m3_jour_4_2"] = np.exp(self.df["pv_4"])
        self.df["m3_trim_4_2"] = self.df["m3_jour_4_2"] * 90

        print("✅ Colonnes m3_jour_i_2 et m3_trim_i_2 calculées avec succès (i=1 à 4).")
        return self.df
    

    def compute_conso_et_si_sc(self):
        """
        Calcule les colonnes si_i_2, sc_i_2, conso_tva_val, conso_mauvaise et diff_ib_t_pct
        selon les règles de tranches et seuils.
        """
        import numpy as np

        # Vérifications colonnes nécessaires
        required_cols = [
            "m3_trim_1_2","m3_trim_2_2","m3_trim_3_2","m3_trim_4_2",
            "c_ibt", "surconso"
        ]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        # Alias pour les seuils
        K1 = self.seuil_T_EP_K1_bis
        K2 = self.seuil_T_EP_K2_bis
        K3 = self.seuil_T_EP_K3_bis

        # si_1_2
        self.df["si_1_2"] = np.where(self.df["m3_trim_1_2"] < K1, 1, 0)

        # sc_1_2
        self.df["sc_1_2"] = np.where(
            (self.df["m3_trim_2_2"] < K1) & (self.df["m3_trim_1_2"] > K1),
            1, 0
        ) * (1 - self.df["si_1_2"])

        # si_2_2
        self.df["si_2_2"] = np.where(
            (self.df["m3_trim_2_2"] > K1) & (self.df["m3_trim_2_2"] < K2),
            1, 0
        ) * (1 - self.df["si_1_2"]) * (1 - self.df["sc_1_2"])

        # sc_2_2
        self.df["sc_2_2"] = np.where(
            (self.df["m3_trim_2_2"] > K2) & (self.df["m3_trim_3_2"] < K2),
            1, 0
        ) * (1 - self.df["si_1_2"]) * (1 - self.df["sc_1_2"]) * (1 - self.df["si_2_2"])

        # si_3_2
        self.df["si_3_2"] = np.where(
            (self.df["m3_trim_3_2"] > K2) & (self.df["m3_trim_3_2"] < K3),
            1, 0
        ) * (1 - self.df["si_1_2"]) * (1 - self.df["sc_1_2"]) * (1 - self.df["si_2_2"]) * (1 - self.df["sc_2_2"])

        # sc_3_2
        self.df["sc_3_2"] = np.where(
            (self.df["m3_trim_3_2"] > K3) & (self.df["m3_trim_4_2"] < K3),
            1, 0
        ) * (1 - self.df["si_1_2"]) * (1 - self.df["sc_1_2"]) * (1 - self.df["si_2_2"]) * (1 - self.df["sc_2_2"]) \
        * (1 - self.df["si_3_2"]) * (1 - self.df["sc_2_2"])

        # si_4_2
        self.df["si_4_2"] = np.where(
            self.df["m3_trim_4_2"] > K3,
            1, 0
        ) * (1 - self.df["si_1_2"]) * (1 - self.df["sc_1_2"]) * (1 - self.df["si_2_2"]) * (1 - self.df["sc_2_2"]) \
        * (1 - self.df["si_3_2"]) * (1 - self.df["sc_3_2"])

        # conso_tva_val
        self.df["conso_tva_val"] = (
            self.df["si_1_2"] * self.df["m3_trim_1_2"] +
            self.df["sc_1_2"] * K1 +
            self.df["si_2_2"] * self.df["m3_trim_2_2"] +
            self.df["sc_2_2"] * K2 +
            self.df["si_3_2"] * self.df["m3_trim_3_2"] +
            self.df["sc_3_2"] * K3 +
            self.df["si_4_2"] * self.df["m3_trim_4_2"]
        )

        # conso_mauvaise
        self.df["conso_mauvaise"] = self.df["conso_tva_val"] + self.df["surconso"]

        # diff_ib_t_pct
        self.df["diff_ib_t_pct"] = ((self.df["conso_mauvaise"] - self.df["c_ibt"]) / self.df["c_ibt"]) * 100

        print("✅ Colonnes si_i_2, sc_i_2, conso_tva_val, conso_mauvaise et diff_ib_t_pct calculées avec succès.")
        return self.df
    
    def compute_cout_env_non_recup(self):
        """
        Calcule la colonne cout_env_non_recup selon la formule :
        cout_env_non_recup = MAX((cout_environnemental_ce - redevances_K0), 0) * conso_mauvaise
        """
        import numpy as np

        # Vérification que conso_mauvaise existe
        if "conso_mauvaise" not in self.df.columns:
            raise ValueError("La colonne 'conso_mauvaise' est manquante. Assurez-vous d'avoir exécuté compute_conso_et_si_sc() avant.")

        # Calcul
        montant_unitaire = max(self.cout_environnemental_ce - self.redevances_K0, 0)
        self.df["cout_env_non_recup"] = montant_unitaire * self.df["conso_mauvaise"]

        print("✅ Colonne cout_env_non_recup calculée avec succès.")
        return self.df
    
    def compute_conso_ttc_m3_jour(self):
        """
        Calcule les colonnes :
        - conso_ttc_m3_jour_pp = conso_tva_val / 90
        - conso_ttc_m3_jour_mp = conso_mauvaise / 90
        """
        # Vérifications
        required_cols = ["conso_tva_val", "conso_mauvaise"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante. Assurez-vous d'avoir exécuté les méthodes préalables.")

        # Calcul
        self.df["conso_ttc_m3_jour_pp"] = self.df["conso_tva_val"] / 90
        self.df["conso_ttc_m3_jour_mp"] = self.df["conso_mauvaise"] / 90

        print("✅ Colonnes conso_ttc_m3_jour_pp et conso_ttc_m3_jour_mp calculées avec succès.")
        return self.df
    
    def compute_var_conso_and_redevance(self):
        """
        Met à jour les colonnes liées à la consommation et à la redevance
        en copiant les colonnes sources, sans boucle.
        """
        # Vérification que les colonnes source existent
        required_cols = [
            "conso_q_cout_complet_m3_trim",
            "conso_hrt_m3_trim_val",
            "conso_mauvaise_percep_m3_trim",
            "var_conso_hrt_optq",
            "var_conso_hrt_mp_optq",
            "conso_sans_tva_val",
            "conso_mauvaise_percep",
            "var_conso_redev_optq",
            "var_conso_redev_mp_optq"
        ]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne source '{col}' est manquante dans self.df.")

        # Assignations directes
        self.df["q_star_consommation_rang1"] = self.df["conso_q_cout_complet_m3_trim"]
        self.df["consommation_hrt"] = self.df["conso_hrt_m3_trim_val"]
        self.df["conso_hrt_mauvaise_perception"] = self.df["conso_mauvaise_percep_m3_trim"]
        self.df["variation_conso_hrt_optimum_q_star"] = self.df["var_conso_hrt_optq"]
        self.df["variation_conso_hrt_mp_optimum_q_star"] = self.df["var_conso_hrt_mp_optq"]
        self.df["consommation_redevance_sans_tva"] = self.df["conso_sans_tva_val"]
        self.df["conso_redevance_mauvaise_perception"] = self.df["conso_mauvaise_percep"]
        self.df["variation_conso_redevance_optimum_q_star"] = self.df["var_conso_redev_optq"]
        self.df["variation_conso_redevance_mp_optimum_q_star"] = self.df["var_conso_redev_mp_optq"]

        print("✅ Colonnes de consommation et de redevance mises à jour avec succès (sans boucle).")
        return self.df

    def compute_variation_et_effets(self):
        """
        Calcule les colonnes liées à la variation de consommation et aux effets TVA/redevance :
        - variation_conso_ttc_optimum_q_star = conso_tva_val - conso_q_cout_complet_m3_trim
        - variation_conso_hrt_q_star = consommation_hrt - q_star_consommation_rang1
        - effet_redevance = consommation_redevance_sans_tva - consommation_hrt
        - effet_tva = conso_tva_val - consommation_redevance_sans_tva
        - dummy_1_a_menage_inf_optimum = 1 si variation_conso_ttc_optimum_q_star < 0, sinon 0
        - dummy_1_b_menage_sup_optimum = 1 si variation_conso_ttc_optimum_q_star > 0, sinon 0
        - dummy_1_c_conso_egale_optimum = 1 si variation_conso_ttc_optimum_q_star == 0, sinon 0
        """
        import numpy as np

        # Vérification colonnes nécessaires
        required_cols = [
            "conso_tva_val",
            "conso_q_cout_complet_m3_trim",
            "consommation_hrt",
            "q_star_consommation_rang1",
            "consommation_redevance_sans_tva"
        ]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante. Assurez-vous d'avoir exécuté les méthodes préalables.")

        # Calcul des variations et effets
        self.df["variation_conso_ttc_optimum_q_star"] = self.df["conso_tva_val"] - self.df["conso_q_cout_complet_m3_trim"]
        self.df["variation_conso_hrt_q_star"] = self.df["consommation_hrt"] - self.df["q_star_consommation_rang1"]
        self.df["effet_redevance"] = self.df["consommation_redevance_sans_tva"] - self.df["consommation_hrt"]
        self.df["effet_tva"] = self.df["conso_tva_val"] - self.df["consommation_redevance_sans_tva"]

        # Calcul des dummies
        self.df["dummy_1_a_menage_inf_optimum"] = np.where(self.df["variation_conso_ttc_optimum_q_star"] < 0, 1, 0)
        self.df["dummy_1_b_menage_sup_optimum"] = np.where(self.df["variation_conso_ttc_optimum_q_star"] > 0, 1, 0)
        self.df["dummy_1_c_conso_egale_optimum"] = np.where(self.df["variation_conso_ttc_optimum_q_star"] == 0, 1, 0)

        print("✅ Colonnes de variation et effets calculées avec succès.")
        return self.df

    def compute_variation_et_effets_mp(self):
        """
        Calcule les colonnes liées à la variation de consommation et aux effets TTC/HTR
        pour le cas "mauvaise perception" (MP) :
        - variation_conso_ttc_mp_optimum_q_star = conso_mauvaise - conso_q_cout_complet_m3_trim
        - variation_conso_hrt_mp_q_star = conso_hrt_mauvaise_perception - q_star_consommation_rang1
        - effet_redevance_1 = conso_redevance_mauvaise_perception - conso_hrt_mauvaise_perception
        - effet_tva_1 = conso_mauvaise - conso_redevance_mauvaise_perception
        - dummy_1_d_menage_inf_optimum = 1 si variation_conso_ttc_mp_optimum_q_star < 0, sinon 0
        - dummy_1_e_menage_sup_optimum = 1 si variation_conso_ttc_mp_optimum_q_star > 0, sinon 0
        - dummy_1_f_conso_egale_optimum = 1 si variation_conso_ttc_mp_optimum_q_star == 0, sinon 0
        """
        import numpy as np

        # Vérification colonnes sources
        required_cols = [
            "conso_mauvaise",
            "conso_q_cout_complet_m3_trim",
            "conso_hrt_mauvaise_perception",
            "q_star_consommation_rang1",
            "conso_redevance_mauvaise_perception"
        ]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        # Calcul des variations et effets
        self.df["variation_conso_ttc_mp_optimum_q_star"] = self.df["conso_mauvaise"] - self.df["conso_q_cout_complet_m3_trim"]
        self.df["variation_conso_hrt_mp_q_star"] = self.df["conso_hrt_mauvaise_perception"] - self.df["q_star_consommation_rang1"]
        self.df["effet_redevance_1"] = self.df["conso_redevance_mauvaise_perception"] - self.df["conso_hrt_mauvaise_perception"]
        self.df["effet_tva_1"] = self.df["conso_mauvaise"] - self.df["conso_redevance_mauvaise_perception"]

        # Calcul des dummies
        self.df["dummy_1_d_menage_inf_optimum"] = np.where(self.df["variation_conso_ttc_mp_optimum_q_star"] < 0, 1, 0)
        self.df["dummy_1_e_menage_sup_optimum"] = np.where(self.df["variation_conso_ttc_mp_optimum_q_star"] > 0, 1, 0)
        self.df["dummy_1_f_conso_egale_optimum"] = np.where(self.df["variation_conso_ttc_mp_optimum_q_star"] == 0, 1, 0)

        print("✅ Colonnes MP de variation et effets calculées avec succès.")
        return self.df
    
    def compute_i1_i2_t1_t2(self):
        """
        Calcule les colonnes i1_14, i2_14, t1_14, t2_14 et t1_t2_euro_jour selon les formules données :
        - i1_14 = (|elasticite_prix_marginal| * Bi) / (1 - |elasticite_prix_marginal|) *
                    ((q_m3_jour ** (-(1-|elasticite_prix_marginal|)/|elasticite_prix_marginal|)) -
                    (conso_ttc_m3_jour_pp ** (-(1-|elasticite_prix_marginal|)/|elasticite_prix_marginal|)))
        - i2_14 = cout_marginal_complet_cme * (conso_ttc_m3_jour_pp - q_m3_jour)
        - t1_14 = i1_14
        - t2_14 = -i2_14
        - t1_t2_euro_jour = t1_14 + t2_14
        """
        import numpy as np

        # Vérification que les colonnes nécessaires existent
        required_cols = ["Bi", "q_m3_jour", "conso_ttc_m3_jour_pp"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        e = abs(self.elasticite_prix_marginal)
        factor = e / (1 - e)
        expo = -(1 - e) / e

        # Calcul i1_14
        self.df["i1_14"] = factor * self.df["Bi"] * (
            self.df["q_m3_jour"] ** expo - self.df["conso_ttc_m3_jour_pp"] ** expo
        )

        # Calcul i2_14
        self.df["i2_14"] = self.cout_marginal_complet_cme * (
            self.df["conso_ttc_m3_jour_pp"] - self.df["q_m3_jour"]
        )

        # Calcul t1_14 et t2_14
        self.df["t1_14"] = self.df["i1_14"]
        self.df["t2_14"] = -self.df["i2_14"]

        # Somme journalière
        self.df["t1_t2_euro_jour"] = self.df["t1_14"] + self.df["t2_14"]

        print("✅ Colonnes i1_14, i2_14, t1_14, t2_14 et t1_t2_euro_jour calculées avec succès.")
        return self.df
    
    def compute_i1_i2_t1_t2_trim(self):
        """
        Calcule les colonnes i1_15, i2_15, t1_15, t2_15 et t1_t2_euro_trim selon les formules :
        - i1_15 = i1_14 * 90
        - i2_15 = i2_14 * 90
        - t1_15 = i1_15
        - t2_15 = -i2_15
        - t1_t2_euro_trim = t1_15 + t2_15
        """
        
        # Vérification que les colonnes journalières existent
        required_cols = ["i1_14", "i2_14"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        # Calcul des colonnes trimestrielles
        self.df["i1_15"] = self.df["i1_14"] * 90
        self.df["i2_15"] = self.df["i2_14"] * 90
        self.df["t1_15"] = self.df["i1_15"]
        self.df["t2_15"] = -self.df["i2_15"]
        self.df["t1_t2_euro_trim"] = self.df["t1_15"] + self.df["t2_15"]

        print("✅ Colonnes trimestrielles i1_15, i2_15, t1_15, t2_15 et t1_t2_euro_trim calculées avec succès.")
        return self.df

    def compute_i1_i2_t1_t2_jour_mp(self):
        """
        Calcule les colonnes i1_16, i2_16, t1_16, t2_16 et t1_t2_euro_jour_1 :
        - i1_16 = (|elasticite_prix_marginal| * Bi) / (1 - |elasticite_prix_marginal|) *
                    ((q_m3_jour ** (-(1-|elasticite_prix_marginal|)/|elasticite_prix_marginal|)) -
                    (conso_ttc_m3_jour_mp ** (-(1-|elasticite_prix_marginal|)/|elasticite_prix_marginal|)))
        - i2_16 = cout_marginal_complet_cme * (conso_ttc_m3_jour_mp - q_m3_jour)
        - t1_16 = i1_16
        - t2_16 = -i2_16
        - t1_t2_euro_jour_1 = t1_16 + t2_16
        """
        import numpy as np

        # Vérification colonnes existantes
        required_cols = ["Bi", "q_m3_jour", "conso_ttc_m3_jour_mp"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        e = abs(self.elasticite_prix_marginal)
        factor = e / (1 - e)
        expo = -(1 - e) / e

        # Calcul i1_16
        self.df["i1_16"] = factor * self.df["Bi"] * (
            self.df["q_m3_jour"] ** expo - self.df["conso_ttc_m3_jour_mp"] ** expo
        )

        # Calcul i2_16
        self.df["i2_16"] = self.cout_marginal_complet_cme * (
            self.df["conso_ttc_m3_jour_mp"] - self.df["q_m3_jour"]
        )

        # t1_16 et t2_16
        self.df["t1_16"] = self.df["i1_16"]
        self.df["t2_16"] = -self.df["i2_16"]

        # Somme journalière
        self.df["t1_t2_euro_jour_1"] = self.df["t1_16"] + self.df["t2_16"]

        print("✅ Colonnes i1_16, i2_16, t1_16, t2_16 et t1_t2_euro_jour_1 calculées avec succès.")
        return self.df
    

    def compute_i1_i2_t1_t2_trim_1(self):
        """
        Calcule les colonnes trimestrielles i1_17, i2_17, t1_17, t2_17 et t1_t2_euro_trim_1
        à partir des valeurs journalières i1_16 et i2_16 :
        - i1_17 = i1_16 * 90
        - i2_17 = i2_16 * 90
        - t1_17 = i1_17
        - t2_17 = -i2_17
        - t1_t2_euro_trim_1 = t1_17 + t2_17
        """

        # Vérification que les colonnes journalières existent
        required_cols = ["i1_16", "i2_16"]
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"La colonne '{col}' est manquante dans self.df.")

        # Calcul des colonnes trimestrielles
        self.df["i1_17"] = self.df["i1_16"] * 90
        self.df["i2_17"] = self.df["i2_16"] * 90
        self.df["t1_17"] = self.df["i1_17"]
        self.df["t2_17"] = -self.df["i2_17"]
        self.df["t1_t2_euro_trim_1"] = self.df["t1_17"] + self.df["t2_17"]

        print("✅ Colonnes trimestrielles i1_17, i2_17, t1_17, t2_17 et t1_t2_euro_trim_1 calculées avec succès.")
        return self.df


    def run_all_computations(self):
        """Exécute tous les calculs dans l'ordre requis"""
        self.compute_daily_and_logs()
        # self.compute_ai_and_q()
        # self.compute_Bi()
        # self.compute_qb_and_costs()
        # self.compute_trim_values()
        # ... etc
        return self.df

    def display_columns(self, columns, step_name=""):
        """Affiche les colonnes spécifiées avec un message"""
        if step_name:
            print(f"\n{'='*50}")
            print(f"✅ {step_name}")
            print('='*50)
        print(self.df[columns].head())
        print()

    def compute_all_qb_related(self):
        """Calculs liés à qb"""
        self.compute_qb_and_costs()
        self.compute_trim_values()
        self.compute_redevance_values()
        self.compute_redevance_trim()
        return self.df

    def compute_all_ttc_related(self):
        """Calculs liés au TTC"""
        self.compute_ttc_values()
        self.compute_ttc_trim()
        return self.df

    
    
    def run_full_pipeline(self, verbose=True):
        """
        Exécute le pipeline complet de calcul des surplus.
        
        Args:
            filepath (str): Chemin vers le fichier Excel à charger
            verbose (bool): Si True, affiche les résultats intermédiaires
        
        Returns:
            pd.DataFrame: DataFrame avec tous les calculs effectués
        """
        def _print_if_verbose(*args, **kwargs):
            """Helper pour afficher uniquement si verbose=True"""
            if verbose:
                print(*args, **kwargs)
        
        # ========== CHARGEMENT DES DONNÉES ==========
        df = self.df
        _print_if_verbose(df.head())
        _print_if_verbose("Shape:", df.shape)
        
        # ========== K Q : CALCULS JOURNALIERS ==========
        df = self.compute_daily_and_logs()
        _print_if_verbose(df[["c_captive_jour", "c_nordin_jour", "c_taylor_jour",
                  "ln_c_captive_jour", "ln_c_nordin_jour", "ln_c_taylor_j",
                  "sur_conso_pct"]].head())
        
        # ========== S U : AI ET Q ==========
        df = self.compute_ai_and_q()
        _print_if_verbose(df[["ai_m3_jour", "q_m3_jour", "conso_q_cout_complet_m3_trim"]].head())
        
        df = self.compute_Bi()
        _print_if_verbose(df[["Bi"]].head())
        
        # ========== QB ET COÛTS ==========
        df = self.compute_qb_and_costs()
        _print_if_verbose(df[["ln_qb","qb_m3_jour","qb_m3_trim","i1","i2","t1","t2","t1_t2_eur_jour"]].head())
        
        df = self.compute_trim_values()
        _print_if_verbose(df[["i1_1","i2_1","t1_1","t2_1","t1_t2_eur_trim","diff_qb_tbse_pct"]].head())
        
        # ========== REDEVANCE ==========
        df = self.compute_redevance_values()
        _print_if_verbose(df[["ln_qb_redev","qb_m3_jour_1","qb_redev_sans_tva","i1_2","i2_2","t1_2","t2_2","t1_t2_eur_jour_1"]].head())
        
        df = self.compute_redevance_trim()
        _print_if_verbose(df[["i1_3","i2_3","t1_3","t2_3","t1_t2_eur_trim_1","diff_qb_redev_tbse_pct"]].head())
        
        # ========== 🔟 CALCUL DES VALEURS TTC ==========
        df = self.compute_ttc_values()
        _print_if_verbose("✅ Colonnes ln_qb_ttc, qb_m3_jour_2, qb_ttc, i1_4, i2_4, t1_4, t2_4, t1_t2_eur_jour_2 calculées")
        
        df = self.compute_ttc_trim()
        _print_if_verbose("✅ Colonnes i1_5, i2_5, t1_5, t2_5 et t1_t2_eur_trim_2 calculées diff_qb_ttc_tbse_pct")
        _print_if_verbose(df[["i1_5","i2_5","t1_5","t2_5","t1_t2_eur_trim_2","diff_qb_ttc_tbse_pct"]].head())
        
        # ========== ABONNEMENT HT ==========
        df = self.compute_abonnement_ht()
        _print_if_verbose(df[["abonnement_ht","abonnement_ht_jour"]].head())
        
        # ========== PRIX HT ET TERMES ==========
        df = self.compute_prix_ht_and_terme()
        _print_if_verbose(df[["prix_ht_t1","prix_ht_t2","prix_ht_t3","prix_ht_t4","terme_prix_1"]].head())
        
        df = self.compute_termes_and_pv()
        _print_if_verbose(df[[
            "terme_prix_1","terme_ln_ai_1","pv_1_somme",
            "terme_prix_2","terme_ln_ai_2","pv_2_somme",
            "terme_prix_3","terme_ln_ai_3","pv_3_somme",
            "terme_prix_4","terme_ln_ai_4","pv_4_somme"
        ]].head())
        
        # ========== M3 JOUR TRIM ==========
        df = self.compute_m3_jour_trim()
        _print_if_verbose(df[[
            "m3_jour_1","m3_trim_1",
            "m3_jour_2","m3_trim_2",
            "m3_jour_3","m3_trim_3",
            "m3_jour_4","m3_trim_4"
        ]].head())
        
        # ========== SI, SC ET CONSO ==========
        df = self.compute_si_sc_conso()
        _print_if_verbose(df[[
            "si_1","sc_1","si_2","sc_2","si_3","sc_3","si_4",
            "conso_hrt_m3_trim_val","conso_mauvaise_percep_m3_trim","diff_ibt_ht_pct"
        ]].head())
        
        df = self.compute_conso_hrt_pp_mp()
        _print_if_verbose(df[["conso_hrt_m3j_pp","conso_hrt_m3j_mp"]].head())
        
        df = self.compute_var_conso_and_dummies()
        _print_if_verbose(df[[
            "var_conso_hrt_optq","var_conso_hrt_mp_optq",
            "dummy_1_a_conso_moins","dummy_1_b_conso_plus","dummy_1_c_conso_eq",
            "dummy_1_d_conso_moins","dummy_1_e_conso_plus","dummy_1_f_conso_eq"
        ]].head())
        
        # ========== DÉFRAGMENTATION ==========
        df = self.defragment_dataframe()
        
        # ========== SÉRIES I1_I2_T1_T2 (6 à 9) ==========
        df = self.compute_i1_i2_t1_t2_6()
        _print_if_verbose(df[["i1_6","i2_6","t1_6","t2_6","t1_t2_eur_jour_3"]].head())
        
        df = self.compute_i1_i2_t1_t2_7()
        _print_if_verbose(df[["i1_7","i2_7","t1_7","t2_7","t1_t2_eur_trim_3"]].head())
        
        df = self.compute_i1_i2_t1_t2_8()
        _print_if_verbose(df[["i1_8","i2_8","t1_8","t2_8","t1_t2_eur_jour_4"]].head())
        
        df = self.compute_i1_i2_t1_t2_9()
        _print_if_verbose(df[["i1_9","i2_9","t1_9","t2_9","t1_t2_eur_trim_4"]].head())
        
        # ========== ABONNEMENT ET PRIX REDEV ==========
        df = self.compute_abonnement_redev()
        _print_if_verbose(df[["abonnement_redev","abonnement_redev_jour"]].head())
        
        df = self.compute_prix_redev()
        _print_if_verbose(df[["prix_redev_t1","prix_redev_t2","prix_redev_t3","prix_redev_t4"]].head())
        
        df = self.compute_pv_redev()
        _print_if_verbose(df[[
            "terme_prix_1_1","terme_ln_ai_1_1","pv_1_somme_1",
            "terme_prix_2_1","terme_ln_ai_2_1","pv_2_somme_1",
            "terme_prix_3_1","terme_ln_ai_3_1","pv_3_somme_1",
            "terme_prix_4_1","terme_ln_ai_4_1","pv_4_somme_1"
        ]].head())
        
        # ========== M3 TRIM REDEV ==========
        df = self.compute_m3_trim_redev()
        _print_if_verbose(df[[
            "m3_jour_1_1","m3_trim_1_1",
            "m3_jour_2_1","m3_trim_2_1",
            "m3_jour_3_1","m3_trim_3_1",
            "m3_jour_4_1","m3_trim_4_1"
        ]].head())
        
        # ========== CONSO REDEV INDICATEURS ==========
        df = self.compute_conso_redev_indicateurs()
        _print_if_verbose(df[[
            "si_1_1", "sc_1_1", "si_2_1", "sc_2_1",
            "si_3_1", "sc_3_1", "si_4_1",
            "conso_sans_tva_val", "conso_mauvaise_percep", "diff_ibt_redev_pct"
        ]].head())
        
        df = self.compute_conso_redev_m3j()
        _print_if_verbose(df[["conso_redev_m3j_pp", "conso_redev_m3j_mp"]].head())
        
        df = self.compute_var_conso_redev()
        _print_if_verbose(df[[
            "var_conso_redev_optq", "var_conso_redev_mp_optq",
            "dummy_1_a_conso_moins_1", "dummy_1_b_conso_plus_1", "dummy_1_c_conso_eq_1",
            "dummy_1_d_conso_moins_1", "dummy_1_e_conso_plus_1", "dummy_1_f_conso_eq_1"
        ]].head())
        
        # ========== SÉRIES I1_I2 (10 à 11) ==========
        df = self.compute_i1_i2_10()
        _print_if_verbose(df[["i1_10", "i2_10", "t1_10", "t2_10", "t1_t2_eur_jour_5"]].head())
        
        df = self.compute_i1_i2_11()
        _print_if_verbose(df[["i1_11", "i2_11", "t1_t2_eur_trim_5"]].head())
        
        # ========== DÉFRAGMENTATION 2 ==========
        df = self.defragment_dataframe()
        
        # ========== SÉRIES I1_I2 (12 à 13) ==========
        df = self.compute_i1_i2_12()
        _print_if_verbose(df[["i1_12", "i2_12", "t1_t2_eur_jour_6"]].head())
        
        df = self.compute_i1_i2_13()
        _print_if_verbose(df[["i1_13","i2_13","t1_13","t2_13","t1_t2_eur_trim_6"]].head())
        
        # ========== ABONNEMENT TTC ==========
        df = self.compute_abonnement()
        _print_if_verbose("prix_TTC_ab (attribut):", self.prix_TTC_ab)
        _print_if_verbose(df[["abonnement_ttc", "abonnement_ttc_jour"]].head())
        
        # ========== PRIX TTC ==========
        df = self.compute_prix_ttc()
        _print_if_verbose(df[["prix_ttc_t1", "prix_ttc_t2", "prix_ttc_t3", "prix_ttc_t4"]].head())
        
        df = self.compute_prix_ln_pv()
        _print_if_verbose(df[["prix_1", "ln_ai_1", "pv_1", "prix_2", "ln_ai_2", "pv_2"]].head())
        
        df = self.compute_m3_from_pv()
        _print_if_verbose(df[["m3_jour_1_2","m3_trim_1_2","m3_jour_2_2","m3_trim_2_2"]].head())
        
        # ========== CONSO ET SI SC FINAL ==========
        df = self.compute_conso_et_si_sc()
        _print_if_verbose(df[["si_1_2","sc_1_2","si_2_2","sc_2_2","si_3_2","sc_3_2","si_4_2","conso_tva_val","conso_mauvaise","diff_ib_t_pct"]].head())
        
        df = self.compute_cout_env_non_recup()
        _print_if_verbose(df[["conso_mauvaise","cout_env_non_recup"]].head())
        
        df = self.compute_conso_ttc_m3_jour()
        _print_if_verbose(df[["conso_ttc_m3_jour_pp", "conso_ttc_m3_jour_mp"]].head())
        
        # ========== VARIATIONS ET EFFETS ==========
        df = self.compute_var_conso_and_redevance()
        _print_if_verbose(df[[
            "q_star_consommation_rang1", "consommation_hrt",
            "conso_hrt_mauvaise_perception", "variation_conso_hrt_optimum_q_star"
        ]].head())
        
        df = self.compute_variation_et_effets()
        _print_if_verbose(df[[
            "variation_conso_ttc_optimum_q_star",
            "variation_conso_hrt_q_star",
            "effet_redevance",
            "effet_tva",
            "dummy_1_a_menage_inf_optimum",
            "dummy_1_b_menage_sup_optimum",
            "dummy_1_c_conso_egale_optimum"
        ]].head())
        
        df = self.compute_variation_et_effets_mp()
        _print_if_verbose(df[[
            "variation_conso_ttc_mp_optimum_q_star",
            "variation_conso_hrt_mp_q_star",
            "effet_redevance_1",
            "effet_tva_1",
            "dummy_1_d_menage_inf_optimum",
            "dummy_1_e_menage_sup_optimum",
            "dummy_1_f_conso_egale_optimum"
        ]].head())
        
        # ========== SÉRIES I1_I2 FINALES (14 à 17) ==========
        df = self.compute_i1_i2_t1_t2()
        _print_if_verbose(df[["i1_14","i2_14","t1_14","t2_14","t1_t2_euro_jour"]].head())
        
        df = self.compute_i1_i2_t1_t2_trim()
        _print_if_verbose(df[["i1_15","i2_15","t1_15","t2_15","t1_t2_euro_trim"]].head())
        
        df = self.compute_i1_i2_t1_t2_jour_mp()
        _print_if_verbose(df[["i1_16","i2_16","t1_16","t2_16","t1_t2_euro_jour_1"]].head())
        
        df = self.compute_i1_i2_t1_t2_trim_1()
        _print_if_verbose(df[["i1_17","i2_17","t1_17","t2_17","t1_t2_euro_trim_1"]].head())
        
        return df


# === MAIN TEST ===
if __name__ == "__main__":



    # Instanciation directe de dfsource
    dfsource = pd.DataFrame({
        "menage": [101, 102, 103, 104],
        "assaini": [1, 0, 1, 0],
        "revenu_net_mois": [2200, 1800, 2500, 2000],
        "c_m3_trim_2": [12.5, 8.3, 15.0, 9.2],
        "c_m3_trim": [12.5*90, 8.3*90, 15.0*90, 9.2*90],
        "c_ibt": [14.0, 9.5, 16.0, 10.0],
        "c_ibt_pp": [12.0, 8.0, 13.0, 9.0],
        "c_tbse": [0.30, 0.25, 0.35, 0.28],
        "consom_nordin_trim": [12.0, 8.0, 13.0, 9.0],
        "consom_taylor_trim": [11.8, 8.2, 14.2, 9.1],
        "sur_conso_1": [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0],
        "sur_conso_2": [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0],
        "surconso":   [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0]
    })

    # Affichage pour vérification
    print(dfsource)


    surplus = surplusG1CP(dfsource)
    
    # Avec affichage détaillé (comportement par défaut)
    df = surplus.run_full_pipeline()
    
    # OU sans affichage (pour exécution silencieuse)
    # df = surplus.run_full_pipeline("surplusG1_data.xls", verbose=False)
    
    # Vous pouvez ensuite utiliser df pour d'autres analyses
    print("\n" + "="*50)
    print("Pipeline terminé. DataFrame final disponible.")
    print("="*50)

