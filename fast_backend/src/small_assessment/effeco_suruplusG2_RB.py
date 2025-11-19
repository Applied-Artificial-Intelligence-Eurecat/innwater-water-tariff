import pandas as pd
import numpy as np
from datetime import datetime
import os

#from EffecotestDatabaseCreatopCSV import EffecotestDatabaseCreatopCSV
# from DataFrameComparator import DataFrameComparator

class effeco_suruplusG2_CP:
    """
    Classe pour initialiser les paramètres économiques et de tarification
    """
    
    def __init__(self, df : pd.DataFrame):
        # Élasticités
        self.elasticite_prix_marginal = -0.31
        self.elasticite_revenu_virtuel = 0.25
        
        # Prix et coûts de base
        self.prix_pi = 1.3
        self.cout_marginal_complet_cme = 10.9

        
        # Redevances
        self.redevances_accise_euro_m3 = 0.16
        
        # Prix HT opérateur EPA
        self.prix_ht_op_a_EPA = 34.235
        self.prix_ht_op_T_EPA_T1 = 2.178
        self.prix_ht_op_T_EPA_T2 = 3.959
        self.prix_ht_op_T_EPA_T3 = 4.978
        self.prix_ht_op_T_EPA_T4 = 6.88
        
        # Seuils EPA
        self.seuil_T_EPA_T4 = 15
        self.seuil_T_EPA_T5 = 30
        self.seuil_T_EPA_T6 = 60
        
        # Seuils EPA bis
        self.seuil_T_EPA_T4_bis = 15
        self.seuil_T_EPA_T5_bis = 30
        self.seuil_T_EPA_T6_bis = 60
        
        # Prix HTVA EPA
        self.prix_htva_ab_EPA = 34.235
        self.prix_htva_t_EPA_T1 = 2.338
        self.prix_htva_t_EPA_T2 = 4.119
        self.prix_htva_t_EPA_T3 = 5.138
        self.prix_htva_t_EPA_T4 = 7.04
        
        # Prix TTC EPA
        self.prix_ttc_a_EPA = 36.18199
        self.prix_ttc_T_EPA_T1 = 2.492958
        self.prix_ttc_T_EPA_T2 = 4.376139
        self.prix_ttc_T_EPA_T3 = 5.423648
        self.prix_ttc_T_EPA_T4 = 7.3885
        
        # Autres paramètres
        self.tbse_epa_prix_ttc = 1.52542
        self.cvm = 0.40
        self.redevances_tarif_ep = 0.12
        self.redevances_tarif_a = 0.04
        self.cout_environnemental_ce = 10
        self.df= df
    
    def __str__(self):
        """
        Méthode pour afficher les valeurs de la classe
        """
        attributes = []
        for attr, value in self.__dict__.items():
            attributes.append(f"{attr}: {value}")
        return "\n".join(attributes)
    
    def get_elasticites(self):
        """
        Retourne les élasticités
        """
        return {
            'elasticite_prix_marginal': self.elasticite_prix_marginal,
            'elasticite_revenu_virtuel': self.elasticite_revenu_virtuel
        }
    
    def get_prix_ht_epa(self):
        """
        Retourne les prix HT EPA
        """
        return {
            'prix_ht_op_a_EPA': self.prix_ht_op_a_EPA,
            'prix_ht_op_T_EPA_T1': self.prix_ht_op_T_EPA_T1,
            'prix_ht_op_T_EPA_T2': self.prix_ht_op_T_EPA_T2,
            'prix_ht_op_T_EPA_T3': self.prix_ht_op_T_EPA_T3,
            'prix_ht_op_T_EPA_T4': self.prix_ht_op_T_EPA_T4
        }
    
    def get_seuils_epa(self):
        """
        Retourne les seuils EPA
        """
        return {
            'seuil_T_EPA_T4': self.seuil_T_EPA_T4,
            'seuil_T_EPA_T5': self.seuil_T_EPA_T5,
            'seuil_T_EPA_T6': self.seuil_T_EPA_T6,
            'seuil_T_EPA_T4_bis': self.seuil_T_EPA_T4_bis,
            'seuil_T_EPA_T5_bis': self.seuil_T_EPA_T5_bis,
            'seuil_T_EPA_T6_bis': self.seuil_T_EPA_T6_bis
        }
    
    def create_dataframe_structure(self):
        """
        Crée un DataFrame avec la structure demandée en récupérant les données du fichier Excel
        
        Args:
            file_path (str): Chemin vers le fichier Excel (par défaut "surplus_G2_data.xls")
            sheet_name (str, optional): Nom de la feuille à lire
            
        Returns:
            pd.DataFrame: DataFrame avec toutes les colonnes, les premières initialisées avec les vraies données
        """
        # Colonnes complètes du DataFrame final
        columns = [
            'menage', 'assaini', 'revenu_net_mois', 'c_m3_trim', 'c_m3_trim_2', 'c_ibt',
            'c_ibt_pp', 'c_tbse', 'consom_nordin_trim', 'consom_taylor_trim', 'c_captive_jour',
            'c_nordin_jour', 'c_taylor_jour', 'ln_c_captive_jour', 'ln_c_nordin_jour', 'ln_c_taylor_j',
            'sur_conso_pct', 'ai_m3_jour', 'q_m3_jour', 'conso_q_cout_complet_m3_trim', 'Bi',
            'ln_qb', 'qb_m3_jour', 'qb_m3_trim', 'i1', 'i2', 't1', 't2', 't1_t2_eur_jour',
            'i1_1', 'i2_1', 't1_1', 't2_1', 't1_t2_eur_trim', 'diff_qb_tbse_pct', 'ln_qb_redev',
            'qb_m3_jour_1', 'qb_redev_sans_tva', 'i1_2', 'i2_2', 't1_2', 't2_2', 't1_t2_eur_jour_1',
            'i1_3', 'i2_3', 't1_3', 't2_3', 't1_t2_eur_trim_1', 'diff_qb_redev_tbse_pct', 'ln_qb_ttc',
            'qb_m3_jour_2', 'qb_ttc', 'i1_4', 'i2_4', 't1_4', 't2_4', 't1_t2_eur_jour_2',
            'i1_5', 'i2_5', 't1_5', 't2_5', 't1_t2_eur_trim_2', 'diff_qb_ttc_tbse_pct', 'abonnement_ht',
            'abonnement_ht_jour', 'prix_ht_t1', 'prix_ht_t2', 'prix_ht_t3', 'prix_ht_t4', 'terme_prix_1',
            'terme_ln_ai_1', 'pv_1_somme', 'terme_prix_2', 'terme_ln_ai_2', 'pv_2_somme', 'terme_prix_3',
            'terme_ln_ai_3', 'pv_3_somme', 'terme_prix_4', 'terme_ln_ai_4', 'pv_4_somme', 'm3_jour_1',
            'm3_trim_1', 'm3_jour_2', 'm3_trim_2', 'm3_jour_3', 'm3_trim_3', 'm3_jour_4',
            'm3_trim_4', 'si_1', 'sc_1', 'si_2', 'sc_2', 'si_3', 'sc_3', 'si_4',
            'conso_hrt_m3_trim', 'conso_hrt_m3_trim_val', 'sur_conso_1', 'conso_mauvaise_percep_m3_trim',
            'diff_ibt_ht_pct', 'conso_hrt_m3j_pp', 'conso_hrt_m3j_mp', 'var_conso_hrt_optq',
            'var_conso_hrt_mp_optq', 'dummy_1_a_conso_moins', 'dummy_1_b_conso_plus', 'dummy_1_c_conso_eq',
            'dummy_1_d_conso_moins', 'dummy_1_e_conso_plus', 'dummy_1_f_conso_eq', 'i1_6', 'i2_6',
            't1_6', 't2_6', 't1_t2_eur_jour_3', 'i1_7', 'i2_7', 't1_7', 't2_7', 't1_t2_eur_trim_3',
            'i1_8', 'i2_8', 't1_8', 't2_8', 't1_t2_eur_jour_4', 'i1_9', 'i2_9', 't1_9', 't2_9',
            't1_t2_eur_trim_4', 'abonnement_redev', 'abonnement_redev_jour', 'prix_redev_t1',
            'prix_redev_t2', 'prix_redev_t3', 'prix_redev_t4', 'terme_prix_1_1', 'terme_ln_ai_1_1',
            'pv_1_somme_1', 'terme_prix_2_1', 'terme_ln_ai_2_1', 'pv_2_somme_1', 'terme_prix_3_1',
            'terme_ln_ai_3_1', 'pv_3_somme_1', 'terme_prix_4_1', 'terme_ln_ai_4_1', 'pv_4_somme_1',
            'm3_jour_1_1', 'm3_trim_1_1', 'm3_jour_2_1', 'm3_trim_2_1', 'm3_jour_3_1', 'm3_trim_3_1',
            'm3_jour_4_1', 'm3_trim_4_1', 'si_1_1', 'sc_1_1', 'si_2_1', 'sc_2_1', 'si_3_1',
            'sc_3_1', 'si_4_1', 'conso_sans_tva', 'conso_sans_tva_val', 'sur_conso_2',
            'conso_mauvaise_percep', 'diff_ibt_redev_pct', 'conso_redev_m3j_pp', 'conso_redev_m3j_mp',
            'var_conso_redev_optq', 'var_conso_redev_mp_optq', 'dummy_1_a_conso_moins_1',
            'dummy_1_b_conso_plus_1', 'dummy_1_c_conso_eq_1', 'dummy_1_d_conso_moins_1',
            'dummy_1_e_conso_plus_1', 'dummy_1_f_conso_eq_1', 'i1_10', 'i2_10', 't1_10', 't2_10',
            't1_t2_eur_jour_5', 'i1_11', 'i2_11', 't1_11', 't2_11', 't1_t2_eur_trim_5', 'i1_12',
            'i2_12', 't1_12', 't2_12', 't1_t2_eur_jour_6', 'i1_13', 'i2_13', 't1_13', 't2_13',
            't1_t2_eur_trim_6', 'abonnement_ttc', 'abonnement_ttc_jour', 'prix_ttc_t1', 'prix_ttc_t2',
            'prix_ttc_t3', 'prix_ttc_t4', 'prix_1', 'ln_ai_1', 'pv_1', 'prix_2', 'ln_ai_2',
            'pv_2', 'prix_3', 'ln_ai_3', 'pv_3', 'prix_4', 'ln_ai_4', 'pv_4', 'm3_jour_1_2',
            'm3_trim_1_2', 'm3_jour_2_2', 'm3_trim_2_2', 'm3_jour_3_2', 'm3_trim_3_2', 'm3_jour_4_2',
            'm3_trim_4_2', 'si_1_2', 'sc_1_2', 'si_2_2', 'sc_2_2', 'si_3_2', 'sc_3_2', 'si_4_2',
            'conso_tva', 'conso_tva_val', 'surconso', 'conso_mauvaise', 'diff_ib_t_pct',
            'cout_env_non_recup', 'conso_ttc_m3_jour_pp', 'conso_ttc_m3_jour_mp', 'q_star_consommation_rang1',
            'consommation_hrt', 'conso_hrt_mauvaise_perception', 'variation_conso_hrt_optimum_q_star',
            'variation_conso_hrt_mp_optimum_q_star', 'consommation_redevance_sans_tva',
            'conso_redevance_mauvaise_perception', 'variation_conso_redevance_optimum_q_star',
            'variation_conso_redevance_mp_optimum_q_star', 'variation_conso_ttc_optimum_q_star',
            'variation_conso_hrt_q_star', 'effet_redevance', 'effet_tva', 'dummy_1_a_menage_inf_optimum',
            'dummy_1_b_menage_sup_optimum', 'dummy_1_c_conso_egale_optimum', 'variation_conso_ttc_mp_optimum_q_star',
            'variation_conso_hrt_mp_q_star', 'effet_redevance_1', 'effet_tva_1', 'dummy_1_d_menage_inf_optimum',
            'dummy_1_e_menage_sup_optimum', 'dummy_1_f_conso_egale_optimum', 'i1_14', 'i2_14', 't1_14',
            't2_14', 't1_t2_euro_jour', 'i1_15', 'i2_15', 't1_15', 't2_15', 't1_t2_euro_trim',
            'i1_16', 'i2_16', 't1_16', 't2_16', 't1_t2_euro_jour_1', 'i1_17', 'i2_17', 't1_17',
            't2_17', 't1_t2_euro_trim_1'
        ]
        
        # Colonnes à initialiser avec les vraies données
        data_columns = [
            'menage', 'assaini', 'revenu_net_mois', 'c_m3_trim', 'c_m3_trim_2', 'c_ibt',
            'c_ibt_pp', 'c_tbse', 'consom_nordin_trim', 'consom_taylor_trim', 'sur_conso_1', 'sur_conso_2'
        ]
        
        try:
            
            print(f"Données chargées:  de la DF")
            # Charger les données depuis le fichier Excel
            excel_data = self.df
            # Créer le DataFrame final avec toutes les colonnes
            df_final = pd.DataFrame(columns=columns)
            
            # Initialiser toutes les colonnes avec NaN pour le nombre de lignes des données réelles
            nb_menages = len(excel_data)
            data_dict = {col: [np.nan] * nb_menages for col in columns}
            df_final = pd.DataFrame(data_dict)
            
            # Copier les données existantes dans les colonnes correspondantes
            for col in data_columns:
                if col in excel_data.columns:
                    df_final[col] = excel_data[col].values
                    print(f"Colonne '{col}' initialisée avec les données du fichier")
                else:
                    print(f"Attention: Colonne '{col}' non trouvée dans les données Excel")
            df_final['surconso'] = df_final['sur_conso_1']
            print(f"DataFrame créé avec {len(df_final)} lignes et {len(df_final.columns)} colonnes")
            print(f"Colonnes initialisées avec les vraies données: {data_columns}")
            
            return df_final
            
        except Exception as e:
            print(f"Erreur lors du chargement des données: {str(e)}")
            print("Création d'un DataFrame vide avec la structure complète...")
            
            # En cas d'erreur, créer un DataFrame vide avec la structure
            df_empty = pd.DataFrame(columns=columns)
            return df_empty

   
    
    def _export_parameters_sheet(self, writer):
        """
        Crée une feuille avec tous les paramètres de la classe
        
        Args:
            writer: L'objet ExcelWriter
        """
        try:
            # Créer un DataFrame avec les paramètres
            params_data = []
            for attr, value in self.__dict__.items():
                params_data.append({
                    'Parametre': attr,
                    'Valeur': value,
                    'Type': type(value).__name__
                })
            
            params_df = pd.DataFrame(params_data)
            params_df.to_excel(writer, sheet_name='Parametres', index=False)
            print(f"✅ Paramètres exportés vers la feuille 'Parametres'")
            
        except Exception as e:
            print(f"⚠️  Erreur lors de l'export des paramètres: {str(e)}")
    
    def _export_metadata_sheet(self, writer, dataframe, main_sheet_name):
        """
        Crée une feuille avec les métadonnées de l'export
        
        Args:
            writer: L'objet ExcelWriter  
            dataframe: Le DataFrame principal
            main_sheet_name: Nom de la feuille principale
        """
        try:
            # Informations générales
            metadata = {
                'Information': [
                    'Date d\'export',
                    'Heure d\'export', 
                    'Nombre de lignes',
                    'Nombre de colonnes',
                    'Nom de la feuille principale',
                    'Taille mémoire (MB)',
                    'Colonnes avec données non-nulles',
                    'Colonnes entièrement vides'
                ],
                'Valeur': [
                    datetime.now().strftime("%Y-%m-%d"),
                    datetime.now().strftime("%H:%M:%S"),
                    len(dataframe),
                    len(dataframe.columns),
                    main_sheet_name,
                    round(dataframe.memory_usage(deep=True).sum() / 1024**2, 2),
                    dataframe.count().sum(),
                    (dataframe.isnull().all()).sum()
                ]
            }
            
            metadata_df = pd.DataFrame(metadata)
            metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            print(f"✅ Métadonnées exportées vers la feuille 'Metadata'")
            
        except Exception as e:
            print(f"⚠️  Erreur lors de l'export des métadonnées: {str(e)}")

    def calculate_derived_columns(self, dataframe):
        """
        Calcule toutes les colonnes dérivées basées sur les formules économiques
        
        Args:
            dataframe (pd.DataFrame): Le DataFrame avec les données de base
            
        Returns:
            pd.DataFrame: Le DataFrame avec toutes les colonnes calculées
            
        Raises:
            Exception: En cas d'erreur lors du calcul
        """
        
        print("\n" + "="*60)
        print("CALCUL DES COLONNES DÉRIVÉES")
        print("="*60)
        
        try:
            df = dataframe.copy()
            
            # Vérifier les colonnes de base nécessaires
            required_columns = ['c_m3_trim', 'revenu_net_mois', 'consom_nordin_trim', 
                              'consom_taylor_trim', 'c_ibt', 'c_ibt_pp', 'c_tbse',
                              'sur_conso_1', 'sur_conso_2']
            
            missing_cols = [col for col in required_columns if col not in df.columns or df[col].isnull().all()]
            if missing_cols:
                print(f"⚠️  Colonnes manquantes ou vides: {missing_cols}")
            
            print("📊 Début des calculs des colonnes dérivées...")
          
            # 1. Calculs de base - consommations journalières
            print("  1. Calculs des consommations journalières...")
            df['c_captive_jour'] = df['c_m3_trim'] / 90
            df['c_nordin_jour'] = df['consom_nordin_trim'] / 90
            df['c_taylor_jour'] = df['consom_taylor_trim'] / 90
            
            # 2. Logarithmes
            print("  2. Calculs des logarithmes...")
            df['ln_c_captive_jour'] = np.log(df['c_m3_trim'])
            df['ln_c_nordin_jour'] = np.log(df['c_nordin_jour'])
            df['ln_c_taylor_j'] = np.log(df['c_taylor_jour'])
            
            # 3. Surconsommation en pourcentage
            print("  3. Calcul de la surconsommation...")
            df['sur_conso_pct'] = 100 * (df['ln_c_taylor_j'] - df['ln_c_nordin_jour'])
            
            # 4. Variables économiques de base
            print("  4. Variables économiques de base...")
            df['ai_m3_jour'] = (df['c_m3_trim'] / 90) * ((df['revenu_net_mois'] / 30) ** self.elasticite_revenu_virtuel)
            df['q_m3_jour'] = df['ai_m3_jour'] / (self.cout_marginal_complet_cme ** abs(self.elasticite_prix_marginal))
            df['conso_q_cout_complet_m3_trim'] = df['q_m3_jour'] * 90
            df['Bi'] = df['ai_m3_jour'] ** (1 / abs(self.elasticite_prix_marginal))
            
            # 5. Calculs qb (quantité de base)
            print("  5. Calculs des quantités de base...")
            df['ln_qb'] = (np.log(df['c_m3_trim'] / 90) + 
                          (self.elasticite_revenu_virtuel * np.log(df['revenu_net_mois'] / 30)) - 
                          (abs(self.elasticite_prix_marginal) * np.log(self.prix_pi)))
            df['qb_m3_jour'] = np.exp(df['ln_qb'])
            df['qb_m3_trim'] = df['qb_m3_jour'] * 90
            
            # 6. Calculs intégrales et surplus (i1, i2, t1, t2) - scénario de base
            print("  6. Calculs des intégrales et surplus (scénario de base)...")
            elasticite_abs = abs(self.elasticite_prix_marginal)
            exposant = -((1 - elasticite_abs) / elasticite_abs)
            
            df['i1'] = ((elasticite_abs * df['Bi']) / (1 - elasticite_abs) * 
                       ((df['q_m3_jour'] ** exposant) - (df['qb_m3_jour'] ** exposant)))
            df['i2'] = self.cout_marginal_complet_cme * (df['qb_m3_jour'] - df['q_m3_jour'])
            df['t1'] = df['i1']
            df['t2'] = -df['i2']
            df['t1_t2_eur_jour'] = df['t1'] + df['t2']
            
            # Version trimestrielle
            df['i1_1'] = df['i1'] * 90
            df['i2_1'] = df['i2'] * 90
            df['t1_1'] = df['i1_1']
            df['t2_1'] = -df['i2_1']
            df['t1_t2_eur_trim'] = df['t1_1'] + df['t2_1']
            
            # 7. Différence avec TBSE
            print("  7. Calcul des différences avec TBSE...")
            df['diff_qb_tbse_pct'] = ((df['qb_m3_trim'] - df['c_tbse']) / df['c_tbse']) * 100
            
            # 8. Scénario avec redevances
            print("  8. Scénario avec redevances...")
            df['ln_qb_redev'] = (np.log(df['c_m3_trim'] / 90) + 
                                (self.elasticite_revenu_virtuel * np.log(df['revenu_net_mois'] / 30)) - 
                                (abs(self.elasticite_prix_marginal) * np.log(self.prix_pi + self.redevances_accise_euro_m3)))
            df['qb_m3_jour_1'] = np.exp(df['ln_qb_redev'])
            df['qb_redev_sans_tva'] = df['qb_m3_jour_1'] * 90
            
            # Intégrales pour redevances
            df['i1_2'] = ((elasticite_abs * df['Bi']) / (1 - elasticite_abs) * 
                         ((df['q_m3_jour'] ** exposant) - (df['qb_m3_jour_1'] ** exposant)))
            df['i2_2'] = self.cout_marginal_complet_cme * (df['qb_m3_jour_1'] - df['q_m3_jour'])
            df['t1_2'] = df['i1_2']
            df['t2_2'] = -df['i2_2']
            df['t1_t2_eur_jour_1'] = df['t1_2'] + df['t2_2']
            
            # Version trimestrielle
            df['i1_3'] = df['i1_2'] * 90
            df['i2_3'] = df['i2_2'] * 90
            df['t1_3'] = df['i1_3']
            df['t2_3'] = -df['i2_3']
            df['t1_t2_eur_trim_1'] = df['t1_3'] + df['t2_3']
            
            # 9. Différence redevances avec TBSE
            df['diff_qb_redev_tbse_pct'] = ((df['qb_redev_sans_tva'] - df['c_tbse']) / df['c_tbse']) * 100
            
            # 10. Scénario TTC
            print("  9. Scénario TTC...")
            df['ln_qb_ttc'] = (np.log(df['c_m3_trim'] / 90) + 
                              (self.elasticite_revenu_virtuel * np.log(df['revenu_net_mois'] / 30)) - 
                              (abs(self.elasticite_prix_marginal) * np.log(self.tbse_epa_prix_ttc)))
            df['qb_m3_jour_2'] = np.exp(df['ln_qb_ttc'])
            df['qb_ttc'] = df['qb_m3_jour_2'] * 90
            
            # Intégrales pour TTC
            df['i1_4'] = ((elasticite_abs * df['Bi']) / (1 - elasticite_abs) * 
                         ((df['q_m3_jour'] ** exposant) - (df['qb_m3_jour_2'] ** exposant)))
            df['i2_4'] = self.cout_marginal_complet_cme * (df['qb_m3_jour_2'] - df['q_m3_jour'])
            df['t1_4'] = df['i1_4']
            df['t2_4'] = -df['i2_4']
            df['t1_t2_eur_jour_2'] = df['t1_4'] + df['t2_4']
            
            # Version trimestrielle
            df['i1_5'] = df['i1_4'] * 90
            df['i2_5'] = df['i2_4'] * 90
            df['t1_5'] = df['i1_5']
            df['t2_5'] = -df['i2_5']
            df['t1_t2_eur_trim_2'] = df['t1_5'] + df['t2_5']
            
            # 11. Différence TTC avec TBSE
            df['diff_qb_ttc_tbse_pct'] = ((df['qb_ttc'] - df['c_tbse']) / df['c_tbse']) * 100
            
            print("  10. Calculs des prix et abonnements...")
            # 12. Prix et abonnements HT
            df['abonnement_ht'] = self.prix_ht_op_a_EPA
            df['abonnement_ht_jour'] = df['abonnement_ht'] / 90
            df['prix_ht_t1'] = self.prix_ht_op_T_EPA_T1
            df['prix_ht_t2'] = self.prix_ht_op_T_EPA_T2
            df['prix_ht_t3'] = self.prix_ht_op_T_EPA_T3
            df['prix_ht_t4'] = self.prix_ht_op_T_EPA_T4
            
            # Calculs des termes de prix (HT)
            df['terme_prix_1'] = self.elasticite_prix_marginal * np.log(df['prix_ht_t1'])
            df['terme_ln_ai_1'] = np.log(df['ai_m3_jour'])
            df['pv_1_somme'] = df['terme_prix_1'] + df['terme_ln_ai_1']
            
            df['terme_prix_2'] = self.elasticite_prix_marginal * np.log(df['prix_ht_t2'])
            df['terme_ln_ai_2'] = np.log(df['ai_m3_jour'])
            df['pv_2_somme'] = df['terme_prix_2'] + df['terme_ln_ai_2']
            
            df['terme_prix_3'] = self.elasticite_prix_marginal * np.log(df['prix_ht_t3'])
            df['terme_ln_ai_3'] = np.log(df['ai_m3_jour'])
            df['pv_3_somme'] = df['terme_prix_3'] + df['terme_ln_ai_3']
            
            df['terme_prix_4'] = self.elasticite_prix_marginal * np.log(df['prix_ht_t4'])
            df['terme_ln_ai_4'] = np.log(df['ai_m3_jour'])
            df['pv_4_somme'] = df['terme_prix_4'] + df['terme_ln_ai_4']
            
            # Consommations par tranches (HT)
            df['m3_jour_1'] = np.exp(df['pv_1_somme'])
            df['m3_trim_1'] = df['m3_jour_1'] * 90
            df['m3_jour_2'] = np.exp(df['pv_2_somme'])
            df['m3_trim_2'] = df['m3_jour_2'] * 90
            df['m3_jour_3'] = np.exp(df['pv_3_somme'])
            df['m3_trim_3'] = df['m3_jour_3'] * 90
            df['m3_jour_4'] = np.exp(df['pv_4_somme'])
            df['m3_trim_4'] = df['m3_jour_4'] * 90
            
            # Fonction conditionnelle SI/ET (HT)
            print("  11. Calculs des conditions de tranches (HT)...")
            df['si_1'] = np.where(df['m3_trim_1'] < self.seuil_T_EPA_T4_bis, 1, 0)
            df['sc_1'] = np.where((df['m3_trim_2'] < self.seuil_T_EPA_T4_bis) & 
                                 (df['m3_trim_1'] > self.seuil_T_EPA_T4_bis), 1, 0) * (1 - df['si_1'])
            df['si_2'] = np.where((df['m3_trim_2'] > self.seuil_T_EPA_T4_bis) & 
                                 (df['m3_trim_2'] < self.seuil_T_EPA_T5_bis), 1, 0) * (1 - df['si_1']) * (1 - df['sc_1'])
            df['sc_2'] = np.where((df['m3_trim_2'] > self.seuil_T_EPA_T5_bis) & 
                                 (df['m3_trim_3'] < self.seuil_T_EPA_T5_bis), 1, 0) * (1 - df['si_1']) * (1 - df['sc_1']) * (1 - df['si_2'])
            df['si_3'] = np.where((df['m3_trim_3'] > self.seuil_T_EPA_T5_bis) & 
                                 (df['m3_trim_3'] < self.seuil_T_EPA_T6_bis), 1, 0) * (1 - df['si_1']) * (1 - df['sc_1']) * (1 - df['si_2']) * (1 - df['sc_2'])
            df['sc_3'] = np.where((df['m3_trim_3'] > self.seuil_T_EPA_T6_bis) & 
                                 (df['m3_trim_4'] < self.seuil_T_EPA_T6_bis), 1, 0) * (1 - df['si_1']) * (1 - df['sc_1']) * (1 - df['si_2']) * (1 - df['sc_2']) * (1 - df['si_3'])
            df['si_4'] = np.where(df['m3_trim_4'] > self.seuil_T_EPA_T6_bis, 1, 0) * (1 - df['si_1']) * (1 - df['sc_1']) * (1 - df['si_2']) * (1 - df['sc_2']) * (1 - df['si_3']) * (1 - df['sc_3'])
            
            # Consommations HRT
            print("  12. Calculs des consommations HRT...")
            df['conso_hrt_m3_trim'] = 0  # Initialisé à 0 selon les specs
            df['conso_hrt_m3_trim_val'] = (df['si_1'] * df['m3_trim_1'] + 
                                          df['sc_1'] * self.seuil_T_EPA_T4 + 
                                          df['si_2'] * df['m3_trim_2'] + 
                                          df['sc_2'] * self.seuil_T_EPA_T5 + 
                                          df['si_3'] * df['m3_trim_3'] + 
                                          df['sc_3'] * self.seuil_T_EPA_T6 + 
                                          df['si_4'] * df['m3_trim_4'])
            
            df['conso_mauvaise_percep_m3_trim'] = df['conso_hrt_m3_trim_val'] + df['sur_conso_1']
            df['diff_ibt_ht_pct'] = ((df['conso_mauvaise_percep_m3_trim'] - df['c_ibt_pp']) / df['c_ibt_pp']) * 100
            
            # Variables dérivées HRT
            df['conso_hrt_m3j_pp'] = df['conso_hrt_m3_trim_val'] / 90
            df['conso_hrt_m3j_mp'] = df['conso_mauvaise_percep_m3_trim'] / 90
            df['var_conso_hrt_optq'] = df['conso_hrt_m3_trim_val'] - df['conso_q_cout_complet_m3_trim']
            df['var_conso_hrt_mp_optq'] = df['conso_mauvaise_percep_m3_trim'] - df['conso_q_cout_complet_m3_trim']
            
            # Variables dummy pour HRT
            df['dummy_1_a_conso_moins'] = np.where(df['var_conso_hrt_optq'] < 0, 1, 0)
            df['dummy_1_b_conso_plus'] = np.where(df['var_conso_hrt_optq'] > 0, 1, 0)
            df['dummy_1_c_conso_eq'] = np.where(df['var_conso_hrt_optq'] == 0, 1, 0)
            df['dummy_1_d_conso_moins'] = np.where(df['var_conso_hrt_mp_optq'] < 0, 1, 0)
            df['dummy_1_e_conso_plus'] = np.where(df['var_conso_hrt_mp_optq'] > 0, 1, 0)
            df['dummy_1_f_conso_eq'] = np.where(df['var_conso_hrt_mp_optq'] == 0, 1, 0)
            
            print("✅ Calculs terminés avec succès!")
            print(f"   - Colonnes calculées: {len([col for col in df.columns if not df[col].isnull().all()])}")
            print(f"   - Lignes traitées: {len(df)}")
            
            return df
            
        except Exception as e:
            error_msg = f"Erreur lors du calcul des colonnes dérivées: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    def calculate_additional_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remplit les colonnes existantes du DataFrame avec les règles supplémentaires
        sans modifier la structure.
        """
        # Calculs i1_6 à t1_t2_eur_trim_4
        abs_ep = abs(self.elasticite_prix_marginal)
        df['i1_6'] = (abs_ep * df['Bi']) / (1 - abs_ep) * (
            (df['q_m3_jour'] ** (-(1 - abs_ep) / abs_ep)) - (df['conso_hrt_m3j_pp'] ** (-(1 - abs_ep) / abs_ep))
        )
        df['i2_6'] = self.cout_marginal_complet_cme * (df['conso_hrt_m3j_pp'] - df['q_m3_jour'])
        df['t1_6'] = df['i1_6']
        df['t2_6'] = -df['i2_6']
        df['t1_t2_eur_jour_3'] = df['t1_6'] + df['t2_6']

        df['i1_7'] = df['i1_6'] * 90
        df['i2_7'] = df['i2_6'] * 90
        df['t1_7'] = df['i1_7']
        df['t2_7'] = -df['i2_7']
        df['t1_t2_eur_trim_3'] = df['t1_7'] + df['t2_7']

        df['i1_8'] = (abs_ep * df['Bi']) / (1 - abs_ep) * (
            (df['q_m3_jour'] ** (-(1 - abs_ep) / abs_ep)) - (df['conso_hrt_m3j_mp'] ** (-(1 - abs_ep) / abs_ep))
        )
        df['i2_8'] = self.cout_marginal_complet_cme * (df['conso_hrt_m3j_mp'] - df['q_m3_jour'])
        df['t1_8'] = df['i1_8']
        df['t2_8'] = -df['i2_8']
        df['t1_t2_eur_jour_4'] = df['t1_8'] + df['t2_8']

        df['i1_9'] = df['i1_8'] * 90
        df['i2_9'] = df['i2_8'] * 90
        df['t1_9'] = df['i1_9']
        df['t2_9'] = -df['i2_9']
        df['t1_t2_eur_trim_4'] = df['t1_9'] + df['t2_9']

        # Calcul des abonnements
        df['abonnement_redev'] = self.prix_htva_ab_EPA
        df['abonnement_redev_jour'] = df['abonnement_redev'] / 90
        df['prix_redev_t1'] = self.prix_htva_t_EPA_T1
        df['prix_redev_t2'] = self.prix_htva_t_EPA_T2
        df['prix_redev_t3'] = self.prix_htva_t_EPA_T3
        df['prix_redev_t4'] = self.prix_htva_t_EPA_T4

        # Log et termes pour m3_jour_1_1 à m3_trim_4_1
        for i, t in enumerate(range(1, 5), start=1):
            df[f'terme_prix_{t}_1'] = self.elasticite_prix_marginal * np.log(df[f'prix_redev_t{t}'])
            df[f'terme_ln_ai_{t}_1'] = np.log(df['ai_m3_jour'])
            df[f'pv_{t}_somme_1'] = df[f'terme_prix_{t}_1'] + df[f'terme_ln_ai_{t}_1']
            df[f'm3_jour_{t}_1'] = np.exp(df[f'pv_{t}_somme_1'])
            df[f'm3_trim_{t}_1'] = df[f'm3_jour_{t}_1'] * 90

        # SI et SC pour les seuils
        df['si_1_1'] = (df['m3_trim_1_1'] < self.seuil_T_EPA_T4_bis).astype(int)
        df['sc_1_1'] = ((df['m3_trim_2_1'] < self.seuil_T_EPA_T4_bis) & (df['m3_trim_1_1'] > self.seuil_T_EPA_T4_bis)).astype(int) * (1 - df['si_1_1'])
        df['si_2_1'] = ((df['m3_trim_2_1'] > self.seuil_T_EPA_T4_bis) & (df['m3_trim_2_1'] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df['si_1_1']) * (1 - df['sc_1_1'])
        df['sc_2_1'] = ((df['m3_trim_2_1'] > self.seuil_T_EPA_T5_bis) & (df['m3_trim_3_1'] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df['si_1_1']) * (1 - df['sc_1_1']) * (1 - df['si_2_1'])
        df['si_3_1'] = ((df['m3_trim_3_1'] > self.seuil_T_EPA_T5_bis) & (df['m3_trim_3_1'] < self.seuil_T_EPA_T6)).astype(int) * (1 - df['si_1_1']) * (1 - df['sc_1_1']) * (1 - df['si_2_1']) * (1 - df['sc_2_1'])
        df['sc_3_1'] = ((df['m3_trim_3_1'] > self.seuil_T_EPA_T6) & (df['m3_trim_4_1'] < self.seuil_T_EPA_T6)).astype(int) * (1 - df['si_1_1']) * (1 - df['sc_1_1']) * (1 - df['si_2_1']) * (1 - df['sc_2_1']) * (1 - df['si_3_1']) * (1 - df['sc_2_1'])
        df['si_4_1'] = (df['m3_trim_4_1'] > self.seuil_T_EPA_T6).astype(int) * (1 - df['si_1_1']) * (1 - df['sc_1_1']) * (1 - df['si_2_1']) * (1 - df['sc_2_1']) * (1 - df['si_3_1']) * (1 - df['sc_3_1'])

        # Consommations sans TVA et mauvaise perception
        df['conso_sans_tva_val'] = df['si_1_1'] * df['m3_trim_1_1'] + df['sc_1_1'] * self.seuil_T_EPA_T4 + df['si_2_1'] * df['m3_trim_2_1'] + df['sc_2_1'] * self.seuil_T_EPA_T5 + df['si_3_1'] * df['m3_trim_3_1'] + df['sc_3_1'] * self.seuil_T_EPA_T6 + df['si_4_1'] * df['m3_trim_4_1']
        df['conso_sans_tva'] = 0
        df['conso_mauvaise_percep'] = df['conso_sans_tva_val'] + df['sur_conso_2']

        # Différences et variantes
        df['diff_ibt_redev_pct'] = ((df['conso_mauvaise_percep'] - df['c_ibt']) / df['c_ibt']) * 100
        df['conso_redev_m3j_pp'] = df['conso_sans_tva_val'] / 90
        df['conso_redev_m3j_mp'] = df['conso_mauvaise_percep'] / 90
        df['var_conso_redev_optq'] = df['conso_sans_tva_val'] - df['conso_q_cout_complet_m3_trim']
        df['var_conso_redev_mp_optq'] = df['conso_mauvaise_percep'] - df['conso_q_cout_complet_m3_trim']

        # Dummies
        df['dummy_1_a_conso_moins_1'] = (df['var_conso_redev_optq'] < 0).astype(int)
        df['dummy_1_b_conso_plus_1'] = (df['var_conso_redev_optq'] > 0).astype(int)
        df['dummy_1_c_conso_eq_1'] = (df['var_conso_redev_optq'] == 0).astype(int)
        df['dummy_1_d_conso_moins_1'] = (df['var_conso_redev_mp_optq'] < 0).astype(int)
        df['dummy_1_e_conso_plus_1'] = (df['var_conso_redev_mp_optq'] > 0).astype(int)
        df['dummy_1_f_conso_eq_1'] = (df['var_conso_redev_mp_optq'] == 0).astype(int)

        return df
    

    ########################################################################################

    def calculate_additional_rules_v2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remplit les colonnes du DataFrame selon les règles i1_10 → dummy_1_f_menage_egale_optimum,
        en utilisant les variables de classe pour les calculs.
        """
        abs_ep = abs(self.elasticite_prix_marginal)

        # -----------------------------
        # 1️⃣ Calculs i1_10 → t1_t2_eur_trim_6
        # -----------------------------
        df['i1_10'] = (abs_ep * df['Bi']) / (1 - abs_ep) * (
            df['q_m3_jour'] ** (-(1 - abs_ep) / abs_ep) - df['conso_redev_m3j_pp'] ** (-(1 - abs_ep) / abs_ep)
        )
        df['i2_10'] = self.cout_marginal_complet_cme * (df['conso_redev_m3j_pp'] - df['q_m3_jour'])
        df['t1_10'] = df['i1_10']
        df['t2_10'] = -df['i2_10']
        df['t1_t2_eur_jour_5'] = df['t1_10'] + df['t2_10']

        df['i1_11'] = df['i1_10'] * 90
        df['i2_11'] = df['i2_10'] * 90
        df['t1_11'] = df['i1_11']
        df['t2_11'] = -df['i2_11']
        df['t1_t2_eur_trim_5'] = df['t1_11'] + df['t2_11']

        df['i1_12'] = (abs_ep * df['Bi']) / (1 - abs_ep) * (
            df['q_m3_jour'] ** (-(1 - abs_ep) / abs_ep) - df['conso_redev_m3j_mp'] ** (-(1 - abs_ep) / abs_ep)
        )
        df['i2_12'] = self.cout_marginal_complet_cme * (df['conso_redev_m3j_mp'] - df['q_m3_jour'])
        df['t1_12'] = df['i1_12']
        df['t2_12'] = -df['i2_12']
        df['t1_t2_eur_jour_6'] = df['t1_12'] + df['t2_12']

        df['i1_13'] = df['i1_12'] * 90
        df['i2_13'] = df['i2_12'] * 90
        df['t1_13'] = df['i1_13']
        df['t2_13'] = -df['i2_13']
        df['t1_t2_eur_trim_6'] = df['t1_13'] + df['t2_13']

        # -----------------------------
        # 2️⃣ Abonnements TTC et prix TTC
        # -----------------------------
        df['abonnement_ttc'] = self.prix_ttc_a_EPA
        df['abonnement_ttc_jour'] = df['abonnement_ttc'] / 90
        df['prix_ttc_t1'] = self.prix_ttc_T_EPA_T1
        df['prix_ttc_t2'] = self.prix_ttc_T_EPA_T2
        df['prix_ttc_t3'] = self.prix_ttc_T_EPA_T3
        df['prix_ttc_t4'] = self.prix_ttc_T_EPA_T4

        # Termes prix / ln_ai / pv / m3_jour / m3_trim
        for t in range(1, 5):
            df[f'prix_{t}'] = self.elasticite_prix_marginal * np.log(df[f'prix_ttc_t{t}'])
            df[f'ln_ai_{t}'] = np.log(df['ai_m3_jour'])
            df[f'pv_{t}'] = df[f'prix_{t}'] + df[f'ln_ai_{t}']
            df[f'm3_jour_{t}_2'] = np.exp(df[f'pv_{t}'])
            df[f'm3_trim_{t}_2'] = df[f'm3_jour_{t}_2'] * 90

        # -----------------------------
        # 3️⃣ SI / SC pour seuils EPA bis
        # -----------------------------
        df['si_1_2'] = (df['m3_trim_1_2'] < self.seuil_T_EPA_T4_bis).astype(int)
        df['sc_1_2'] = ((df['m3_trim_2_2'] < self.seuil_T_EPA_T4_bis) & (df['m3_trim_1_2'] > self.seuil_T_EPA_T4_bis)).astype(int) * (1 - df['si_1_2'])
        df['si_2_2'] = ((df['m3_trim_2_2'] > self.seuil_T_EPA_T4_bis) & (df['m3_trim_2_2'] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df['si_1_2']) * (1 - df['sc_1_2'])
        df['sc_2_2'] = ((df['m3_trim_2_2'] > self.seuil_T_EPA_T5_bis) & (df['m3_trim_3_2'] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df['si_1_2']) * (1 - df['sc_1_2']) * (1 - df['si_2_2'])
        df['si_3_2'] = ((df['m3_trim_3_2'] > self.seuil_T_EPA_T5_bis) & (df['m3_trim_3_2'] < self.seuil_T_EPA_T6_bis)).astype(int) * (1 - df['si_1_2']) * (1 - df['sc_1_2']) * (1 - df['si_2_2']) * (1 - df['sc_2_2'])
        df['sc_3_2'] = ((df['m3_trim_3_2'] > self.seuil_T_EPA_T6_bis) & (df['m3_trim_4_2'] < self.seuil_T_EPA_T6_bis)).astype(int) * (1 - df['si_1_2']) * (1 - df['sc_1_2']) * (1 - df['si_2_2']) * (1 - df['sc_2_2']) * (1 - df['si_3_2']) * (1 - df['sc_2_2'])
        df['si_4_2'] = (df['m3_trim_4_2'] > self.seuil_T_EPA_T6_bis).astype(int) * (1 - df['si_1_2']) * (1 - df['sc_1_2']) * (1 - df['si_2_2']) * (1 - df['sc_2_2']) * (1 - df['si_3_2']) * (1 - df['sc_3_2'])

        # -----------------------------
        # 4️⃣ Consommations
        # -----------------------------
        df['conso_tva'] = 0
        df['conso_tva_val'] = (
            df['si_1_2'] * df['m3_trim_1_2'] +
            df['sc_1_2'] * self.seuil_T_EPA_T4 +
            df['si_2_2'] * df['m3_trim_2_2'] +
            df['sc_2_2'] * self.seuil_T_EPA_T5 +
            df['si_3_2'] * df['m3_trim_3_2'] +
            df['sc_3_2'] * self.seuil_T_EPA_T6 +
            df['si_4_2'] * df['m3_trim_4_2']
        )
        df['conso_mauvaise'] = df['conso_tva_val'] + df['surconso']

        # -----------------------------
        # 5️⃣ Différences, effets et dummies
        # -----------------------------
        df['diff_ib_t_pct'] = ((df['conso_mauvaise'] - df['c_ibt']) / df['c_ibt']) * 100
        df['conso_ttc_m3_jour_pp'] = df['conso_tva_val'] / 90
        df['conso_ttc_m3_jour_mp'] = df['conso_mauvaise'] / 90
        df['q_star_consommation_rang1'] = df['conso_q_cout_complet_m3_trim']
        df['consommation_hrt'] = df['conso_hrt_m3_trim_val']
        df['conso_hrt_mauvaise_perception'] = df['conso_mauvaise_percep_m3_trim']

        df['variation_conso_ttc_optimum_q_star'] = df['conso_tva_val'] - df['q_star_consommation_rang1']
        df['variation_conso_ttc_mp_optimum_q_star'] = df['conso_mauvaise'] - df['q_star_consommation_rang1']
        df['variation_conso_hrt_q_star'] = df['consommation_hrt'] - df['q_star_consommation_rang1']
        df['variation_conso_hrt_mp_q_star'] = df['conso_hrt_mauvaise_perception'] - df['q_star_consommation_rang1']

        df['effet_redevance'] = df['consommation_redevance_sans_tva'] - df['consommation_hrt']
        df['effet_tva'] = df['conso_tva_val'] - df['consommation_redevance_sans_tva']

        # Dummies
        df['dummy_1_a_menage_inf_optimum'] = (df['variation_conso_ttc_optimum_q_star'] < 0).astype(int)
        df['dummy_1_b_menage_sup_optimum'] = (df['variation_conso_ttc_optimum_q_star'] > 0).astype(int)
        df['dummy_1_c_conso_egale_optimum'] = (df['variation_conso_ttc_optimum_q_star'] == 0).astype(int)
        df['dummy_1_d_menage_inf_optimum'] = (df['variation_conso_ttc_mp_optimum_q_star'] < 0).astype(int)
        df['dummy_1_e_menage_sup_optimum'] = (df['variation_conso_ttc_mp_optimum_q_star'] > 0).astype(int)
        df['dummy_1_f_conso_egale_optimum'] = (df['variation_conso_ttc_mp_optimum_q_star'] == 0).astype(int)

        return df


    def KQ(self, df):
        df = df.copy()
        df['c_captive_jour'] = df['c_m3_trim'] / 90
        df['c_nordin_jour'] = df['consom_nordin_trim'] / 90
        df['c_taylor_jour'] = df['consom_taylor_trim'] / 90
        df['ln_c_captive_jour'] = np.log(df['c_m3_trim'])
        df['ln_c_nordin_jour'] = np.log(df['c_nordin_jour'])
        df['ln_c_taylor_j'] = np.log(df['c_taylor_jour'])
        df['sur_conso_pct'] = 100 * (df['ln_c_taylor_j'] - df['ln_c_nordin_jour'])
        return df

    

    def SU(self, df):
        df = df.copy()
        df['ai_m3_jour'] = (df['c_m3_trim'] / 90) * ((df['revenu_net_mois'] / 30) ** self.elasticite_revenu_virtuel)
        df['q_m3_jour'] = df['ai_m3_jour'] / (self.cout_marginal_complet_cme ** abs(self.elasticite_prix_marginal))
        df['conso_q_cout_complet_m3_trim'] = df['q_m3_jour'] * 90
        return df

   

    def calc_Bi(self, df):
        df = df.copy()
        df['Bi'] = df['ai_m3_jour'] ** (1 / abs(self.elasticite_prix_marginal))
        return df
    

    def calc_i1_i2_t1_t2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les variables ln_qb, qb_m3_jour, qb_m3_trim, i1, i2, t1, t2 et t1_t2_eur_jour.
        """

        try:
            # ln_qb
            df["ln_qb"] = (
                np.log(df["c_m3_trim"] / 90)
                + (self.elasticite_revenu_virtuel * np.log(df["revenu_net_mois"] / 30))
                - (abs(self.elasticite_prix_marginal) * np.log(self.prix_pi))
            )

            # qb_m3_jour et qb_m3_trim
            df["qb_m3_jour"] = np.exp(df["ln_qb"])
            df["qb_m3_trim"] = df["qb_m3_jour"] * 90

            # i1
            expo = (1 - abs(self.elasticite_prix_marginal)) / abs(self.elasticite_prix_marginal)
            df["i1"] = (
                (abs(self.elasticite_prix_marginal) * df["Bi"])
                / (1 - abs(self.elasticite_prix_marginal))
                * (
                    (df["q_m3_jour"] ** -expo)
                    - (df["qb_m3_jour"] ** -expo)
                )
            )

            # i2
            df["i2"] = self.cout_marginal_complet_cme * (df["qb_m3_jour"] - df["q_m3_jour"])

            # t1, t2
            df["t1"] = df["i1"]
            df["t2"] = -df["i2"]

            # Somme t1+t2
            df["t1_t2_eur_jour"] = df["t1"] + df["t2"]

            return df

        except Exception as e:
            print(f"❌ Erreur dans calc_i1_i2_t1_t2: {e}")
            return df
        

    def calc_AHAM(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ajoute les colonnes dérivées i1_1, i2_1, t1_1, t2_1, t1_t2_eur_trim et diff_qb_tbse_pct
        en suivant les formules Excel (AH16 → AM16).
        """
        try:
            # i1_1 = AB16 * 90   => I1*90
            df["i1_1"] = df["i1"] * 90

            # i2_1 = AC16 * 90   => I2*90
            df["i2_1"] = df["i2"] * 90

            # t1_1 = AH16        => i1_1
            df["t1_1"] = df["i1_1"]

            # t2_1 = -AI16       => -i2_1
            df["t2_1"] = -df["i2_1"]

            # t1_t2_eur_trim = AJ16+AK16 => t1_1+t2_1
            df["t1_t2_eur_trim"] = df["t1_1"] + df["t2_1"]

            # diff_qb_tbse_pct = ((AA16-H16)/H16)*100 => ((qb_m3_trim - c_tbse)/c_tbse)*100
            df["diff_qb_tbse_pct"] = ((df["qb_m3_trim"] - df["c_tbse"]) / df["c_tbse"]) * 100

            return df

        except KeyError as e:
            print(f"❌ Erreur lors du calcul des colonnes dérivées: {e}")
            return df


    def calc_AOAV(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour le DataFrame avec les colonnes dérivées liées aux redevances (AOAV).
        """

        abs_e = abs(self.elasticite_prix_marginal)
        pi_redev = self.prix_pi + self.redevances_accise_euro_m3

        # ln_qb_redev
        df["ln_qb_redev"] = (
            np.log(df["c_m3_trim"] / 90)
            + (self.elasticite_revenu_virtuel * np.log(df["revenu_net_mois"] / 30))
            - (abs_e * np.log(pi_redev))
        )

        # qb_m3_jour_1
        df["qb_m3_jour_1"] = np.exp(df["ln_qb_redev"])

        # qb_redev_sans_tva
        df["qb_redev_sans_tva"] = df["qb_m3_jour_1"] * 90

        # i1_2
        df["i1_2"] = (
            (abs_e * df["Bi"]) / (1 - abs_e)
            * (
                (df["q_m3_jour"] ** (-(1 - abs_e) / abs_e))
                - (df["qb_m3_jour_1"] ** (-(1 - abs_e) / abs_e))
            )
        )

        # i2_2
        df["i2_2"] = self.cout_marginal_complet_cme * (df["qb_m3_jour_1"] - df["q_m3_jour"])

        # t1_2 et t2_2
        df["t1_2"] = df["i1_2"]
        df["t2_2"] = -df["i2_2"]

        # t1_t2_eur_jour_1
        df["t1_t2_eur_jour_1"] = df["t1_2"] + df["t2_2"]

        return df
    
    def AXBC(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les intégrales trimestrielles pour le scénario redevances
        et les différences avec TBSE.
        
        Champs calculés :
            - i1_3, i2_3, t1_3, t2_3, t1_t2_eur_trim_1, diff_qb_redev_tbse_pct
        """
        df = df.copy()
        
        # Calculs des intégrales trimestrielles
        df['i1_3'] = df['i1_2'] * 90
        df['i2_3'] = df['i2_2'] * 90
        df['t1_3'] = df['i1_3']
        df['t2_3'] = -df['i2_3']
        df['t1_t2_eur_trim_1'] = df['t1_3'] + df['t2_3']
        
        # Différence redevances avec TBSE
        df['diff_qb_redev_tbse_pct'] = ((df['qb_redev_sans_tva'] - df['c_tbse']) / df['c_tbse']) * 100
        
        return df
    

    def calc_BEBL(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les colonnes pour le scénario TTC.

        Champs calculés :
            ln_qb_ttc, qb_m3_jour_2, qb_ttc
            i1_4, i2_4, t1_4, t2_4, t1_t2_eur_jour_2

        Args:
            df (pd.DataFrame): DataFrame contenant les colonnes nécessaires

        Returns:
            pd.DataFrame: DataFrame avec les colonnes mises à jour
        """
        df = df.copy()

        elasticite_abs = abs(self.elasticite_prix_marginal)

        # ln_qb_ttc
        df['ln_qb_ttc'] = (
            np.log(df['c_m3_trim'] / 90) +
            (self.elasticite_revenu_virtuel * np.log(df['revenu_net_mois'] / 30)) -
            (elasticite_abs * np.log(self.tbse_epa_prix_ttc))
        )

        # Quantités
        df['qb_m3_jour_2'] = np.exp(df['ln_qb_ttc'])
        df['qb_ttc'] = df['qb_m3_jour_2'] * 90

        # Intégrales et surplus
        exposant = -((1 - elasticite_abs) / elasticite_abs)
        df['i1_4'] = (elasticite_abs * df['Bi']) / (1 - elasticite_abs) * (
            (df['q_m3_jour'] ** exposant) - (df['qb_m3_jour_2'] ** exposant)
        )
        df['i2_4'] = self.cout_marginal_complet_cme * (df['qb_m3_jour_2'] - df['q_m3_jour'])
        df['t1_4'] = df['i1_4']
        df['t2_4'] = -df['i2_4']
        df['t1_t2_eur_jour_2'] = df['t1_4'] + df['t2_4']

        return df
    

    ##### calc_BNBS


    def calc_BNBS(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcul des champs i1_5, i2_5, t1_5, t2_5, t1_t2_eur_trim_2, diff_qb_ttc_tbse_pct
        à partir des colonnes précédemment calculées.
        """
        import numpy as np

        # i1_5 = i1_4 * 90
        df['i1_5'] = df['i1_4'] * 90

        # i2_5 = i2_4 * 90
        df['i2_5'] = df['i2_4'] * 90

        # t1_5 = i1_5
        df['t1_5'] = df['i1_5']

        # t2_5 = -i2_5
        df['t2_5'] = -df['i2_5']

        # t1_t2_eur_trim_2 = t1_5 + t2_5
        df['t1_t2_eur_trim_2'] = df['t1_5'] + df['t2_5']

        # diff_qb_ttc_tbse_pct = ((qb_ttc - c_tbse) / c_tbse) * 100
        df['diff_qb_ttc_tbse_pct'] = ((df['qb_ttc'] - df['c_tbse']) / df['c_tbse']) * 100

        return df
    
    def calc_BWBX(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les champs abonnement_ht et abonnement_ht_jour.
        
        abonnement_ht        : Prix HT abonnement EPA
        abonnement_ht_jour   : abonnement HT divisé par 90 (par jour)
        """
        # Ajouter colonne abonnement_ht avec la valeur constante prix_ht_op_a_EPA
        df["abonnement_ht"] = self.prix_ht_op_a_EPA
        
        # Calcul de l'abonnement par jour
        df["abonnement_ht_jour"] = df["abonnement_ht"] / 90
        
        return df

    def calcBZCC(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les champs prix_ht_t1 à prix_ht_t4 avec les prix HT EPA correspondants.
        """
        df["prix_ht_t1"] = self.prix_ht_op_T_EPA_T1
        df["prix_ht_t2"] = self.prix_ht_op_T_EPA_T2
        df["prix_ht_t3"] = self.prix_ht_op_T_EPA_T3
        df["prix_ht_t4"] = self.prix_ht_op_T_EPA_T4
    
        return df
    

    def calc_CECP(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les colonnes terme_prix_X, terme_ln_ai_X et pv_X_somme pour X=1 à 4 (sans boucle)
        """
        # Terme prix
        df["terme_prix_1"] = self.elasticite_prix_marginal * np.log(df["prix_ht_t1"])
        df["terme_prix_2"] = self.elasticite_prix_marginal * np.log(df["prix_ht_t2"])
        df["terme_prix_3"] = self.elasticite_prix_marginal * np.log(df["prix_ht_t3"])
        df["terme_prix_4"] = self.elasticite_prix_marginal * np.log(df["prix_ht_t4"])

        # Terme ln(ai_m3_jour) (identique pour les 4 périodes)
        df["terme_ln_ai_1"] = np.log(df["ai_m3_jour"])
        df["terme_ln_ai_2"] = np.log(df["ai_m3_jour"])
        df["terme_ln_ai_3"] = np.log(df["ai_m3_jour"])
        df["terme_ln_ai_4"] = np.log(df["ai_m3_jour"])

        # Somme des deux
        df["pv_1_somme"] = df["terme_prix_1"] + df["terme_ln_ai_1"]
        df["pv_2_somme"] = df["terme_prix_2"] + df["terme_ln_ai_2"]
        df["pv_3_somme"] = df["terme_prix_3"] + df["terme_ln_ai_3"]
        df["pv_4_somme"] = df["terme_prix_4"] + df["terme_ln_ai_4"]

        return df
    

    def calc_CRCY(self, df):
        """
        Met à jour les champs m3_jour_x et m3_trim_x 
        à partir de pv_x_somme pour chaque trimestre (1 à 4), sans boucle.
        """
        df["m3_jour_1"] = np.exp(df["pv_1_somme"])
        df["m3_trim_1"] = df["m3_jour_1"] * 90

        df["m3_jour_2"] = np.exp(df["pv_2_somme"])
        df["m3_trim_2"] = df["m3_jour_2"] * 90

        df["m3_jour_3"] = np.exp(df["pv_3_somme"])
        df["m3_trim_3"] = df["m3_jour_3"] * 90

        df["m3_jour_4"] = np.exp(df["pv_4_somme"])
        df["m3_trim_4"] = df["m3_jour_4"] * 90

        return df
    
    #### DDDT
    def calc_DADL(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les colonnes liées aux seuils et à la consommation HRT/mauvaise perception :
        - si_1, sc_1, si_2, sc_2, si_3, sc_3, si_4
        - conso_hrt_m3_trim, conso_hrt_m3_trim_val
        - conso_mauvaise_percep_m3_trim, diff_ibt_ht_pct
        """

        # si_1
        df["si_1"] = np.where(df["m3_trim_1"] < self.seuil_T_EPA_T4_bis, 1, 0)

        # sc_1
        df["sc_1"] = np.where(
            (df["m3_trim_2"] < self.seuil_T_EPA_T4_bis) & (df["m3_trim_1"] > self.seuil_T_EPA_T4_bis),
            1, 0
        ) * (1 - df["si_1"])

        # si_2
        df["si_2"] = np.where(
            (df["m3_trim_2"] > self.seuil_T_EPA_T4_bis) & (df["m3_trim_2"] < self.seuil_T_EPA_T5_bis),
            1, 0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"])

        # sc_2
        df["sc_2"] = np.where(
            (df["m3_trim_2"] > self.seuil_T_EPA_T5_bis) & (df["m3_trim_3"] < self.seuil_T_EPA_T5_bis),
            1, 0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"])

        # si_3
        df["si_3"] = np.where(
            (df["m3_trim_3"] > self.seuil_T_EPA_T5_bis) & (df["m3_trim_3"] < self.seuil_T_EPA_T6_bis),
            1, 0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"])

        # sc_3
        df["sc_3"] = np.where(
            (df["m3_trim_3"] > self.seuil_T_EPA_T6_bis) & (df["m3_trim_4"] < self.seuil_T_EPA_T6_bis),
            1, 0
        ) * (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"]) * (1 - df["si_3"])

        # si_4
        df["si_4"] = np.where(df["m3_trim_4"] > self.seuil_T_EPA_T6_bis, 1, 0) * \
            (1 - df["si_1"]) * (1 - df["sc_1"]) * (1 - df["si_2"]) * (1 - df["sc_2"]) * (1 - df["si_3"]) * (1 - df["sc_3"])

        # conso HRT
        df["conso_hrt_m3_trim"] = 0

        df["conso_hrt_m3_trim_val"] = (
            df["si_1"] * df["m3_trim_1"] +
            df["sc_1"] * self.seuil_T_EPA_T4 +
            df["si_2"] * df["m3_trim_2"] +
            df["sc_2"] * self.seuil_T_EPA_T5 +
            df["si_3"] * df["m3_trim_3"] +
            df["sc_3"] * self.seuil_T_EPA_T6 +
            df["si_4"] * df["m3_trim_4"]
        )

        # conso mauvaise perception
        df["conso_mauvaise_percep_m3_trim"] = df["conso_hrt_m3_trim_val"] + df["sur_conso_1"]

        # diff IBT HT
        df["diff_ibt_ht_pct"] = ((df["conso_mauvaise_percep_m3_trim"] - df["c_ibt_pp"]) / df["c_ibt_pp"]) * 100

        return df
    
    def calc_DNDO(self, df):
        """
        Calcule les consommations HRT journalières à partir des valeurs trimestrielles.
        """
        df["conso_hrt_m3j_pp"] = df["conso_hrt_m3_trim_val"] / 90
        df["conso_hrt_m3j_mp"] = df["conso_mauvaise_percep_m3_trim"] / 90
        return df
    

    def calc_DQDX(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les champs dérivés :
            - var_conso_hrt_optq
            - var_conso_hrt_mp_optq
            - dummy_1_a_conso_moins
            - dummy_1_b_conso_plus
            - dummy_1_c_conso_eq
            - dummy_1_d_conso_moins
            - dummy_1_e_conso_plus
            - dummy_1_f_conso_eq
        """
        df = df.copy()  # Pour éviter de modifier l'original

        # Calcul des variations
        df["var_conso_hrt_optq"] = df["conso_hrt_m3_trim_val"] - df["conso_q_cout_complet_m3_trim"]
        df["var_conso_hrt_mp_optq"] = df["conso_mauvaise_percep_m3_trim"] - df["conso_q_cout_complet_m3_trim"]

        # Dummy pour var_conso_hrt_optq
        df["dummy_1_a_conso_moins"] = np.where(df["var_conso_hrt_optq"] < 0, 1, 0)
        df["dummy_1_b_conso_plus"] = np.where(df["var_conso_hrt_optq"] > 0, 1, 0)
        df["dummy_1_c_conso_eq"] = np.where(df["var_conso_hrt_optq"] == 0, 1, 0)

        # Dummy pour var_conso_hrt_mp_optq
        df["dummy_1_d_conso_moins"] = np.where(df["var_conso_hrt_mp_optq"] < 0, 1, 0)
        df["dummy_1_e_conso_plus"] = np.where(df["var_conso_hrt_mp_optq"] > 0, 1, 0)
        df["dummy_1_f_conso_eq"] = np.where(df["var_conso_hrt_mp_optq"] == 0, 1, 0)

        return df
    


    def calc_DZED(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_6
            - i2_6
            - t1_6
            - t2_6
            - t1_t2_eur_jour_3
        """
        df = df.copy()

        # Sécurisation numérique
        epsilon = 1e-12  

        # Variables intermédiaires
        e = abs(self.elasticite_prix_marginal)
        Bi = df["Bi"]
        q = df["q_m3_jour"].clip(lower=epsilon)
        conso = df["conso_hrt_m3j_pp"].clip(lower=epsilon)

        # Éviter division par zéro (cas e = 1)
        if np.isclose(e, 1.0):
            df["i1_6"] = np.nan
        else:
            exponent = -(1 - e) / e
            df["i1_6"] = (e * Bi) / (1 - e) * (
                np.power(q, exponent) - np.power(conso, exponent)
            )

        # i2_6 = cout_marginal_complet_cme * (conso - q)
        df["i2_6"] = self.cout_marginal_complet_cme * (conso - q)

        # t1_6 = i1_6
        df["t1_6"] = df["i1_6"]

        # t2_6 = -i2_6
        df["t2_6"] = -df["i2_6"]

        # t1_t2_eur_jour_3 = t1_6 + t2_6
        df["t1_t2_eur_jour_3"] = df["t1_6"] + df["t2_6"]

        return df
    

    def calc_EFEJ(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_7 = i1_6 * 90
            - i2_7 = i2_6 * 90
            - t1_7 = i1_7
            - t2_7 = -i2_7
            - t1_t2_eur_trim_3 = t1_7 + t2_7
        """
        df = df.copy()

        # Calculs principaux
        df["i1_7"] = df["i1_6"] * 90
        df["i2_7"] = df["i2_6"] * 90
        df["t1_7"] = df["i1_7"]
        df["t2_7"] = -df["i2_7"]
        df["t1_t2_eur_trim_3"] = df["t1_7"] + df["t2_7"]

        return df
    
    def calc_ELEP(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_8 = (|elasticite_prix_marginal| * Bi) / (1 - |elasticite_prix_marginal|) *
                    ( q_m3_jour^(-(1-|e|)/|e|) - conso_hrt_m3j_mp^(-(1-|e|)/|e|) )
            - i2_8 = cout_marginal_complet_cme * (conso_hrt_m3j_mp - q_m3_jour)
            - t1_8 = i1_8
            - t2_8 = -i2_8
            - t1_t2_eur_jour_4 = t1_8 + t2_8
        """
        df = df.copy()

        # Variables intermédiaires
        e = abs(self.elasticite_prix_marginal)
        Bi = df["Bi"]
        q = df["q_m3_jour"]
        conso_mp = df["conso_hrt_m3j_mp"]

        # i1_8 : calcul principal
        exponent = -((1 - e) / e)
        df["i1_8"] = (e * Bi) / (1 - e) * (np.power(q, exponent) - np.power(conso_mp, exponent))

        # i2_8 : coût marginal complet
        df["i2_8"] = self.cout_marginal_complet_cme * (conso_mp - q)

        # t1_8 = i1_8
        df["t1_8"] = df["i1_8"]

        # t2_8 = -i2_8
        df["t2_8"] = -df["i2_8"]

        # t1_t2_eur_jour_4 = t1_8 + t2_8
        df["t1_t2_eur_jour_4"] = df["t1_8"] + df["t2_8"]

        return df
    

    def calc_ELER(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_9 = i1_8 * 90
            - i2_9 = i2_8 * 90
            - t1_9 = i1_9
            - t2_9 = -i2_9
            - t1_t2_eur_trim_4 = t1_9 + t2_9
        """
        df = df.copy()

        # Calculs principaux
        df["i1_9"] = df["i1_8"] * 90
        df["i2_9"] = df["i2_8"] * 90

        # Mise à jour des t1/t2 et somme
        df["t1_9"] = df["i1_9"]
        df["t2_9"] = -df["i2_9"]
        df["t1_t2_eur_trim_4"] = df["t1_9"] + df["t2_9"]

        return df
    
    def calc_EZFA(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs liés à l'abonnement :
            - abonnement_redev = prix_htva_ab_EPA
            - abonnement_redev_jour = abonnement_redev / 90
        """
        df = df.copy()

        # Calcul principal
        df["abonnement_redev"] = self.prix_htva_ab_EPA
        df["abonnement_redev_jour"] = df["abonnement_redev"] / 90

        return df


    
    def calc_PRIX_FCFF(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs des prix de redevance :
            - prix_redev_t1 = prix_htva_t_EPA_T1
            - prix_redev_t2 = prix_htva_t_EPA_T2
            - prix_redev_t3 = prix_htva_t_EPA_T3
            - prix_redev_t4 = prix_htva_t_EPA_T4
        """
        df = df.copy()

        df["prix_redev_t1"] = self.prix_htva_t_EPA_T1
        df["prix_redev_t2"] = self.prix_htva_t_EPA_T2
        df["prix_redev_t3"] = self.prix_htva_t_EPA_T3
        df["prix_redev_t4"] = self.prix_htva_t_EPA_T4

        return df

    def calc_FHFF(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs suivants :
            - terme_prix_X_1 = elasticite_prix_marginal * LN(prix_redev_tX)
            - terme_ln_ai_X_1 = LN(ai_m3_jour)
            - pv_X_somme_1 = terme_prix_X_1 + terme_ln_ai_X_1
        pour X = 1 à 4
        """
        df = df.copy()

        # Vérification que les colonnes nécessaires existent
        prix_cols = ["prix_redev_t1", "prix_redev_t2", "prix_redev_t3", "prix_redev_t4"]
        for i, col in enumerate(prix_cols, start=1):
            df[f"terme_prix_{i}_1"] = self.elasticite_prix_marginal * np.log(df[col])
            df[f"terme_ln_ai_{i}_1"] = np.log(df["ai_m3_jour"])
            df[f"pv_{i}_somme_1"] = df[f"terme_prix_{i}_1"] + df[f"terme_ln_ai_{i}_1"]

        return df
    
    def calc_FUGB(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs journaliers et trimestriels m3_jour_X_1 et m3_trim_X_1
        à partir des colonnes pv_X_somme_1 (X = 1 à 4)
        """
        df = df.copy()

        for i in range(1, 5):
            # m3_jour_X_1 = EXP(pv_X_somme_1)
            df[f"m3_jour_{i}_1"] = np.exp(df[f"pv_{i}_somme_1"])
            # m3_trim_X_1 = m3_jour_X_1 * 90
            df[f"m3_trim_{i}_1"] = df[f"m3_jour_{i}_1"] * 90

        return df
    
    def calc_GDGO(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les indicateurs si_X_1, sc_X_1 et les consommations finales :
            - si_1_1, sc_1_1, si_2_1, sc_2_1, si_3_1, sc_3_1, si_4_1
            - conso_sans_tva, conso_sans_tva_val, conso_mauvaise_percep, diff_ibt_redev_pct
        """
        df = df.copy()

        # SI et ET convertis en pandas
        df["si_1_1"] = (df["m3_trim_1_1"] < self.seuil_T_EPA_T4_bis).astype(int)

        df["sc_1_1"] = ((df["m3_trim_2_1"] < self.seuil_T_EPA_T4_bis) & 
                        (df["m3_trim_1_1"] > self.seuil_T_EPA_T4_bis)).astype(int) * (1 - df["si_1_1"])

        df["si_2_1"] = ((df["m3_trim_2_1"] > self.seuil_T_EPA_T4_bis) &
                        (df["m3_trim_2_1"] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df["si_1_1"]) * (1 - df["sc_1_1"])

        df["sc_2_1"] = ((df["m3_trim_2_1"] > self.seuil_T_EPA_T5_bis) &
                        (df["m3_trim_3_1"] < self.seuil_T_EPA_T5_bis)).astype(int) * \
                    (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"])

        df["si_3_1"] = ((df["m3_trim_3_1"] > self.seuil_T_EPA_T5_bis) &
                        (df["m3_trim_3_1"] < self.seuil_T_EPA_T6_bis)).astype(int) * \
                    (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"]) * (1 - df["sc_2_1"])

        df["sc_3_1"] = ((df["m3_trim_3_1"] > self.seuil_T_EPA_T6_bis) &
                        (df["m3_trim_4_1"] < self.seuil_T_EPA_T6_bis)).astype(int) * \
                    (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"]) * (1 - df["sc_2_1"]) * \
                    (1 - df["si_3_1"]) * (1 - df["sc_2_1"])

        df["si_4_1"] = (df["m3_trim_4_1"] > self.seuil_T_EPA_T6_bis).astype(int) * \
                    (1 - df["si_1_1"]) * (1 - df["sc_1_1"]) * (1 - df["si_2_1"]) * (1 - df["sc_2_1"]) * \
                    (1 - df["si_3_1"]) * (1 - df["sc_3_1"])

        # Consommation sans TVA
        df["conso_sans_tva"] = 0
        df["conso_sans_tva_val"] = (
            df["si_1_1"] * df["m3_trim_1_1"] +
            df["sc_1_1"] * self.seuil_T_EPA_T4_bis +
            df["si_2_1"] * df["m3_trim_2_1"] +
            df["sc_2_1"] * self.seuil_T_EPA_T5_bis +
            df["si_3_1"] * df["m3_trim_3_1"] +
            df["sc_3_1"] * self.seuil_T_EPA_T6_bis +
            df["si_4_1"] * df["m3_trim_4_1"]
        )

        # Consommation avec mauvaise perception
        df["conso_mauvaise_percep"] = df["conso_sans_tva_val"] + df["sur_conso_2"]

        # Différence IBT / redevance %
        df["diff_ibt_redev_pct"] = ((df["conso_mauvaise_percep"] - df["c_ibt"]) / df["c_ibt"]) * 100

        return df
    

    def calc_GQGR(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les consommations journalières :
            - conso_redev_m3j_pp = conso_sans_tva_val / 90
            - conso_redev_m3j_mp = conso_mauvaise_percep / 90
        """
        df = df.copy()

        df["conso_redev_m3j_pp"] = df["conso_sans_tva_val"] / 90
        df["conso_redev_m3j_mp"] = df["conso_mauvaise_percep"] / 90

        return df


    def calc_GTHA(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - var_conso_redev_optq
            - var_conso_redev_mp_optq
            - dummy_1_a_conso_moins_1
            - dummy_1_b_conso_plus_1
            - dummy_1_c_conso_eq_1
            - dummy_1_d_conso_moins_1
            - dummy_1_e_conso_plus_1
            - dummy_1_f_conso_eq_1
        selon les formules :
            var_conso_redev_optq = conso_sans_tva_val - conso_q_cout_complet_m3_trim
            var_conso_redev_mp_optq = conso_mauvaise_percep - conso_q_cout_complet_m3_trim
            dummy_* = 1 si condition vraie, sinon 0
        """
        df = df.copy()

        # Variables intermédiaires
        df["var_conso_redev_optq"] = (
            df["conso_sans_tva_val"] - df["conso_q_cout_complet_m3_trim"]
        )
        df["var_conso_redev_mp_optq"] = (
            df["conso_mauvaise_percep"] - df["conso_q_cout_complet_m3_trim"]
        )

        # Dummies pour var_conso_redev_optq
        df["dummy_1_a_conso_moins_1"] = (df["var_conso_redev_optq"] < 0).astype(int)
        df["dummy_1_b_conso_plus_1"] = (df["var_conso_redev_optq"] > 0).astype(int)
        df["dummy_1_c_conso_eq_1"] = (df["var_conso_redev_optq"] == 0).astype(int)

        # Dummies pour var_conso_redev_mp_optq
        df["dummy_1_d_conso_moins_1"] = (df["var_conso_redev_mp_optq"] < 0).astype(int)
        df["dummy_1_e_conso_plus_1"] = (df["var_conso_redev_mp_optq"] > 0).astype(int)
        df["dummy_1_f_conso_eq_1"] = (df["var_conso_redev_mp_optq"] == 0).astype(int)

        return df
    



    def calc_HCHG(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_10
            - i2_10
            - t1_10
            - t2_10
            - t1_t2_eur_jour_5
        selon les formules :
            i1_10 = (|e| * Bi) / (1 - |e|) * ( q^-((1-|e|)/|e|) - conso^-((1-|e|)/|e|) )
            i2_10 = cout_marginal_complet_cme * (conso - q)
            t1_10 = i1_10
            t2_10 = -i2_10
            t1_t2_eur_jour_5 = t1_10 + t2_10
        """
        df = df.copy()

        # Sécurisation numérique pour éviter division par zéro et puissances sur zéro
        epsilon = 1e-12

        # Variables intermédiaires
        e = abs(self.elasticite_prix_marginal)
        Bi = df["Bi"]
        q = df["q_m3_jour"].clip(lower=epsilon)
        conso = df["conso_redev_m3j_pp"].clip(lower=epsilon)

        # Calcul de i1_10
        if np.isclose(e, 1.0):
            df["i1_10"] = np.nan
        else:
            exponent = -(1 - e) / e
            df["i1_10"] = (e * Bi) / (1 - e) * (np.power(q, exponent) - np.power(conso, exponent))

        # Calcul de i2_10
        df["i2_10"] = self.cout_marginal_complet_cme * (conso - q)

        # Calcul t1_10 et t2_10
        df["t1_10"] = df["i1_10"]
        df["t2_10"] = -df["i2_10"]

        # Somme t1 + t2
        df["t1_t2_eur_jour_5"] = df["t1_10"] + df["t2_10"]

        return df
    

    def calc_HIHM(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs trimestriels à partir des colonnes i1_10 et i2_10 :
            - i1_11 = i1_10 * 90
            - i2_11 = i2_10 * 90
            - t1_11 = i1_11
            - t2_11 = -i2_11
            - t1_t2_eur_trim_5 = t1_11 + t2_11
        """
        df = df.copy()

        # Calcul des valeurs trimestrielles
        df["i1_11"] = df["i1_10"] * 90
        df["i2_11"] = df["i2_10"] * 90

        df["t1_11"] = df["i1_11"]
        df["t2_11"] = -df["i2_11"]

        df["t1_t2_eur_trim_5"] = df["t1_11"] + df["t2_11"]

        return df
    
    def calc_HOHS(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule et met à jour les champs :
            - i1_12
            - i2_12
            - t1_12
            - t2_12
            - t1_t2_eur_jour_6
        selon les formules :
            i1_12 = (|e| * Bi) / (1 - |e|) * ( q^-((1-|e|)/|e|) - conso^-((1-|e|)/|e|) )
                    avec conso = conso_redev_m3j_mp
            i2_12 = cout_marginal_complet_cme * (conso_redev_m3j_mp - q)
            t1_12 = i1_12
            t2_12 = -i2_12
            t1_t2_eur_jour_6 = t1_12 + t2_12
        """
        df = df.copy()

        # Sécurisation numérique
        epsilon = 1e-12

        # Variables intermédiaires
        e = abs(self.elasticite_prix_marginal)
        Bi = df["Bi"]
        q = df["q_m3_jour"].clip(lower=epsilon)
        conso_mp = df["conso_redev_m3j_mp"].clip(lower=epsilon)

        # Calcul i1_12
        if np.isclose(e, 1.0):
            df["i1_12"] = np.nan
        else:
            exponent = -(1 - e) / e
            df["i1_12"] = (e * Bi) / (1 - e) * (np.power(q, exponent) - np.power(conso_mp, exponent))

        # Calcul i2_12
        df["i2_12"] = self.cout_marginal_complet_cme * (conso_mp - q)

        # Calcul t1_12 et t2_12
        df["t1_12"] = df["i1_12"]
        df["t2_12"] = -df["i2_12"]

        # Somme t1 + t2
        df["t1_t2_eur_jour_6"] = df["t1_12"] + df["t2_12"]

        return df

    

    def calc_HUHY(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les colonnes :
        i1_13 = i1_12 * 90
        i2_13 = i2_12 * 90
        t1_13 = i1_13
        t2_13 = -i2_13
        t1_t2_eur_trim_6 = t1_13 + t2_13
        """

        df = df.copy()

        # --- Calculs des nouvelles colonnes ---
        df["i1_13"] = df["i1_12"] * 90
        df["i2_13"] = df["i2_12"] * 90
        df["t1_13"] = df["i1_13"]
        df["t2_13"] = -df["i2_13"]
        df["t1_t2_eur_trim_6"] = df["t1_13"] + df["t2_13"]

        return df


    def calc_ICID(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les colonnes :
        abonnement_ttc = prix_ttc_a_EPA
        abonnement_ttc_jour = abonnement_ttc / 90
        """

        df = df.copy()

        # --- Calculs des nouvelles colonnes ---
        df["abonnement_ttc"] = self.prix_ttc_a_EPA
        df["abonnement_ttc_jour"] = df["abonnement_ttc"] / 90

        return df
    

    def calc__IFII(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs TTC des tranches EPA :
            - prix_ttc_t1 = prix_ttc_T_EPA_T1
            - prix_ttc_t2 = prix_ttc_T_EPA_T2
            - prix_ttc_t3 = prix_ttc_T_EPA_T3
            - prix_ttc_t4 = prix_ttc_T_EPA_T4
        """
        df = df.copy()

        df["prix_ttc_t1"] = self.prix_ttc_T_EPA_T1
        df["prix_ttc_t2"] = self.prix_ttc_T_EPA_T2
        df["prix_ttc_t3"] = self.prix_ttc_T_EPA_T3
        df["prix_ttc_t4"] = self.prix_ttc_T_EPA_T4

        return df
    

    def calc_IKIV(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs suivantes :
            prix_1 = elasticite_prix_marginal * LN(prix_ttc_t1)
            ln_ai_1 = LN(ai_m3_jour)
            pv_1 = prix_1 + ln_ai_1

            prix_2 = elasticite_prix_marginal * LN(prix_ttc_t2)
            ln_ai_2 = LN(ai_m3_jour)
            pv_2 = prix_2 + ln_ai_2

            prix_3 = elasticite_prix_marginal * LN(prix_ttc_t3)
            ln_ai_3 = LN(ai_m3_jour)
            pv_3 = prix_3 + ln_ai_3

            prix_4 = elasticite_prix_marginal * LN(prix_ttc_t4)
            ln_ai_4 = LN(ai_m3_jour)
            pv_4 = prix_4 + ln_ai_4
        """
        df = df.copy()
        epsilon = 1e-9  # Pour éviter log(0)

        # Calcul tranche 1
        df["prix_1"] = self.elasticite_prix_marginal * np.log(df["prix_ttc_t1"] + epsilon)
        df["ln_ai_1"] = np.log(df["ai_m3_jour"] + epsilon)
        df["pv_1"] = df["prix_1"] + df["ln_ai_1"]

        # Calcul tranche 2
        df["prix_2"] = self.elasticite_prix_marginal * np.log(df["prix_ttc_t2"] + epsilon)
        df["ln_ai_2"] = np.log(df["ai_m3_jour"] + epsilon)
        df["pv_2"] = df["prix_2"] + df["ln_ai_2"]

        # Calcul tranche 3
        df["prix_3"] = self.elasticite_prix_marginal * np.log(df["prix_ttc_t3"] + epsilon)
        df["ln_ai_3"] = np.log(df["ai_m3_jour"] + epsilon)
        df["pv_3"] = df["prix_3"] + df["ln_ai_3"]

        # Calcul tranche 4
        df["prix_4"] = self.elasticite_prix_marginal * np.log(df["prix_ttc_t4"] + epsilon)
        df["ln_ai_4"] = np.log(df["ai_m3_jour"] + epsilon)
        df["pv_4"] = df["prix_4"] + df["ln_ai_4"]

        return df


    def calc_IXJE(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les volumes journaliers et trimestriels à partir des pv_* sans boucle :
            - m3_jour_X_2 = EXP(pv_X)
            - m3_trim_X_2 = m3_jour_X_2 * 90
        """
        df = df.copy()

        # Calcul pour chaque tranche explicitement
        df["m3_jour_1_2"] = np.exp(df["pv_1"])
        df["m3_trim_1_2"] = df["m3_jour_1_2"] * 90

        df["m3_jour_2_2"] = np.exp(df["pv_2"])
        df["m3_trim_2_2"] = df["m3_jour_2_2"] * 90

        df["m3_jour_3_2"] = np.exp(df["pv_3"])
        df["m3_trim_3_2"] = df["m3_jour_3_2"] * 90

        df["m3_jour_4_2"] = np.exp(df["pv_4"])
        df["m3_trim_4_2"] = df["m3_jour_4_2"] * 90

        return df
    

    def calc_JGJR(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les indicateurs si_X_2, sc_X_2 et les consommations avec TVA et mauvaise perception.
        """
        df = df.copy()

        # SI et ET pour tranche 1
        df["si_1_2"] = (df["m3_trim_1_2"] < self.seuil_T_EPA_T4_bis).astype(int)
        df["sc_1_2"] = ((df["m3_trim_2_2"] < self.seuil_T_EPA_T4_bis) & 
                        (df["m3_trim_1_2"] > self.seuil_T_EPA_T4_bis)).astype(int) * (1 - df["si_1_2"])

        # Tranche 2
        df["si_2_2"] = ((df["m3_trim_2_2"] > self.seuil_T_EPA_T4_bis) & 
                        (df["m3_trim_2_2"] < self.seuil_T_EPA_T5_bis)).astype(int) * (1 - df["si_1_2"]) * (1 - df["sc_1_2"])
        df["sc_2_2"] = ((df["m3_trim_2_2"] > self.seuil_T_EPA_T5_bis) & 
                        (df["m3_trim_3_2"] < self.seuil_T_EPA_T5_bis)).astype(int) * \
                    (1 - df["si_1_2"]) * (1 - df["sc_1_2"]) * (1 - df["si_2_2"])

        # Tranche 3
        df["si_3_2"] = ((df["m3_trim_3_2"] > self.seuil_T_EPA_T5_bis) & 
                        (df["m3_trim_3_2"] < self.seuil_T_EPA_T6_bis)).astype(int) * \
                    (1 - df["si_1_2"]) * (1 - df["sc_1_2"]) * (1 - df["si_2_2"]) * (1 - df["sc_2_2"])
        df["sc_3_2"] = ((df["m3_trim_3_2"] > self.seuil_T_EPA_T6_bis) & 
                        (df["m3_trim_4_2"] < self.seuil_T_EPA_T6_bis)).astype(int) * \
                    (1 - df["si_1_2"]) * (1 - df["sc_1_2"]) * (1 - df["si_2_2"]) * (1 - df["sc_2_2"]) * \
                    (1 - df["si_3_2"]) * (1 - df["sc_2_2"])

        # Tranche 4
        df["si_4_2"] = (df["m3_trim_4_2"] > self.seuil_T_EPA_T6_bis).astype(int) * \
                    (1 - df["si_1_2"]) * (1 - df["sc_1_2"]) * (1 - df["si_2_2"]) * (1 - df["sc_2_2"]) * \
                    (1 - df["si_3_2"]) * (1 - df["sc_3_2"])

        # Consommation avec TVA
        df["conso_tva"] = 0
        df["conso_tva_val"] = (
            df["si_1_2"] * df["m3_trim_1_2"] +
            df["sc_1_2"] * self.seuil_T_EPA_T4_bis+
            df["si_2_2"] * df["m3_trim_2_2"] +
            df["sc_2_2"] * self.seuil_T_EPA_T5_bis +
            df["si_3_2"] * df["m3_trim_3_2"] +
            df["sc_3_2"] * self.seuil_T_EPA_T6_bis +
            df["si_4_2"] * df["m3_trim_4_2"]
        )

        # Surconsommation
        #df["surconso"] = df["sur_conso_2"]  # à adapter si source différente

        # Consommation totale avec mauvaise perception
        df["conso_mauvaise"] = df["conso_tva_val"] + df["surconso"]

        # Différence IBT / redevance %
        df["diff_ib_t_pct"] = ((df["conso_mauvaise"] - df["c_ibt"]) / df["c_ibt"]) * 100

        return df
    
    def calc_JT(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule le coût environnemental non récupéré :
            cout_env_non_recup = MAX(cout_environnemental_ce - redevances_tarif_ep - redevances_tarif_a - cvm, 0) * JQ15
        """
        df = df.copy()

        df["cout_env_non_recup"] = np.maximum(
            self.cout_environnemental_ce - self.redevances_tarif_ep - self.redevances_tarif_a - self.cvm, 
            0
        ) * df["conso_mauvaise"]

        return df
    
    def calc_JV_JW(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les consommations TTC journalières :
            - conso_ttc_m3_jour_pp = conso_tva_val / 90
            - conso_ttc_m3_jour_mp = conso_mauvaise / 90
        """
        df = df.copy()

        df["conso_ttc_m3_jour_pp"] = df["conso_tva_val"] / 90
        df["conso_ttc_m3_jour_mp"] = df["conso_mauvaise"] / 90

        return df
    
    def calc_JYKG(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les colonnes principales de consommation et de variations :
            - q_star_consommation_rang1
            - consommation_hrt
            - conso_hrt_mauvaise_perception
            - variation_conso_hrt_optimum_q_star
            - variation_conso_hrt_mp_optimum_q_star
            - consommation_redevance_sans_tva
            - conso_redevance_mauvaise_perception
            - variation_conso_redevance_optimum_q_star
            - variation_conso_redevance_mp_optimum_q_star
        """
        df = df.copy()

        df["q_star_consommation_rang1"] = df["conso_q_cout_complet_m3_trim"]
        df["consommation_hrt"] = df["conso_hrt_m3_trim_val"]
        df["conso_hrt_mauvaise_perception"] = df["conso_mauvaise_percep_m3_trim"]
        df["variation_conso_hrt_optimum_q_star"] = df["var_conso_hrt_optq"]
        df["variation_conso_hrt_mp_optimum_q_star"] = df["var_conso_hrt_mp_optq"]
        df["consommation_redevance_sans_tva"] = df["conso_sans_tva_val"]
        df["conso_redevance_mauvaise_perception"] = df["conso_mauvaise_percep"]
        df["variation_conso_redevance_optimum_q_star"] = df["var_conso_redev_optq"]
        df["variation_conso_redevance_mp_optimum_q_star"] = df["var_conso_redev_mp_optq"]

        return df


    def calc_KIKO(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les colonnes de variations de consommation et les dummies :
            - variation_conso_ttc_optimum_q_star
            - variation_conso_hrt_q_star
            - effet_redevance
            - effet_tva
            - dummy_1_a_menage_inf_optimum
            - dummy_1_b_menage_sup_optimum
            - dummy_1_c_conso_egale_optimum
        """
        df = df.copy()

        # Variations de consommation
        df["variation_conso_ttc_optimum_q_star"] = df["conso_tva_val"] - df["conso_q_cout_complet_m3_trim"]
        df["variation_conso_hrt_q_star"] = df["consommation_hrt"] - df["q_star_consommation_rang1"]

        # Effets
        df["effet_redevance"] = df["consommation_redevance_sans_tva"] - df["consommation_hrt"]
        df["effet_tva"] = df["conso_tva_val"] - df["consommation_redevance_sans_tva"]

        # Dummies
        df["dummy_1_a_menage_inf_optimum"] = np.where(df["variation_conso_ttc_optimum_q_star"] < 0, 1, 0)
        df["dummy_1_b_menage_sup_optimum"] = np.where(df["variation_conso_ttc_optimum_q_star"] > 0, 1, 0)
        df["dummy_1_c_conso_egale_optimum"] = np.where(df["variation_conso_ttc_optimum_q_star"] == 0, 1, 0)

        return df
    



    def calc_KQKW(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Met à jour les colonnes de variations de consommation et dummies pour mauvaise perception :
            - variation_conso_ttc_mp_optimum_q_star
            - variation_conso_hrt_mp_q_star
            - effet_redevance_1
            - effet_tva_1
            - dummy_1_d_menage_inf_optimum
            - dummy_1_e_menage_sup_optimum
            - dummy_1_f_conso_egale_optimum
        """
        df = df.copy()

        # Variations de consommation
        df["variation_conso_ttc_mp_optimum_q_star"] = df["conso_mauvaise"] - df["conso_q_cout_complet_m3_trim"]
        df["variation_conso_hrt_mp_q_star"] = df["conso_hrt_mauvaise_perception"] - df["q_star_consommation_rang1"]

        # Effets
        df["effet_redevance_1"] = df["conso_redevance_mauvaise_perception"] - df["conso_hrt_mauvaise_perception"]
        df["effet_tva_1"] = df["conso_mauvaise"] - df["conso_redevance_mauvaise_perception"]

        # Dummies
        df["dummy_1_d_menage_inf_optimum"] = np.where(df["variation_conso_ttc_mp_optimum_q_star"] < 0, 1, 0)
        df["dummy_1_e_menage_sup_optimum"] = np.where(df["variation_conso_ttc_mp_optimum_q_star"] > 0, 1, 0)
        df["dummy_1_f_conso_egale_optimum"] = np.where(df["variation_conso_ttc_mp_optimum_q_star"] == 0, 1, 0)

        return df


    


    def calc_KYLC(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs des colonnes suivantes :
            - i1_14 = (|elasticite_prix_marginal| * Bi) / (1 - |elasticite_prix_marginal|) *
                    ((q_m3_jour ^ -((1 - |elasticite_prix_marginal|) / |elasticite_prix_marginal|)) -
                    (conso_ttc_m3_jour_pp ^ -((1 - |elasticite_prix_marginal|) / |elasticite_prix_marginal|)))
            - i2_14 = cout_marginal_complet_cme * (conso_ttc_m3_jour_pp - q_m3_jour)
            - t1_14 = i1_14
            - t2_14 = -i2_14
            - t1_t2_euro_jour = t1_14 + t2_14
        """
        df = df.copy()

        # Petits epsilon pour éviter divisions ou logs de zéro
        eps = 1e-12

        # Élasticité absolue sécurisée
        e = np.abs(self.elasticite_prix_marginal)
        e = np.where(e == 0, eps, e)

        # Calcul du ratio d’exposant
        ratio = (1 - e) / e

        # i1_14
        df["i1_14"] = (
            (e * df["Bi"]) / (1 - e)
            * (
                np.power(df["q_m3_jour"].clip(lower=eps), -ratio)
                - np.power(df["conso_ttc_m3_jour_pp"].clip(lower=eps), -ratio)
            )
        )

        # i2_14
        df["i2_14"] = self.cout_marginal_complet_cme * (
            df["conso_ttc_m3_jour_pp"] - df["q_m3_jour"]
        )

        # t1_14, t2_14 et somme
        df["t1_14"] = df["i1_14"]
        df["t2_14"] = -df["i2_14"]
        df["t1_t2_euro_jour"] = df["t1_14"] + df["t2_14"]

        return df

    

    def calc_LELI(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs des colonnes suivantes :
            - i1_15 = i1_14 * 90
            - i2_15 = i2_14 * 90
            - t1_15 = i1_15
            - t2_15 = -i2_15
            - t1_t2_euro_trim = t1_15 + t2_15
        """
        df = df.copy()

        # Calculs
        df["i1_15"] = df["i1_14"] * 90
        df["i2_15"] = df["i2_14"] * 90
        df["t1_15"] = df["i1_15"]
        df["t2_15"] = -df["i2_15"]
        df["t1_t2_euro_trim"] = df["t1_15"] + df["t2_15"]

        return df



    def calc_LKLO(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs des colonnes suivantes :
            - i1_16 = (|elasticite_prix_marginal| * Bi) / (1 - |elasticite_prix_marginal|) *
                    ((q_m3_jour ^ -((1 - |elasticite_prix_marginal|) / |elasticite_prix_marginal|)) -
                    (JBi ^ -((1 - |elasticite_prix_marginal|) / |elasticite_prix_marginal|)))
            - i2_16 = cout_marginal_complet_cme * (conso_ttc_m3_jour_mp - q_m3_jour)
            - t1_16 = i1_16
            - t2_16 = -i2_16
            - t1_t2_euro_jour_1 = t1_16 + t2_16
        """
        df = df.copy()

        eps = 1e-12  # pour éviter les divisions par zéro

        # Élasticité absolue sécurisée
        abs_e = np.abs(self.elasticite_prix_marginal)
        abs_e = np.where(abs_e == 0, eps, abs_e)

        ratio = (1 - abs_e) / abs_e

        # i1_16
        df["i1_16"] = (
            (abs_e * df["Bi"]) / (1 - abs_e)
            * (
                np.power(df["q_m3_jour"].clip(lower=eps), -ratio)
                - np.power(df["conso_ttc_m3_jour_mp"].clip(lower=eps), -ratio)
            )
        )

        # i2_16
        df["i2_16"] = self.cout_marginal_complet_cme * (
            df["conso_ttc_m3_jour_mp"] - df["q_m3_jour"]
        )

        # t1_16 et t2_16
        df["t1_16"] = df["i1_16"]
        df["t2_16"] = -df["i2_16"]

        # Somme en euros par jour
        df["t1_t2_euro_jour_1"] = df["t1_16"] + df["t2_16"]

        return df


        ### LQLU

    def calc_LQLU(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les valeurs des colonnes suivantes :
            - i1_17 = i1_16 * 90
            - i2_17 = i2_16 * 90
            - t1_17 = i1_17
            - t2_17 = -i2_17
            - t1_t2_euro_trim_1 = t1_17 + t2_17
        """
        df = df.copy()

        # Calculs principaux
        df["i1_17"] = df["i1_16"] * 90
        df["i2_17"] = df["i2_16"] * 90
        df["t1_17"] = df["i1_17"]
        df["t2_17"] = -df["i2_17"]

        # Somme trimestrielle
        df["t1_t2_euro_trim_1"] = df["t1_17"] + df["t2_17"]

        return df


    
    def pipeline(self):
        """
        Fonction pipeline pour exécuter l'ensemble des traitements sur le DataFrame.

        Args:
            fichier_excel (str): Chemin du fichier Excel source.
            export_path (str, optional): Chemin pour exporter le DataFrame final. Par défaut None.
        Returns:
            pd.DataFrame: DataFrame final après tous les calculs.
        """
        print("="*60)
        print("INITIALISATION DE LA CLASSE effeco_surplusG2_CP")
        print("="*60)

        # Création d'une instance de la classe
    

        print("\n" + "="*60)
        print("CRÉATION DU DATAFRAME AVEC DONNÉES RÉELLES")
        print("="*60)

        try:
            df = self.create_dataframe_structure()
            if len(df) == 0:
                print("❌ DataFrame créé mais vide.")
                return None
            
            print(f"\n✅ DataFrame créé avec succès ! {len(df)} lignes x {len(df.columns)} colonnes")
            
            # Conversion des colonnes numériques
            colonnes_a_convertir = [
                'revenu_net_mois', 'c_m3_trim', 'c_m3_trim_2', 
                'c_ibt', 'c_ibt_pp', 'c_tbse', 
                'consom_nordin_trim', 'consom_taylor_trim'
            ]
            for col in colonnes_a_convertir:
                df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
            
            # -----------------------------
            # Début des calculs successifs
            # -----------------------------
            df_complet = self.KQ(df)
            df_complet = self.SU(df_complet)
            df_complet = self.calc_Bi(df_complet)
            df_complet = self.calc_i1_i2_t1_t2(df_complet)
            df_complet = self.calc_AHAM(df_complet)
            df_complet = self.calc_AOAV(df_complet)
            df_complet = self.AXBC(df_complet)
            df_complet = self.calc_BEBL(df_complet)
            df_complet = self.calc_BNBS(df_complet)
            df_complet = self.calc_BWBX(df_complet)
            df_complet = self.calcBZCC(df_complet)
            df_complet = self.calc_CECP(df_complet)
            df_complet = self.calc_CRCY(df_complet)
            df_complet = self.calc_DADL(df_complet)
            df_complet = self.calc_DNDO(df_complet)
            df_complet = self.calc_DQDX(df_complet)
            df_complet = self.calc_DZED(df_complet)
            df_complet = self.calc_EFEJ(df_complet)
            df_complet = self.calc_ELEP(df_complet)
            df_complet = self.calc_ELER(df_complet)
            df_complet = self.calc_EZFA(df_complet)
            df_complet = self.calc_PRIX_FCFF(df_complet)
            df_complet = self.calc_FHFF(df_complet)
            df_complet = self.calc_FUGB(df_complet)
            df_complet = self.calc_GDGO(df_complet)
            df_complet = self.calc_GQGR(df_complet)
            df_complet = self.calc_GTHA(df_complet)
            df_complet = self.calc_HCHG(df_complet)
            df_complet = self.calc_HIHM(df_complet)
            df_complet = self.calc_HOHS(df_complet)
            df_complet = self.calc_HUHY(df_complet)
            df_complet = self.calc_ICID(df_complet)
            df_complet = self.calc__IFII(df_complet)
            df_complet = self.calc_IKIV(df_complet)
            df_complet = self.calc_IXJE(df_complet)
            df_complet = self.calc_JGJR(df_complet)
            df_complet = self.calc_JT(df_complet)
            df_complet = self.calc_JV_JW(df_complet)
            df_complet = self.calc_JYKG(df_complet)
            df_complet = self.calc_KIKO(df_complet)
            df_complet = self.calc_KQKW(df_complet)
            df_complet = self.calc_KYLC(df_complet)
            df_complet = self.calc_LELI(df_complet)
            df_complet = self.calc_LKLO(df_complet)
            df_complet = self.calc_LQLU(df_complet)
            
            print("\n✅ Tous les calculs terminés !")
            print(f"DataFrame final: {len(df_complet)} lignes x {len(df_complet.columns)} colonnes")

            # # Export si chemin fourni
            # if export_path:
            #     parametres.export_to_excel(dataframe=df_complet, output_path=export_path)
            #     print(f"\n📄 DataFrame exporté vers : {export_path}")

            return df_complet

        except Exception as e:
            print(f"❌ Erreur lors du pipeline : {e}")
            return None





# Exemple d'utilisation
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

    _effeco_suruplusG2_CP = effeco_suruplusG2_CP(dfsource)
    # Chemin vers le fichier Excel source
    fichier_source = "surplus_G2_data.xls"

    # # Chemin pour exporter le DataFrame final (optionnel)
    # fichier_export = "resultats/surplus_G2_complet.xlsx"

    # Appel de la fonction pipeline
    df_final = _effeco_suruplusG2_CP.pipeline()

    if df_final is not None:
        # Affichage d'un aperçu des premières lignes
        print("\nAperçu du DataFrame final :")
        print(df_final.head(5))

        # Exemple : afficher certaines colonnes calculées
        colonnes_interet = ['c_captive_jour', 'ln_c_captive_jour', 'ai_m3_jour', 'q_m3_jour', 'qb_m3_jour']
        print("\nÉchantillon des colonnes clés :")
        print(df_final[colonnes_interet].head(5))
    else:
        print("❌ Le pipeline n'a pas pu être exécuté correctement.")