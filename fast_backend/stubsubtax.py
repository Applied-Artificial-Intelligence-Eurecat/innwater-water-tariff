import pandas as pd

class ExcelLister:
    """
    Classe autonome permettant de lire et d’afficher un fichier Excel
    ayant la structure :
    Menage | Assaini | C_T1 | C_T2 | C_T3 | C_T4
    """

    EXPECTED_COLUMNS = ["Menage", "Assaini", "C_T1", "C_T2", "C_T3", "C_T4"]

    def __init__(self, file_path: str, n_preview: int = 10):
        """
        Initialise la classe :
        - charge le fichier Excel,
        - vérifie la structure,
        - affiche un aperçu et le nombre d’enregistrements.
        """
        self.file_path = file_path
        self.n_preview = n_preview
        self.data = None

        print(f"📂 Fichier cible : {self.file_path}")

        # Étape 1 : lecture du fichier
        try:
            self.data = pd.read_excel(self.file_path)
            print("✅ Fichier lu avec succès.")
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ Fichier introuvable : {self.file_path}")
        except Exception as e:
            raise ValueError(f"⚠️ Erreur lors de la lecture du fichier : {e}")

        # Étape 2 : vérification des colonnes
        missing = [col for col in self.EXPECTED_COLUMNS if col not in self.data.columns]
        if missing:
            raise ValueError(f"⚠️ Colonnes manquantes dans le fichier : {missing}")
        else:
            self.data = self.data[self.EXPECTED_COLUMNS]
            print("✅ Structure du fichier validée.")

        # Étape 3 : aperçu automatique
        print("\n📊 Aperçu des données :")
        print(self.data.head(self.n_preview))

        # Étape 4 : affichage du nombre d’enregistrements
        print(f"\n📈 Nombre total d’enregistrements : {len(self.data)}")

    def list_as_dict(self):
        """Retourne les données sous forme de liste de dictionnaires."""
        return self.data.to_dict(orient="records")
    
    
    def get_dataframe(self):
        """Retourne le DataFrame complet."""
        return self.data



# === MAIN ===
if __name__ == "__main__":
    # Nom du fichier à lire
    file_path = "subTaxInputCom.xls"

    try:
        # Création automatique de l’objet → tout se fait dans __init__
        excel_lister = ExcelLister(file_path)

        # Exemple d’utilisation d’une autre méthode
        data_list = excel_lister.list_as_dict()
        print("\n🔍 Exemple de 2 premières lignes au format dictionnaire :")
        for row in data_list[:2]:
            print(row)

    except Exception as e:
        print(f"\n🚨 Erreur : {e}")
