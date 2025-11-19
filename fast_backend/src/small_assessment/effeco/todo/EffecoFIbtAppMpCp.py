import pandas as pd
from typing import Optional
from pathlib import Path
from Effeco_facture_ibt_approchee_mp import Effeco_facture_ibt_approchee_mp


class EffecoFIbtAppMpCp:
    """
    Classe pour gérer les paramètres de facturation IBT (Increasing Block Tariff)
    et construire les DataFrames associés.
    
    EffecoFIbtAppMpCp : Effeco Facture IBT Approchée Multi-Projets avec Calculs de Prix
    """
    
    def __init__(self, id_projet: int = 1):
        """
        Initialise les paramètres avec les valeurs par défaut.
        
        Args:
            id_projet (int): Identifiant du projet (par défaut 1)
        """
        # ID projet par défaut
        self.id_projet = id_projet
        
        # Configuration des seuils de consommation
        self._init_seuils()
        
        # Configuration des prix HT
        self._init_prix_ht()
        
        # Configuration des redevances
        self._init_redevances()
        
        # Configuration de la TVA
        self._init_tva()
        
        # Structure des colonnes du DataFrame
        self._colonnes = self._define_columns()

    def _init_seuils(self) -> None:
        """Initialise les seuils de consommation."""
        self.t_ep_seuil_max_1 = 15
        self.t_ep_seuil_max_2 = 30
        self.t_ep_seuil_max_3 = 60

    def _init_prix_ht(self) -> None:
        """Initialise les prix HT par tranche."""
        self.p_HT_Op_1 = 18.69
        self.p_HT_Op_2 = 0.878
        self.p_HT_Op_3 = 1.839
        self.p_HT_Op_4 = 2.768
        self.p_HT_Op_5 = 4.38

    def _init_redevances(self) -> None:
        """Initialise les redevances."""
        self.tarif_ep_redevances = 0
        self.redevances_abonnement = 0
        self.redevances_accise_euro_m3 = 0.12
        self.redevances_accise_eur_m3 = 0.04

    def _init_tva(self) -> None:
        """Initialise les paramètres de TVA."""
        # Montants TVA unitaires
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

    def _define_columns(self) -> list[str]:
        """
        Définit la structure des colonnes du DataFrame.
        
        Returns:
            list[str]: Liste des noms de colonnes
        """
        return [
            "id_projet", "menage", "assaini", "consommation_m3_trim",
            "q_01", "calcul_c_t3", "q_02", "calcul_c_t4", "q_03", "q_04",
            
            # Colonnes eau potable (ep)
            "ep_abonnement", "ep_t1", "ep_t2", "ep_t3", "ep_t4", "ep_total",
            "ep_taxe_forfaitaire", "ep_taxe_t1", "ep_taxe_t2", "ep_taxe_t3", "ep_taxe_t4", "ep_taxe_total",
            "ep_abo_ht", "ep_abo_ht_t1", "ep_abo_ht_t2", "ep_abo_ht_t3", "ep_abo_ht_t4", "ep_abo_ht_total",
            "ep_abo_ttc", "ep_tranche_1", "ep_tranche_2", "ep_tranche_3", "ep_tranche_4",
            "ep_total_dep_ttc_hors_abo", "ep_montant_facture_ttc",
            
            # Colonnes assainissement (a)
            "a_abonnement", "a_t1", "a_t2", "a_t3", "a_t4", "a_total",
            "a_taxe_forfaitaire", "a_taxe_t1", "a_taxe_t2", "a_taxe_t3", "a_taxe_t4", "a_taxe_total",
            "a_abo_ht", "a_abo_ht_t1", "a_abo_ht_t2", "a_abo_ht_t3", "a_abo_ht_t4", "a_abo_ht_total",
            "a_abo_ttc", "a_tranche_1", "a_tranche_2", "a_tranche_3", "a_tranche_4",
            "a_total_dep_ttc_hors_abo", "a_montant_facture_ttc",
            
            # Colonnes eau potable + assainissement (epa)
            "epa_abonnement", "epa_t1", "epa_t2", "epa_t3", "epa_t4", "epa_total",
            "epa_taxe_forfaitaire", "epa_taxe_t1", "epa_taxe_t2", "epa_taxe_t3", "epa_taxe_t4", "epa_taxe_total",
            "epa_abo_ht", "epa_abo_ht_t1", "epa_abo_ht_t2", "epa_abo_ht_t3", "epa_abo_ht_t4", "epa_abo_ht_total",
            "epa_abo_ttc", "epa_tranche_1", "epa_tranche_2", "epa_tranche_3", "epa_tranche_4",
            "epa_total_dep_ttc_hors_abo", "epa_montant_facture_ttc"
        ]

    def get_prix_tranches(self) -> dict[int, float]:
        """
        Retourne un dictionnaire des prix HT par tranche.
        
        Returns:
            dict[int, float]: Dictionnaire {numéro_tranche: prix_ht}
        """
        return {
            1: self.p_HT_Op_1,
            2: self.p_HT_Op_2,
            3: self.p_HT_Op_3,
            4: self.p_HT_Op_4,
            5: self.p_HT_Op_5
        }

    def get_seuils(self) -> dict[int, float]:
        """
        Retourne un dictionnaire des seuils de consommation.
        
        Returns:
            dict[int, float]: Dictionnaire {numéro_seuil: valeur_seuil}
        """
        return {
            1: self.t_ep_seuil_max_1,
            2: self.t_ep_seuil_max_2,
            3: self.t_ep_seuil_max_3
        }

    def create_dataframe_structure(self) -> pd.DataFrame:
        """
        Crée un DataFrame vide avec la structure complète et initialise la colonne id_projet
        avec l'attribut self.id_projet.
        
        Returns:
            pd.DataFrame: DataFrame vide avec la structure complète
        """
        # Création du DataFrame vide avec types appropriés
        df = pd.DataFrame(columns=self._colonnes)
        
        # Définition des types de données pour certaines colonnes clés
        df = df.astype({
            'id_projet': 'Int64',  # Utilise Int64 pour permettre les NaN
            'menage': 'Int64',
            'assaini': 'Int64',
            'consommation_m3_trim': 'float64'
        }, errors='ignore')  # ignore les erreurs si les colonnes n'existent pas encore
        
        return df

    def load_excel_data(self, filepath: str = "Facture_IBT_approchee_MP_data.xls", 
                       sheet_name: int = 0) -> pd.DataFrame:
        """
        Lit le fichier Excel et retourne le DataFrame avec colonnes normalisées.
        
        Args:
            filepath (str): Chemin vers le fichier Excel
            sheet_name (int): Numéro de la feuille à lire
            
        Returns:
            pd.DataFrame: DataFrame avec les données Excel
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            Exception: Pour toute autre erreur de lecture
        """
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier {filepath} n'existe pas.")
        
        try:
            effeco_manager = Effeco_facture_ibt_approchee_mp(filepath, sheet_name)
            effeco_manager.read_excel()
            return effeco_manager.get_dataframe()
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier Excel : {e}")

    def build_dataframe_with_excel(self, filepath: str = "Facture_IBT_approchee_MP_data.xls", 
                                  sheet_name: int = 0) -> pd.DataFrame:
        """
        Construit un DataFrame complet avec structure fixe et remplit les colonnes
        'menage', 'assaini', 'consommation_m3_trim' depuis le fichier Excel,
        et initialise 'id_projet' avec self.id_projet.
        
        Args:
            filepath (str): Chemin vers le fichier Excel
            sheet_name (int): Numéro de la feuille à lire
            
        Returns:
            pd.DataFrame: DataFrame complet avec données Excel et structure fixe
            
        Raises:
            ValueError: Si les colonnes requises sont manquantes dans le fichier Excel
        """
        # DataFrame vide avec toutes les colonnes
        df = self.create_dataframe_structure()
        
        # Lecture des données Excel
        df_excel = self.load_excel_data(filepath, sheet_name)
        
        # Vérification des colonnes requises
        required_columns = ["menage", "assaini", "conso_m3_trim"]
        missing_columns = [col for col in required_columns if col not in df_excel.columns]
        if missing_columns:
            raise ValueError(f"Colonnes manquantes dans le fichier Excel : {missing_columns}")
        
        # Copie des colonnes Excel dans le DataFrame complet
        df["menage"] = df_excel["menage"]
        df["assaini"] = df_excel["assaini"] 
        df["consommation_m3_trim"] = df_excel["conso_m3_trim"]
        
        # Initialisation de la colonne id_projet pour tous les enregistrements
        df["id_projet"] = self.id_projet
        
        # Application des règles de calcul
        df = self.apply_calculation_rules(df)
        
        return df

    def apply_calculation_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique toutes les règles de calcul pour la facturation IBT.
        
        Args:
            df (pd.DataFrame): DataFrame avec les colonnes de base
            
        Returns:
            pd.DataFrame: DataFrame avec tous les calculs effectués
        """
        # 1. Calculs des quantités par tranche
        df = self._calculate_quantities(df)
        
        # 2. Calculs eau potable (ep)
        df = self._calculate_ep_values(df)
        
        # 3. Calculs assainissement (a)
        df = self._calculate_a_values(df)
        
        # 4. Calculs eau potable + assainissement (epa)
        df = self._calculate_epa_values(df)
        
        return df

    def _calculate_quantities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule les quantités par tranche de consommation."""
        # q_01: MIN(consommation_m3_trim; t_ep_seuil_max_1)
        df["q_01"] = df["consommation_m3_trim"].clip(upper=self.t_ep_seuil_max_1)
        
        # calcul_c_t3: MAX(consommation_m3_trim - t_ep_seuil_max_1; 0)
        df["calcul_c_t3"] = (df["consommation_m3_trim"] - self.t_ep_seuil_max_1).clip(lower=0)
        
        # q_02: MIN(calcul_c_t3; t_ep_seuil_max_2 - t_ep_seuil_max_1)
        df["q_02"] = df["calcul_c_t3"].clip(upper=self.t_ep_seuil_max_2 - self.t_ep_seuil_max_1)
        
        # calcul_c_t4: MAX(consommation_m3_trim - t_ep_seuil_max_2; 0)
        df["calcul_c_t4"] = (df["consommation_m3_trim"] - self.t_ep_seuil_max_2).clip(lower=0)
        
        # q_03: MIN(calcul_c_t4; t_ep_seuil_max_3 - t_ep_seuil_max_2)
        df["q_03"] = df["calcul_c_t4"].clip(upper=self.t_ep_seuil_max_3 - self.t_ep_seuil_max_2)
        
        # q_04: MAX(consommation_m3_trim - t_ep_seuil_max_3; 0)
        df["q_04"] = (df["consommation_m3_trim"] - self.t_ep_seuil_max_3).clip(lower=0)
        
        return df

    def _calculate_ep_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule toutes les valeurs pour l'eau potable (ep)."""
        # Coûts de base
        df["ep_abonnement"] = self.p_HT_Op_1
        df["ep_t1"] = df["q_01"] * self.p_HT_Op_2
        df["ep_t2"] = df["q_02"] * self.p_HT_Op_3
        df["ep_t3"] = df["q_03"] * self.p_HT_Op_4
        df["ep_t4"] = df["q_04"] * self.p_HT_Op_5
        df["ep_total"] = df["ep_abonnement"] + df["ep_t1"] + df["ep_t2"] + df["ep_t3"] + df["ep_t4"]
        
        # Taxes
        df["ep_taxe_forfaitaire"] = self.tarif_ep_redevances
        df["ep_taxe_t1"] = self.redevances_accise_euro_m3 * df["q_01"]
        df["ep_taxe_t2"] = self.redevances_accise_euro_m3 * df["q_02"]
        df["ep_taxe_t3"] = self.redevances_accise_euro_m3 * df["q_03"]
        df["ep_taxe_t4"] = self.redevances_accise_euro_m3 * df["q_04"]
        df["ep_taxe_total"] = (df["ep_taxe_forfaitaire"] + df["ep_taxe_t1"] + 
                              df["ep_taxe_t2"] + df["ep_taxe_t3"] + df["ep_taxe_t4"])
        
        # TVA HT
        df["ep_abo_ht"] = self.mnt_tva_unite_1
        df["ep_abo_ht_t1"] = self.mnt_tva_unite_2 * df["q_01"]
        df["ep_abo_ht_t2"] = self.mnt_tva_unite_3 * df["q_02"]
        df["ep_abo_ht_t3"] = self.mnt_tva_unite_4 * df["q_03"]
        df["ep_abo_ht_t4"] = self.mnt_tva_unite_5 * df["q_04"]
        df["ep_abo_ht_total"] = (df["ep_abo_ht"] + df["ep_abo_ht_t1"] + 
                                df["ep_abo_ht_t2"] + df["ep_abo_ht_t3"] + df["ep_abo_ht_t4"])
        
        # Totaux TTC
        df["ep_abo_ttc"] = df["ep_abonnement"] + df["ep_taxe_forfaitaire"] + df["ep_abo_ht"]
        df["ep_tranche_1"] = df["ep_t1"] + df["ep_taxe_t1"] + df["ep_abo_ht_t1"]
        df["ep_tranche_2"] = df["ep_t2"] + df["ep_taxe_t2"] + df["ep_abo_ht_t2"]
        df["ep_tranche_3"] = df["ep_t3"] + df["ep_taxe_t3"] + df["ep_abo_ht_t3"]
        df["ep_tranche_4"] = df["ep_t4"] + df["ep_taxe_t4"] + df["ep_abo_ht_t4"]
        df["ep_total_dep_ttc_hors_abo"] = (df["ep_tranche_1"] + df["ep_tranche_2"] + 
                                          df["ep_tranche_3"] + df["ep_tranche_4"])
        df["ep_montant_facture_ttc"] = df["ep_total_dep_ttc_hors_abo"] + df["ep_abo_ttc"]
        
        return df

    def _calculate_a_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule toutes les valeurs pour l'assainissement (a)."""
        # Coûts de base
        df["a_abonnement"] = df["assaini"] * self.prix_h_tva_1
        df["a_t1"] = df["assaini"] * df["q_01"] * self.prix_h_tva_2
        df["a_t2"] = df["assaini"] * df["q_02"] * self.prix_h_tva_3
        df["a_t3"] = df["assaini"] * df["q_03"] * self.prix_h_tva_4
        df["a_t4"] = df["assaini"] * df["q_04"] * self.prix_h_tva_5
        df["a_total"] = df["a_abonnement"] + df["a_t1"] + df["a_t2"] + df["a_t3"] + df["a_t4"]
        
        # Taxes
        df["a_taxe_forfaitaire"] = df["assaini"] * self.redevances_abonnement
        df["a_taxe_t1"] = df["assaini"] * self.redevances_accise_eur_m3 * df["q_01"]
        df["a_taxe_t2"] = df["assaini"] * self.redevances_accise_eur_m3 * df["q_02"]
        df["a_taxe_t3"] = df["assaini"] * self.redevances_accise_eur_m3 * df["q_03"]
        df["a_taxe_t4"] = df["assaini"] * self.redevances_accise_eur_m3 * df["q_04"]
        df["a_taxe_total"] = (df["a_taxe_forfaitaire"] + df["a_taxe_t1"] + 
                             df["a_taxe_t2"] + df["a_taxe_t3"] + df["a_taxe_t4"])
        
        # TVA HT
        df["a_abo_ht"] = df["assaini"] * self.montant_tva_1
        df["a_abo_ht_t1"] = df["assaini"] * self.montant_tva_2 * df["q_01"]
        df["a_abo_ht_t2"] = df["assaini"] * self.montant_tva_3 * df["q_02"]
        df["a_abo_ht_t3"] = df["assaini"] * self.montant_tva_4 * df["q_03"]
        df["a_abo_ht_t4"] = df["assaini"] * self.montant_tva_5 * df["q_04"]
        df["a_abo_ht_total"] = (df["a_abo_ht"] + df["a_abo_ht_t1"] + 
                               df["a_abo_ht_t2"] + df["a_abo_ht_t3"] + df["a_abo_ht_t4"])
        
        # Totaux TTC
        df["a_abo_ttc"] = df["a_abonnement"] + df["a_taxe_forfaitaire"] + df["a_abo_ht"]
        df["a_tranche_1"] = df["a_t1"] + df["a_taxe_t1"] + df["a_abo_ht_t1"]
        df["a_tranche_2"] = df["a_t2"] + df["a_taxe_t2"] + df["a_abo_ht_t2"]
        df["a_tranche_3"] = df["a_t3"] + df["a_taxe_t3"] + df["a_abo_ht_t3"]
        df["a_tranche_4"] = df["a_t4"] + df["a_taxe_t4"] + df["a_abo_ht_t4"]
        df["a_total_dep_ttc_hors_abo"] = (df["a_tranche_1"] + df["a_tranche_2"] + 
                                         df["a_tranche_3"] + df["a_tranche_4"])
        df["a_montant_facture_ttc"] = df["a_total_dep_ttc_hors_abo"] + df["a_abo_ttc"]
        
        return df

    def _calculate_epa_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule toutes les valeurs combinées eau potable + assainissement (epa)."""
        df["epa_abonnement"] = df["ep_abonnement"] + df["a_abonnement"]
        df["epa_t1"] = df["ep_t1"] + df["a_t1"]
        df["epa_t2"] = df["ep_t2"] + df["a_t2"]
        df["epa_t3"] = df["ep_t3"] + df["a_t3"]
        df["epa_t4"] = df["ep_t4"] + df["a_t4"]
        df["epa_total"] = df["ep_total"] + df["a_total"]
        
        df["epa_taxe_forfaitaire"] = df["ep_taxe_forfaitaire"] + df["a_taxe_forfaitaire"]
        df["epa_taxe_t1"] = df["ep_taxe_t1"] + df["a_taxe_t1"]
        df["epa_taxe_t2"] = df["ep_taxe_t2"] + df["a_taxe_t2"]
        df["epa_taxe_t3"] = df["ep_taxe_t3"] + df["a_taxe_t3"]
        df["epa_taxe_t4"] = df["ep_taxe_t4"] + df["a_taxe_t4"]
        df["epa_taxe_total"] = df["ep_taxe_total"] + df["a_taxe_total"]
        
        df["epa_abo_ht"] = df["ep_abo_ht"] + df["a_abo_ht"]
        df["epa_abo_ht_t1"] = df["ep_abo_ht_t1"] + df["a_abo_ht_t1"]
        df["epa_abo_ht_t2"] = df["ep_abo_ht_t2"] + df["a_abo_ht_t2"]
        df["epa_abo_ht_t3"] = df["ep_abo_ht_t3"] + df["a_abo_ht_t3"]
        df["epa_abo_ht_t4"] = df["ep_abo_ht_t4"] + df["a_abo_ht_t4"]
        df["epa_abo_ht_total"] = df["ep_abo_ht_total"] + df["a_abo_ht_total"]
        
        df["epa_abo_ttc"] = df["ep_abo_ttc"] + df["a_abo_ttc"]
        df["epa_tranche_1"] = df["ep_tranche_1"] + df["a_tranche_1"]
        df["epa_tranche_2"] = df["ep_tranche_2"] + df["a_tranche_2"]
        df["epa_tranche_3"] = df["ep_tranche_3"] + df["a_tranche_3"]
        df["epa_tranche_4"] = df["ep_tranche_4"] + df["a_tranche_4"]
        df["epa_total_dep_ttc_hors_abo"] = df["ep_total_dep_ttc_hors_abo"] + df["a_total_dep_ttc_hors_abo"]
        df["epa_montant_facture_ttc"] = df["ep_montant_facture_ttc"] + df["a_montant_facture_ttc"]
        
        return df

    def get_dataframe_info(self, df: pd.DataFrame) -> dict:
        """
        Retourne des informations sur le DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame à analyser
            
        Returns:
            dict: Informations sur le DataFrame
        """
        return {
            "nombre_lignes": len(df),
            "nombre_colonnes": len(df.columns),
            "colonnes_avec_donnees": df.notna().any().sum(),
            "colonnes_vides": df.isna().all().sum(),
            "types_colonnes": df.dtypes.to_dict()
        }

    def __str__(self) -> str:
        """Représentation string de la classe."""
        return f"EffecoFIbtAppMpCp(id_projet={self.id_projet}, seuils={self.get_seuils()})"

    def __repr__(self) -> str:
        """Représentation pour débogage."""
        return self.__str__()


def main():
    """Fonction principale pour tester la classe."""
    # Initialisation des paramètres
    params = EffecoFIbtAppMpCp(id_projet=1)
    print(f"Paramètres initialisés : {params}")
    print(f"Prix par tranches : {params.get_prix_tranches()}")
    print(f"Seuils : {params.get_seuils()}")
    
    # Construction du DataFrame complet avec les données Excel
    try:
        df_full = params.build_dataframe_with_excel()
        print("\nDataFrame complet avec données Excel et calculs :")
        print(df_full.head())
        
        # Affichage de quelques colonnes calculées pour vérification
        print(f"\nExemple de calculs (première ligne) :")
        if len(df_full) > 0:
            print(f"  Consommation : {df_full['consommation_m3_trim'].iloc[0]:.2f} m³")
            print(f"  q_01 : {df_full['q_01'].iloc[0]:.2f} m³")
            print(f"  q_02 : {df_full['q_02'].iloc[0]:.2f} m³")
            print(f"  q_03 : {df_full['q_03'].iloc[0]:.2f} m³")
            print(f"  q_04 : {df_full['q_04'].iloc[0]:.2f} m³")
            print(f"  Montant facture EP TTC : {df_full['ep_montant_facture_ttc'].iloc[0]:.2f} €")
            print(f"  Montant facture A TTC : {df_full['a_montant_facture_ttc'].iloc[0]:.2f} €")
            print(f"  Montant facture EPA TTC : {df_full['epa_montant_facture_ttc'].iloc[0]:.2f} €")
        
        print(f"\nInformations sur le DataFrame :")
        info = params.get_dataframe_info(df_full)
        for key, value in info.items():
            if key != 'types_colonnes':  # On évite d'afficher tous les types
                print(f"  {key}: {value}")
            
    except FileNotFoundError as e:
        print(f"Erreur de fichier : {e}")
    except ValueError as e:
        print(f"Erreur de données : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()