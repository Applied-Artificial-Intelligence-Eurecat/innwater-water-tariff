import pandas as pd
import unicodedata


# TODO : Replace the data in the Excel file with the elements from the simulator's general context.
class Effeco_facture_ibt_approchee_PP:
    def __init__(self, filepath: str = "Facture_IBT_approchee_PP_data.xls", sheet_name: int = 0):
        """
        Classe pour lire le fichier Excel Facture_IBT_approchee_PP_data.xls
        et construire un DataFrame avec les colonnes : menage, assaini, C_m3_trim.
        :param filepath: chemin du fichier Excel (par défaut Facture_IBT_approchee_PP_data.xls)
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
            
            # Vérification des colonnes attendues (adaptées pour PP)
            expected_cols = ["menage", "assaini", "c_m3_trim"]
            missing = [col for col in expected_cols if col not in self.df.columns]
            
            if missing:
                print(f"Colonnes disponibles: {list(self.df.columns)}")
                raise ValueError(f"Colonnes manquantes dans le fichier Excel : {missing}")
                
            print(f"Fichier Excel lu avec succès : {len(self.df)} lignes chargées")
            print(f"Colonnes trouvées : {list(self.df.columns)}")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier {self.filepath} n'a pas été trouvé")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture du fichier Excel : {e}")

    def get_dataframe(self) -> pd.DataFrame:
        """
        Retourne le DataFrame construit.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        return self.df

    def get_info(self) -> dict:
        """
        Retourne des informations sur le DataFrame.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        
        return {
            "nombre_lignes": len(self.df),
            "nombre_colonnes": len(self.df.columns),
            "colonnes": list(self.df.columns),
            "types_donnees": dict(self.df.dtypes),
            "valeurs_manquantes": dict(self.df.isnull().sum())
        }

    def get_summary(self) -> pd.DataFrame:
        """
        Retourne un résumé statistique des données numériques.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        
        # Sélection des colonnes numériques
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            return self.df[numeric_cols].describe()
        else:
            print("Aucune colonne numérique trouvée")
            return pd.DataFrame()

    def filter_by_menage(self, menage_id) -> pd.DataFrame:
        """
        Filtre les données par ID de ménage.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        
        return self.df[self.df['menage'] == menage_id]

    def get_unique_menages(self) -> list:
        """
        Retourne la liste des ménages uniques.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        
        return sorted(self.df['menage'].unique().tolist())

    def export_to_csv(self, output_path: str = "facture_pp_export.csv"):
        """
        Exporte le DataFrame vers un fichier CSV.
        """
        if self.df is None:
            raise ValueError("Le DataFrame n'a pas encore été créé. Utilise read_excel() d'abord.")
        
        self.df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Données exportées vers : {output_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Création de l'instance
        reader = Effeco_facture_ibt_approchee_PP()
        
        # Lecture du fichier Excel
        reader.read_excel()
        
        # Récupération du DataFrame
        df = reader.get_dataframe()
        
        # Affichage des premières lignes
        print("\n=== APERÇU DES DONNÉES ===")
        print(df.head())
        
        # Informations sur le DataFrame
        print("\n=== INFORMATIONS SUR LES DONNÉES ===")
        info = reader.get_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Résumé statistique
        print("\n=== RÉSUMÉ STATISTIQUE ===")
        summary = reader.get_summary()
        if not summary.empty:
            print(summary)
        
        # Ménages uniques
        print("\n=== MÉNAGES UNIQUES ===")
        menages = reader.get_unique_menages()
        print(f"Nombre de ménages uniques : {len(menages)}")
        print(f"Premiers ménages : {menages[:10] if len(menages) > 10 else menages}")
        
        # Exemple de filtrage par ménage (utilise le premier ménage disponible)
        if menages:
            print(f"\n=== DONNÉES POUR LE MÉNAGE {menages[0]} ===")
            menage_data = reader.filter_by_menage(menages[0])
            print(menage_data)
        
    except Exception as e:
        print(f"Erreur : {e}")