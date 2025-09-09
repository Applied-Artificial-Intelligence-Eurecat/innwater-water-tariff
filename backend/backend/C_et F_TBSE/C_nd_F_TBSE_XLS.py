import pandas as pd

class C_nd_F_TBSE_XLS:
    """
    Classe pour lire un fichier Excel 'C_nd_F_TBSE.xls' structuré avec le schéma donné.
    """

    EXPECTED_COLUMNS = [
        "id_projet", "cons_menage", "cons_ln_part_captive", "cons_m3_jour", "cons_m3_trim",
        "cons_assaini", "c_var_revenu", "c_var_revenuJour", "c_var_abTTC", "c_var_abTTCJour",
        "c_var_revMoinsF3", "c_var_revMoinsFJour", "c_var_b1LnP", "c_var_b2LnRF",
        "cons_tbse_somme_ln", "cons_tbse_m3_jour", "cons_tbse_m3_trim",
        "f_tbse_part_op", "f_tbse_part_agence", "f_tbse_part_etat", "f_tbse_total",
        "f_ep_epa_ep_f_p_op", "f_ep_epa_ep_f_p_ag", "f_ep_epa_ep_f_p_etat", "f_ep_epa_ep_f_total_pf",
        "f_ep_epa_ep_var_p_op", "f_ep_epa_ep_var_p_ag", "f_ep_epa_ep_var_p_etat", "f_ep_epa_ep_var_total_pv",
        "f_ep_epa_ep_fndVar_p_op", "f_ep_epa_ep_fndVar_p_ag", "f_ep_epa_ep_fndVar_p_etat",
        "f_ep_epa_ep_fndVar_f_ep_ttc", "f_ep_epa_ep_fndVar_f_ep_ttc_verif",
        "f_ep_epa_a_f_p_op", "f_ep_epa_a_f_p_ag", "f_ep_epa_a_f_p_etat", "f_ep_epa_a_f_total_pf",
        "f_ep_epa_a_var_p_op", "f_ep_epa_a_var_p_ag", "f_ep_epa_a_var_p_etat", "f_ep_epa_a_var_totalPV",
        "f_ep_epa_a_fndVar_p_op", "f_ep_epa_a_fndVar_p_ag", "f_ep_epa_a_fndVar_p_etat",
        "f_ep_epa_a_fndVar_f_A_TTC", "f_ep_epa_a_fndVar_f_A_TTC_Verif",
        "f_ep_epaep_afp_op", "f_ep_epaep_afp_ag", "f_ep_epaep_afp_etat", "f_ep_epaep_aftotalPF",
        "f_ep_epa_ep_a_var_p_op", "f_ep_epa_ep_a_var_p_ag", "f_ep_epa_ep_a_var_p_etat", "f_ep_epa_ep_a_var_totalPV",
        "f_ep_epa_ep_a_fndVar_p_op", "f_ep_epa_ep_a_fndVar_p_ag", "f_ep_epa_ep_a_fndVar_p_etat",
        "f_ep_epa_ep_a_fndVar_f_EP_APA_TTC", "f_ep_epa_ep_a_fndVar_f_EP_APA_TTC_Verif",
        "verifvs"
    ]

    def __init__(self, filepath: str = "C_nd_F_TBSE.xls"):
        self.filepath = filepath
        self.df = None

    def load_excel(self):
        """Charge le fichier Excel et vérifie les colonnes."""
        try:
            self.df = pd.read_excel(self.filepath)
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du fichier Excel : {e}")

        # Vérification des colonnes
        missing_cols = [col for col in self.EXPECTED_COLUMNS if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans le fichier Excel : {missing_cols}")

        print("✅ Fichier chargé avec succès et toutes les colonnes sont présentes.")
        return self.df

    def get_project_by_id(self, project_id):
        """Retourne les données pour un projet spécifique via son id_projet."""
        if self.df is None:
            raise ValueError("Le fichier n'a pas encore été chargé.")
        
        project_data = self.df[self.df["id_projet"] == project_id]
        if project_data.empty:
            print(f"Aucun projet trouvé avec l'id {project_id}.")
            return None
        return project_data.to_dict(orient="records")[0]

    def get_all_projects(self):
        """Retourne la liste de tous les projets sous forme de dictionnaires."""
        if self.df is None:
            raise ValueError("Le fichier n'a pas encore été chargé.")
        return self.df.to_dict(orient="records")


def main():
    # Création de l'objet avec le fichier par défaut
    reader = C_nd_F_TBSE_XLS()
    
    # Chargement du fichier
    try:
        df = reader.load_excel()
        print(f"Nombre de projets trouvés : {len(df)}")
    except ValueError as e:
        print(e)
        return
    
    # Exemple : afficher un projet avec id = 1
    projet = reader.get_project_by_id(1)
    if projet:
        print("Projet ID=1 :", projet)


if __name__ == "__main__":
    main()
