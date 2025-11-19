import pandas as pd
import numpy as np

class SubTInConsoDF:
    """
    Classe pour gérer les données de consommation avec calculs automatiques.
    
    Attributes:
        df (pd.DataFrame): DataFrame contenant toutes les colonnes de données
        colonnes_source (list): Liste complète des colonnes disponibles
    """
    
    def __init__(self, df_init=None, droit_acces_ep_t1=-28.3349, 
                 sub_tax_redevances=0.0000, sub_tax_hors_tva=-28.3349, 
                 sub_tax_tva=-0.5950, sub_tax_ttc=-28.9299):
        """
        Initialise le DataFrame avec les colonnes de consommation.
        
        Args:
            df_init (pd.DataFrame, optional): DataFrame d'initialisation avec les valeurs de base.
                                             Si None, initialise avec des zéros.
            droit_acces_ep_t1 (float, optional): Valeur du droit d'accès EP trimestre 1.
                                                 Par défaut: -28.3349
        """
        # Stocke le droit d'accès comme attribut de classe
        self.droit_acces_ep_t1 = droit_acces_ep_t1
        
        # Stocke les attributs Sub Tax
        self.sub_tax_redevances = sub_tax_redevances
        self.sub_tax_hors_tva = sub_tax_hors_tva
        self.sub_tax_tva = sub_tax_tva
        self.sub_tax_ttc = sub_tax_ttc

        # Liste complète des colonnes
        self.colonnes_source = [
            "menage_A11", "assaini_B11", "c_t1_C11", "c_t2_D11", "c_t3_E11", "c_t4_F11",
            "somme_conso_G11",
            "droit_acces_ep_t1_H11", "t1_ep_I11", "t2_ep_J11", "t3_ep_K11", "t4_ep_L11", "total_ep_M11",
            "droit_acces_2_ep_t1_N11", "t1_2_ep_O11", "t2_2_ep_P11", "t3_2_ep_Q11", "t4_2_ep_R11", "total_2_ep_S11",
            "droit_acces_3_ep_t1_T11", "t1_3_ep_U11", "t2_3_ep_V11", "t3_3_ep_W11", "t4_3_ep_X11", "total_3_ep_Y11",
            "abo_ttc_ep_Z11", "tranche1_ep_AA11", "tranche2_ep_AB11", "tranche3_ep_AC11", "tranche4_ep_AD11",
            "total_sub_tax_ttc_c_captive_ep_dae_AE11", "total_sub_tax_ttc_c_captive_ep_dai_AF11",
            "droit_acces_a_dae_t1_AI11", "t1_4_a_AJ11", "t2_4_a_AK11", "t3_4_a_AL11", "t4_4_a_AM11", "total_4_a_AN11",
            "droit_acces_a_dae_t2_AO11", "t1_5_a_AP11", "t2_5_a_AQ11", "t3_5_a_AR11", "t4_5_a_AS11", "total_5_a_AT11",
            "droit_acces_a_dae_t3_AU11", "t1_6_a_AV11", "t2_6_a_AW11", "t3_6_a_AX11", "t4_6_a_AY11", "total_6_a_AZ11",
            "abo_ttc_a_BA11", "tranche1_a_BB11", "tranche2_a_BC11", "tranche3_a_BD11", "tranche4_a_BE11",
            "total_sub_tax_ttc_c_captive_a_dae_BF11", "total_sub_tax_ttc_c_captive_a_dai_BG11",
            "droit_acces_epa_dae_t4_BJ11", "t1_7_epa_BK11", "t2_7_epa_BL11", "t3_7_epa_BM11", "t4_7_epa_BN11",
            "total_7_epa_BO11", "droit_acces_epa_dae_t5_BP11", "t1_8_epa_BQ11", "t2_8_epa_BR11",
            "t3_8_epa_BS11", "t4_8_epa_BT11", "total_8_epa_BU11", "droit_acces_epa_dae_t6_BV11",
            "t1_9_epa_BW11", "t2_9_epa_BX11", "t3_9_epa_BY11", "t4_9_epa_BZ11", "total_9_epa_CA11",
            "abo_ttc_epa_CB11", "tranche1_epa_CC11", "tranche2_epa_CD11", "tranche3_epa_CE11", "tranche4_epa_CF11",
            "total_sub_tax_ttc_c_captive_epa_dae_CG11", "total_sub_tax_ttc_c_captive_epa_dai_CH11"
        ]
        
        # Colonnes principales à initialiser
        self.colonnes_principales = [
            "menage_A11", "assaini_B11", "c_t1_C11", 
            "c_t2_D11", "c_t3_E11", "c_t4_F11"
        ]
        
        # Colonnes de consommation pour les calculs
        self.colonnes_conso = ['c_t1_C11', 'c_t2_D11', 'c_t3_E11', 'c_t4_F11']
        
        # Initialisation du DataFrame avec toutes les colonnes à zéro
        self.df = pd.DataFrame([{col: 0 for col in self.colonnes_source}])
        
        # Si un DataFrame d'initialisation est fourni, on l'utilise
        if df_init is not None:
            self._initialiser_depuis_df(df_init)
        
        # Initialise la colonne droit_acces_ep_t1_H11
        self.initialiser_droit_acces_ep_t1()
        
        # Calcul initial de la somme des consommations
        self.calcul_somme_conso()

        self.df['droit_acces_ep_t1_H11']= self.droit_acces_ep_t1
    
    def _initialiser_depuis_df(self, df_init):
        """
        Initialise les valeurs depuis un DataFrame fourni.
        
        Args:
            df_init (pd.DataFrame): DataFrame contenant les valeurs initiales
        """
        for col in self.colonnes_principales:
            if col in df_init.columns:
                self.df[col] = df_init[col].values
    
    def initialiser_droit_acces_ep_t1(self, valeur=None):
        """
        Initialise la colonne droit_acces_ep_t1_H11 avec une valeur donnée.
        
        Args:
            valeur (float, optional): Valeur à attribuer à la colonne.
                                     Si None, utilise self.droit_acces_ep_t1
        
        Example:
            >>> data = SubTInConsoDF()
            >>> data.initialiser_droit_acces_ep_t1(-30.5)
        """
        if valeur is None:
            valeur = self.droit_acces_ep_t1
        
        self.df['droit_acces_ep_t1_H11'] = valeur
    
    def calcul_somme_conso(self):
        """Calcule la colonne 'somme_conso_G11' à partir des consommations trimestrielles."""
        self.df['somme_conso_G11'] = self.df[self.colonnes_conso].sum(axis=1)
    
    def requete_somme_conso(self, data):
        """
        Applique le calcul de somme de consommation sur un DataFrame externe.
        
        Cette méthode permet d'appliquer la même logique de calcul que calcul_somme_conso()
        mais sur un DataFrame fourni en paramètre au lieu du DataFrame interne.
        
        Args:
            data (pd.DataFrame): DataFrame contenant les colonnes de consommation
                                 (c_t1_C11, c_t2_D11, c_t3_E11, c_t4_F11)
        
        Returns:
            pd.DataFrame: Le DataFrame modifié avec la colonne somme_conso_G11 mise à jour
        
        Example:
            >>> df_externe = pd.DataFrame({
            ...     'c_t1_C11': [1, 2, 3],
            ...     'c_t2_D11': [2, 3, 4],
            ...     'c_t3_E11': [3, 4, 5],
            ...     'c_t4_F11': [4, 5, 6]
            ... })
            >>> obj = SubTInConsoDF()
            >>> df_resultat = obj.requete_somme_conso(df_externe)
        """
        colonnes_requises = ["c_t1_C11", "c_t2_D11", "c_t3_E11", "c_t4_F11"]
        
        # Vérifie que toutes les colonnes nécessaires sont présentes
        colonnes_manquantes = [col for col in colonnes_requises if col not in data.columns]
        if colonnes_manquantes:
            raise ValueError(f"Colonnes manquantes dans le DataFrame: {colonnes_manquantes}")
        
        # Applique le calcul
        data["somme_conso_G11"] = data[colonnes_requises].sum(axis=1)
        
        return data
    
    def appliquer_tarifs_ep(self, sub_ht_op_dict):
        """
        Met à jour les colonnes de tarification EP (Eau Potable) en multipliant 
        les consommations trimestrielles par les tarifs correspondants.
        
        Cette méthode applique les formules suivantes:
        - t1_ep_I11 = c_t1_C11 * J1 (tarif trimestre 1)
        - t2_ep_J11 = c_t2_D11 * J2 (tarif trimestre 2)
        - t3_ep_K11 = c_t3_E11 * J3 (tarif trimestre 3)
        - t4_ep_L11 = c_t4_F11 * J4 (tarif trimestre 4)
        
        Note: La correspondance est J4=J1, J5=J2, J6=J3, J7=J4 dans les formules Excel
        
        Args:
            sub_ht_op_dict (dict): Dictionnaire contenant les tarifs au format 
                                   {J1: val1, J2: val2, ..., Jn: valn}
                                   Les clés J1, J2, J3, J4 doivent être présentes
        
        Raises:
            ValueError: Si les clés nécessaires (J1, J2, J3, J4) sont manquantes
        
        Example:
            >>> tarifs = {'J1': 1.2, 'J2': 1.3, 'J3': 1.4, 'J4': 1.5}
            >>> data = SubTInConsoDF(df_init)
            >>> data.appliquer_tarifs_ep(tarifs)
        """
        # Mapping entre les clés du dictionnaire et les colonnes
        # J4=J1, J5=J2, J6=J3, J7=J4 dans la notation Excel
        mapping_tarifs = {
            'J1': ('c_t1_C11', 't1_ep_I11'),  # Trimestre 1 - correspond à J4 dans Excel
            'J2': ('c_t2_D11', 't2_ep_J11'),  # Trimestre 2 - correspond à J5 dans Excel
            'J3': ('c_t3_E11', 't3_ep_K11'),  # Trimestre 3 - correspond à J6 dans Excel
            'J4': ('c_t4_F11', 't4_ep_L11')   # Trimestre 4 - correspond à J7 dans Excel
        }
        
        # Vérifie que toutes les clés nécessaires sont présentes
        cles_manquantes = [cle for cle in mapping_tarifs.keys() if cle not in sub_ht_op_dict]
        if cles_manquantes:
            raise ValueError(f"Clés manquantes dans sub_ht_op_dict: {cles_manquantes}")
        
        # Applique les calculs pour chaque trimestre
        for cle_tarif, (col_conso, col_resultat) in mapping_tarifs.items():
            tarif = sub_ht_op_dict[cle_tarif]
            self.df[col_resultat] = self.df[col_conso] * tarif
        
        # Calcule le total EP
        self.calcul_total_ep()
    
    def calcul_total_ep(self):
        """Calcule la colonne 'total_ep_M11' comme somme des tarifs EP trimestriels."""
        colonnes_ep = ['t1_ep_I11', 't2_ep_J11', 't3_ep_K11', 't4_ep_L11']
        self.df['total_ep_M11'] = self.df[colonnes_ep].sum(axis=1)
    
    def mettre_a_jour(self, colonne, valeur):
        """
        Met à jour une colonne avec une nouvelle valeur et recalcule la somme si nécessaire.
        
        Args:
            colonne (str): Nom de la colonne à mettre à jour
            valeur: Nouvelle valeur (scalaire ou array)
        
        Raises:
            ValueError: Si la colonne n'existe pas
        """
        if colonne not in self.df.columns:
            raise ValueError(f"La colonne '{colonne}' n'existe pas dans le DataFrame")
        
        self.df[colonne] = valeur
        
        # Recalcule la somme si une colonne de consommation a été modifiée
        if colonne in self.colonnes_conso:
            self.calcul_somme_conso()
    
    def afficher(self, colonnes=None):
        """
        Affiche les colonnes spécifiées ou les colonnes principales par défaut.
        
        Args:
            colonnes (list, optional): Liste des colonnes à afficher. 
                                      Si None, affiche les colonnes principales.
        """
        if colonnes is None:
            colonnes = self.colonnes_principales + ["somme_conso_G11"]
        
        # Filtre les colonnes existantes
        colonnes_existantes = [col for col in colonnes if col in self.df.columns]
        
        if not colonnes_existantes:
            print("Aucune colonne à afficher")
            return
        
        print(self.df[colonnes_existantes].to_string(index=False))
    
    def obtenir_resume(self):
        """
        Retourne un résumé statistique des colonnes de consommation.
        
        Returns:
            pd.Series: Statistiques des consommations
        """
        stats = {
            'Total consommation': self.df['somme_conso_G11'].sum(),
            'Moyenne par trimestre': self.df[self.colonnes_conso].mean().mean(),
            'Consommation T1': self.df['c_t1_C11'].sum(),
            'Consommation T2': self.df['c_t2_D11'].sum(),
            'Consommation T3': self.df['c_t3_E11'].sum(),
            'Consommation T4': self.df['c_t4_F11'].sum(),
        }
        return pd.Series(stats)
    
    def exporter_csv(self, fichier, colonnes=None):
        """
        Exporte les données vers un fichier CSV.
        
        Args:
            fichier (str): Chemin du fichier de sortie
            colonnes (list, optional): Colonnes à exporter. Si None, exporte toutes les colonnes.
        """
        if colonnes is None:
            df_export = self.df
        else:
            colonnes_existantes = [col for col in colonnes if col in self.df.columns]
            df_export = self.df[colonnes_existantes]
        
        df_export.to_csv(fichier, index=False)
        print(f"Données exportées vers {fichier}")
    
    def __repr__(self):
        """Représentation textuelle de l'objet."""
        return f"SubTInConsoDF(lignes={len(self.df)}, colonnes={len(self.df.columns)})"
    

    def appliquer_sub_tax_redevances_ep(self, sub_tax_redevances_dict):
        """
        Applique les calculs des colonnes '2_ep' à partir des consommations
        et des coefficients de sub_tax_redevances.

        Formules Excel / SQL équivalentes :
            droit_acces_2_ep_t1_N11 = K2 (= self.sub_tax_redevances)
            t1_2_ep_O11 = c_t1_C11 * K1
            t2_2_ep_P11 = c_t2_D11 * K2
            t3_2_ep_Q11 = c_t3_E11 * K3
            t4_2_ep_R11 = c_t4_F11 * K4
            total_2_ep_S11 = droit_acces_2_ep_t1_N11 + t1_2_ep_O11 + t2_2_ep_P11 + t3_2_ep_Q11 + t4_2_ep_R11

        Args:
            sub_tax_redevances_dict (dict): Dictionnaire de coefficients comme renvoyé
                par get_sub_tax_redevances_dict(), ex :
                {'K1': 1.1, 'K2': 1.2, 'K3': 1.3, 'K4': 1.4}
        """
        # Récupère les coefficients avec valeurs par défaut 0.0
        K1 = sub_tax_redevances_dict.get('K1', 0.0)
        K2 = sub_tax_redevances_dict.get('K2', 0.0)
        K3 = sub_tax_redevances_dict.get('K3', 0.0)
        K4 = sub_tax_redevances_dict.get('K4', 0.0)

        # Applique les calculs individuels
        self.df['droit_acces_2_ep_t1_N11'] = self.sub_tax_redevances
        self.df['t1_2_ep_O11'] = self.df['c_t1_C11'] * K1
        self.df['t2_2_ep_P11'] = self.df['c_t2_D11'] * K2
        self.df['t3_2_ep_Q11'] = self.df['c_t3_E11'] * K3
        self.df['t4_2_ep_R11'] = self.df['c_t4_F11'] * K4

        # Appelle la méthode de totalisation
        self.calcul_total_2_ep()


    def calcul_total_2_ep(self):
        """
        Calcule la colonne 'total_2_ep_S11' comme la somme :
            droit_acces_2_ep_t1_N11 + t1_2_ep_O11 + t2_2_ep_P11 + t3_2_ep_Q11 + t4_2_ep_R11
        """
        colonnes = [
            'droit_acces_2_ep_t1_N11',
            't1_2_ep_O11',
            't2_2_ep_P11',
            't3_2_ep_Q11',
            't4_2_ep_R11'
        ]
        self.df['total_2_ep_S11'] = self.df[colonnes].sum(axis=1)

    def calculer_total_3_ep(self, M_values):
        """
        Calcule total_3_ep_Y11 pour un nombre variable de coefficients M (TVA).

        Args:
            M_values (list[float]): Liste ou collection de valeurs TVA (M4, M5, M6, ...)

        Hypothèses :
            - self.df contient les colonnes c_t1_C11, c_t2_D11, ..., c_tn
            - self.sub_tax_TVA contient la valeur du droit d'accès (M2)
        """

        droit_acces_3_ep_t1 = self.sub_tax_tva
        total_intermediaire = 0.0
        details = {}

        for i, M in enumerate(M_values, start=1):
            col_name = f'c_t{i}_C11'
            if col_name not in self.df.columns:
                # si la colonne n’existe pas, on arrête la boucle
                break
            c_value = self.df.loc[0, col_name]
            tranche_val = c_value * M
            details[f"t{i}_3_ep"] = tranche_val
            total_intermediaire += tranche_val

        # Total final
        total_3_ep = droit_acces_3_ep_t1 + total_intermediaire

        # Retour complet
        return {
            "droit_acces_3_ep_t1": droit_acces_3_ep_t1,
            **details,
            "total_3_ep": total_3_ep
        }

    
    def calcul_total_sub_tax_ttc_ep(self):
        """
        Calcule les colonnes de totalisation TTC EP (eau potable) selon les formules :

            abo_ttc_ep_Z11 = droit_acces_ep_t1_H11 + droit_acces_2_ep_t1_N11 + droit_acces_3_ep_t1_T11
            tranche1_ep_AA11 = t1_ep_I11 + t1_2_ep_O11 + t1_3_ep_U11
            tranche2_ep_AB11 = t2_ep_J11 + t2_2_ep_P11 + t2_3_ep_V11
            tranche3_ep_AC11 = t3_ep_K11 + t3_2_ep_Q11 + t3_3_ep_W11
            tranche4_ep_AD11 = t4_ep_L11 + t4_2_ep_R11 + t4_3_ep_X11
            total_sub_tax_ttc_c_captive_ep_dae_AE11 =
                tranche1_ep_AA11 + tranche2_ep_AB11 + tranche3_ep_AC11 + tranche4_ep_AD11

        Returns:
            pd.Series: Ligne de DataFrame contenant les valeurs calculées.
        """
        self._verifier_colonnes([
            'droit_acces_ep_t1_H11', 'droit_acces_2_ep_t1_N11', 'droit_acces_3_ep_t1_T11',
            't1_ep_I11', 't2_ep_J11', 't3_ep_K11', 't4_ep_L11',
            't1_2_ep_O11', 't2_2_ep_P11', 't3_2_ep_Q11', 't4_2_ep_R11',
            't1_3_ep_U11', 't2_3_ep_V11', 't3_3_ep_W11', 't4_3_ep_X11'
        ]) if hasattr(self, "_verifier_colonnes") else None

        df = self.df  # raccourci

        # Calculs des composantes
        df['abo_ttc_ep_Z11'] = (
            df['droit_acces_ep_t1_H11']
            + df['droit_acces_2_ep_t1_N11']
            + df['droit_acces_3_ep_t1_T11']
        )

        df['tranche1_ep_AA11'] = df['t1_ep_I11'] + df['t1_2_ep_O11'] + df['t1_3_ep_U11']
        df['tranche2_ep_AB11'] = df['t2_ep_J11'] + df['t2_2_ep_P11'] + df['t2_3_ep_V11']
        df['tranche3_ep_AC11'] = df['t3_ep_K11'] + df['t3_2_ep_Q11'] + df['t3_3_ep_W11']
        df['tranche4_ep_AD11'] = df['t4_ep_L11'] + df['t4_2_ep_R11'] + df['t4_3_ep_X11']

        df['total_sub_tax_ttc_c_captive_ep_dae_AE11'] = (
            df['tranche1_ep_AA11']
            + df['tranche2_ep_AB11']
            + df['tranche3_ep_AC11']
            + df['tranche4_ep_AD11']
        )

        return df[[
            'abo_ttc_ep_Z11',
            'tranche1_ep_AA11', 'tranche2_ep_AB11',
            'tranche3_ep_AC11', 'tranche4_ep_AD11',
            'total_sub_tax_ttc_c_captive_ep_dae_AE11'
        ]]
    
    ### AF11

    def calcul_total_sub_tax_ttc_ep_dai(self):
        """
        Calcule la colonne :
            total_sub_tax_ttc_c_captive_ep_dai_AF11 = total_sub_tax_ttc_c_captive_ep_dae_AE11 + abo_ttc_ep_Z11

        Returns:
            float: Valeur calculée pour la ligne courante.
        """
        self._verifier_colonnes([
            'total_sub_tax_ttc_c_captive_ep_dae_AE11',
            'abo_ttc_ep_Z11'
        ]) if hasattr(self, "_verifier_colonnes") else None

        df = self.df
        df['total_sub_tax_ttc_c_captive_ep_dai_AF11'] = (
            df['total_sub_tax_ttc_c_captive_ep_dae_AE11'] + df['abo_ttc_ep_Z11']
        )

        return df['total_sub_tax_ttc_c_captive_ep_dai_AF11']





# Exemple d'utilisation
if __name__ == "__main__":
    print("=== Test 1: Initialisation avec données ===")
    df_init = pd.DataFrame([{
        "menage_A11": 10, 
        "assaini_B11": 5, 
        "c_t1_C11": 3,
        "c_t2_D11": 4, 
        "c_t3_E11": 2, 
        "c_t4_F11": 1
    }])
    
    data = SubTInConsoDF(df_init)
    data.afficher()
    
    print("\n=== Test 2: Mise à jour d'une valeur ===")
    data.mettre_a_jour('c_t1_C11', 5)
    data.afficher()
    
    print("\n=== Test 3: Résumé statistique ===")
    print(data.obtenir_resume())
    
    print("\n=== Test 4: Initialisation vide ===")
    data_vide = SubTInConsoDF()
    data_vide.afficher()
    print(f"Droit d'accès EP T1: {data_vide.df['droit_acces_ep_t1_H11'].iloc[0]}")
    
    print("\n=== Test 4b: Initialisation avec droit d'accès personnalisé ===")
    data_custom = SubTInConsoDF(droit_acces_ep_t1=-30.5)
    print(f"Droit d'accès EP T1 personnalisé: {data_custom.df['droit_acces_ep_t1_H11'].iloc[0]}")
    
    print("\n=== Représentation de l'objet ===")
    print(data)
    
    print("\n=== Test 5: Requête sur DataFrame externe ===")
    df_externe = pd.DataFrame({
        'c_t1_C11': [1, 2, 3],
        'c_t2_D11': [2, 3, 4],
        'c_t3_E11': [3, 4, 5],
        'c_t4_F11': [4, 5, 6]
    })
    print("DataFrame avant calcul:")
    print(df_externe)
    
    df_resultat = data.requete_somme_conso(df_externe)
    print("\nDataFrame après calcul:")
    print(df_resultat)
    
    print("\n=== Test 6: Application des tarifs EP ===")
    # Simulation d'un dictionnaire retourné par get_sub_ht_op_dict()
    # J4=J1, J5=J2, J6=J3, J7=J4 dans la notation Excel
    tarifs_dict = {
        'J1': 1.2,  # Tarif pour trimestre 1 (= J4 dans Excel)
        'J2': 1.3,  # Tarif pour trimestre 2 (= J5 dans Excel)
        'J3': 1.4,  # Tarif pour trimestre 3 (= J6 dans Excel)
        'J4': 1.5   # Tarif pour trimestre 4 (= J7 dans Excel)
    }
    
    data.appliquer_tarifs_ep(tarifs_dict)
    
    colonnes_ep = ["c_t1_C11", "c_t2_D11", "c_t3_E11", "c_t4_F11",
                   "t1_ep_I11", "t2_ep_J11", "t3_ep_K11", "t4_ep_L11", "total_ep_M11"]
    print("DataFrame après application des tarifs EP:")
    data.afficher(colonnes_ep)


    # Simulation du dictionnaire retourné
    sub_tax_dict = {
        'K1': 1.05, 
        'K2': 1.10, 
        'K3': 1.15, 
        'K4': 1.20
    }

    # Application sur ton objet
    data.appliquer_sub_tax_redevances_ep(sub_tax_dict)

    # Vérification du résultat
    colonnes = [
        'droit_acces_2_ep_t1_N11',
        't1_2_ep_O11', 't2_2_ep_P11', 't3_2_ep_Q11', 't4_2_ep_R11',
        'total_2_ep_S11'
    ]
    data.afficher(colonnes)


    ##### calcul de N11	O11	P11	Q11	R11

    
    data.appliquer_sub_tax_redevances_ep(sub_tax_dict)

    colonnes_affichees = [
        'droit_acces_2_ep_t1_N11',
        't1_2_ep_O11', 't2_2_ep_P11', 't3_2_ep_Q11', 't4_2_ep_R11',
        'total_2_ep_S11'
    ]
    data.afficher(colonnes_affichees)

    ##### T11	U11	V11	W11	X11	Y11 attentyion TODO


    tva_dict = {
    'J1': 0.1234,  # TVA pour le 1er trimestre
    'J2': 0.2345,  # TVA pour le 2ème trimestre
    'J3': 0.3456,  # TVA pour le 3ème trimestre
    'J4': 0.4567   # TVA pour le 4ème trimestre
    }

    # On peut alors l’utiliser pour les calculs
    print(tva_dict['J1'])  # 0.1234
    print(tva_dict['J2'])  # 0.2345

    print("Dictionnaire TVA :", tva_dict)

    # Exemple : extraire les valeurs dans l'ordre pour calculer total_3_ep
    M_values = list(tva_dict.values())
    print("Valeurs TVA pour calcul :", M_values)

    # Appel de la méthode de calcul total_3_ep avec ces valeurs
    res_3_ep = data.calculer_total_3_ep(M_values)

    # Affichage du résultat
    print("Droit d'accès 3 EP :", res_3_ep["droit_acces_3_ep_t1"])
    print("Total 3 EP :", res_3_ep["total_3_ep"])

    
    
    # Supposons que tu as déjà appelé :
    # obj.appliquer_tarifs_ep(...)
    # obj.appliquer_sub_tax_redevances_ep(...)
    # obj.calculer_total_3_ep([...])


    #### Z11	AA11	AB11	AC11	AD11	AE11

    result = data.calcul_total_sub_tax_ttc_ep()
    print(result)

    # AF11




