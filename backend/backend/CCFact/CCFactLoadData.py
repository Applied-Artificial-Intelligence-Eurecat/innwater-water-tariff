import pandas as pd
from typing import Dict, Any, Optional
import logging

class CCFactLoadData:
    """Classe pour charger les données du fichier Excel CCFactdata.xls"""
    
    # Schéma des colonnes attendues
    EXPECTED_COLUMNS = [
        'id_projet', 'menage', 'assaini', 'constante', 'taille_famille', 'snwa', 'swim', 'garden_weather',
        'conso_captive_step_constante', 'conso_captive_step_taille_famille', 'conso_captive_step_snwa',
        'conso_captive_step_swim', 'conso_captive_step_garden_weather', 'conso_captive_step_total',
        'conso_captive_step_c_m3_jour', 'conso_captive_step_c_m3_trim', 'q01', 'calcul_c_t3', 'q02',
        'calcul_c_t4', 'q03', 'q04', 'rc_ep_ope_abt', 'rc_ep_ope_t1', 'rc_ep_ope_t2', 'rc_ep_ope_t3',
        'rc_ep_ope_t4', 'rc_ep_ope_total', 'rc_ep_agence_abt', 'rc_ep_agence_t1', 'rc_ep_agence_t2',
        'rc_ep_agence_t3', 'rc_ep_agence_t4', 'rc_ep_agence_total_abt', 'rc_ep_eta_abt', 'rc_ep_eta_t1',
        'rc_ep_eta_t2', 'rc_ep_eta_t3', 'rc_ep_eta_t4', 'rc_ep_eta_total_abt', 'dep_ep_tranches_abo_ttc',
        'dep_ep_tranches_1', 'dep_ep_tranches_2', 'dep_ep_tranches_3', 'dep_ep_tranches_4',
        'dep_ep_ttc_hors_abt', 'mnt_fact_ep_ttc', 'r_a_ope_abt', 'r_a_ope_t1', 'r_a_ope_t2', 'r_a_ope_t3',
        'r_a_ope_t4', 'r_a_ope_total_abt', 'r_a_agence_abt', 'r_a_agence_t1', 'r_a_agence_t2', 'r_a_agence_t3',
        'r_a_agence_t4', 'r_a_agence_total_abt', 'r_a_etat_abt', 'r_a_etat_t1', 'r_a_etat_t2', 'r_a_etat_t3',
        'r_a_etat_t4', 'r_a_etat_total_abt', 'd_a_abo_ttc', 'd_a_t1', 'd_a_t2', 'd_a_t3', 'd_a_t4', 'd_a_hors_abo',
        'mnt_fact_a_ttc', 'rc_ope_abt', 'rc_epa_ope_t1', 'rc_epa_ope_t2', 'rc_epa_ope_t3', 'rc_epa_ope_t4',
        'rc_epa_ope_total_abt', 'rc_epa_agence_abt', 'rc_epa_agence_t1', 'rc_epa_agence_t2', 'rc_epa_agence_t3',
        'rc_epa_agence_t4', 'rc_epa_agence_total_abt', 'rc_epa_etat_abt', 'rc_epa_etat_t1', 'rc_epa_etat_t2',
        'rc_epa_etat_t3', 'rc_epa_etat_t4', 'rc_epa_etat_total_abt', 'd_epa_ee_hors_ab_abo_ttc',
        'd_epa_ee_hors_ab_t1', 'd_epa_ee_hors_ab_t2', 'd_epa_ee_hors_ab_t3', 'd_epa_ee_hors_ab_t4',
        'd_epa_ee_hors_ab_d_ee_ttc_hors_ab', 'm_epa_fact_ee_ttc', 'ep_fixe_op', 'ep_fixe_agence', 'ep_fixe_etat',
        'ep_fixe_total', 'ep_variable_op', 'ep_variable_agence', 'ep_variable_etat', 'ep_variable_total',
        'ep_total_op', 'ep_total_agence', 'ep_total_etat', 'ep_total_mnt_fact_ep_ttc', 'ep_verif_mnt_fact_ep_ttc',
        'assain_fixe_op', 'assain_fixe_agence', 'assain_fixe_etat', 'assain_fixe_total', 'assain_variable_op',
        'assain_variable_agence', 'assain_variable_etat', 'assain_variable_total', 'assain_total_op',
        'assain_total_agence', 'assain_total_etat', 'assain_total_mnt_fact_a_ttc', 'assain_verif_mnt_fact_a_ttc',
        's_epa_fixe_op', 's_epa_fixe_agence', 's_epa_fixe_etat', 's_epa_fixe_total', 's_epa_variable_op',
        's_epa_variable_agence', 's_epa_variable_etat', 's_epa_variable_total', 's_epa_total_op',
        's_epa_total_agence', 's_epa_total_etat', 's_epa_total_mnt_fact_epa_ttc', 's_epa_verif_mnt_fact_epa_ttc'
    ]
    
    def __init__(self, file_path: str = "CCFactdata.xls"):
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(__name__)
    
    def load_data(self) -> pd.DataFrame:
        """
        Charge les données depuis le fichier Excel
        
        Returns:
            pd.DataFrame: DataFrame contenant les données
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le schéma ne correspond pas
        """
        try:
            # Chargement du fichier Excel
            self.logger.info(f"Chargement du fichier {self.file_path}")
            self.data = pd.read_excel(self.file_path)
            
            # Validation du schéma
            self._validate_schema()
            
            self.logger.info(f"Données chargées avec succès. Shape: {self.data.shape}")
            return self.data
            
        except FileNotFoundError:
            error_msg = f"Fichier non trouvé: {self.file_path}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement: {str(e)}")
            raise
    
    def _validate_schema(self) -> None:
        """Valide que le schéma du fichier correspond aux attentes"""
        if self.data is None:
            raise ValueError("Aucune donnée chargée")
        
        missing_columns = set(self.EXPECTED_COLUMNS) - set(self.data.columns)
        extra_columns = set(self.data.columns) - set(self.EXPECTED_COLUMNS)
        
        if missing_columns:
            error_msg = f"Colonnes manquantes: {missing_columns}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        if extra_columns:
            self.logger.warning(f"Colonnes supplémentaires détectées: {extra_columns}")
    
    def get_data(self) -> pd.DataFrame:
        """Retourne les données chargées"""
        if self.data is None:
            raise ValueError("Les données n'ont pas été chargées. Appelez load_data() d'abord.")
        return self.data
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne des informations sur les données chargées"""
        if self.data is None:
            return {"status": "non_chargé"}
        
        return {
            "status": "chargé",
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "missing_values": self.data.isnull().sum().to_dict(),
            "dtypes": self.data.dtypes.to_dict()
        }

# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Instance de la classe
        loader = CCFactLoadData("CCFactdata.xls")
        
        # Chargement des données
        data = loader.load_data()
        
        # Affichage des informations
        info = loader.get_info()
        print(f"Données chargées: {info['shape']}")
        print(f"Colonnes: {len(info['columns'])}")
        
        # Aperçu des données
        print("\nAperçu des données:")
        print(data.head())
        
    except Exception as e:
        print(f"Erreur: {e}")