import pandas as pd

class sub_Tax_Input_Consom_service:
    """
    Service de filtrage de DataFrame pour extraire
    les colonnes nécessaires aux calculs de consommation et taxes.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialise le service avec une DataFrame complète.
        """
        self.dataframe = dataframe

    def get_sub_dataframe(self) -> pd.DataFrame:
        """
        Renvoie la sous-DataFrame contenant uniquement
        les colonnes d'intérêt.
        """
        required_columns = [
            'Assainissement Collectif (1 = oui)',
            'i_new',
            'Facture_IBT_C_BCP F',
            'Facture_IBT_C_BCP H',
            'Facture_IBT_C_BCP J',
            'Facture_IBT_C_BCP K'
        ]

        # Vérifie la présence des colonnes nécessaires
        missing = [col for col in required_columns if col not in self.dataframe.columns]
        if missing:
            raise KeyError(f"Colonnes manquantes dans la DataFrame : {missing}")

        # Retourne une copie de la sous-DataFrame filtrée
        return self.dataframe[required_columns].copy()


# === Exemple d'utilisation ===
if __name__ == "__main__":
    # Exemple : DataFrame complète simulée
    df_complete = pd.DataFrame({
        'Assainissement Collectif (1 = oui)': [1, 0, 1],
        'i_new': [10, 20, 30],
        'Facture_IBT_C_BCP F': [100, 200, 150],
        'Facture_IBT_C_BCP H': [110, 210, 160],
        'Facture_IBT_C_BCP J': [120, 220, 170],
        'Facture_IBT_C_BCP K': [130, 230, 180],
        'Autre_colonne': [999, 888, 777]
    })

    service = sub_Tax_Input_Consom_service(df_complete)
    sub_df = service.get_sub_dataframe()

    print("✅ Sous-DataFrame extraite :")
    print(sub_df)
