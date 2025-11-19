import pandas as pd
import unicodedata

class Effeco_facture_ibt_approchee_mp:
    def __init__(self, filepath: str = "Facture_IBT_approchee_MP_data.xls", sheet_name: int = 0):
        """
        Classe pour lire le fichier Excel Facture_IBT_approchee_MP_data.xls
        et construire un DataFrame avec les colonnes : menage, assaini, conso_m3_trim.

        :param filepath: chemin du fichier Excel (par défaut Facture_IBT_approchee_MP_data.xls)
        :param sheet_name: index ou nom de la feuille à lire (0 = première feuille par défaut)
        """
        self.filepath = filepath
        self.sheet_name = sheet_name
        self.df = None

    def _normalize_column(self, col_name: str) -> str:
        """
        Nettoie le nom de colonne : minuscules, suppression espaces et accents.
        """
        col_name = col_name.strip().lower()
        col_name = ''.join(c for c in unicodedata.normalize('NFKD', col_name) if not unicodedata.combining(c))
        return col_name

    def read_excel(self):
        """
        Lecture du fichier Excel et création du DataFrame avec colonnes normalisées.
        """
        try:
            self.df = pd.read_excel(self.filepath, sheet_name=self.sheet_name)

            # Normalisation des noms de colonnes
            self.df.columns = [self._normalize_column(col) for col in self.df.columns]

            # Vérification des colonnes attendues
            expected_cols = ["menage", "assaini", "conso_m3_trim"]
            missing = [col for col in expected_cols if col not in self.df.columns]
            if missing:
                raise ValueError(f"Colonnes manquantes dans le fichier Excel : {missing}")

        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture du fichier Excel : {e}")

    def get_dataframe(self) -> pd.DataFrame:
        """
        Retourne le DataFrame construit.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        return self.df


# Exemple d’utilisation
if __name__ == "__main__":
    reader = Effeco_facture_ibt_approchee_mp()
    reader.read_excel()
    df = reader.get_dataframe()
    print(df.head())
