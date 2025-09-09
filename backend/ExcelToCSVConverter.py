import pandas as pd
import os
import numpy as np

class ExcelToCSVConverter:
    def __init__(self, input_file_path, output_file_path=None):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path or self._generate_output_path()
        self.df = None
        self.column_names = []
        
    def _generate_output_path(self):
        base_name = os.path.splitext(self.input_file_path)[0]
        return f"{base_name}.csv"
    
    def read_excel_with_custom_header(self, sheet_name=0, header_row=0):
        """
        Lit le fichier Excel en extrayant les noms de colonnes corrects
        """
        try:
            # Lire le fichier sans header pour voir la structure
            df_raw = pd.read_excel(self.input_file_path, 
                                 sheet_name=sheet_name, 
                                 engine='xlrd',
                                 header=None)
            
            print(f"Shape du fichier brut: {df_raw.shape}")
            
            # Afficher les premières lignes pour comprendre la structure
            print("=== STRUCTURE DU FICHIER ===")
            for i in range(min(10, len(df_raw))):
                print(f"Ligne {i}: {df_raw.iloc[i].tolist()}")
            
            # Extraire les noms de colonnes - ils semblent être dans différentes cellules
            # Basé sur votre output, les colonnes sont dispersées
            self._extract_column_names(df_raw)
            
            # Maintenant lire les données réelles (à partir de la ligne où commencent les données)
            self.df = pd.read_excel(self.input_file_path,
                                  sheet_name=sheet_name,
                                  engine='xlrd',
                                  header=None,
                                  skiprows=self._find_data_start_row(df_raw))
            
            # Appliquer les noms de colonnes
            if len(self.column_names) == self.df.shape[1]:
                self.df.columns = self.column_names
            else:
                print(f"Warning: {len(self.column_names)} noms de colonnes mais {self.df.shape[1]} colonnes")
                # Créer des noms de colonnes par défaut
                self.df.columns = [f'col_{i}' for i in range(self.df.shape[1])]
            
            print(f"DataFrame final shape: {self.df.shape}")
            return self.df
            
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            raise
    
    def _extract_column_names(self, df_raw):
        """Extrait les noms de colonnes de la structure complexe"""
        # Basé sur votre description, les noms de colonnes sont dispersés
        # Essayons de les collecter à partir des premières lignes
        
        column_names = []
        
        # Parcourir les premières lignes pour trouver les noms de colonnes
        for row_idx in range(min(20, len(df_raw))):
            row = df_raw.iloc[row_idx].dropna().tolist()
            if any('id_projet' in str(cell) for cell in row if pd.notna(cell)):
                # Trouvé la ligne avec les noms de colonnes
                print(f"Noms de colonnes trouvés à la ligne {row_idx}: {row}")
                column_names = [str(cell).strip() for cell in df_raw.iloc[row_idx] if pd.notna(cell)]
                break
        
        if not column_names:
            # Si pas trouvé, utiliser la liste fournie manuellement
            column_names = [
                "id_projet", "menage", "tailledelafamille", "nbreenfants", "nbreadultes", 
                "revenunetmois", "ucoxford", "ucocde", "niveaudevieoxford", "niveaudevieocde",
                "poor_oxford", "poor_ocde", "assaini", "sep_t0_ibt_ep", "sep_tmin_ibt_ep",
                "sep_t_ibt_ep", "sep_t_ibt_pp_ep", "sep_t0_tbse_ep", "sep_tmin_tbse_ep",
                "sep_t_tbse_ep", "a_t0_ibt", "a_tmin_ibt", "a_t_ibt", "a_t_ibt_pp", "a_t0_tbse",
                "a_tmin_tbse", "a_t_tbse", "sepa_t0_ibt", "sepa_tmin_ibt", "sepa_t_ibt",
                "sepa_t_ibt_pp", "sepa_t0_tbse", "sepa_tmin_tbse", "sepa_t_tbse", "par_ibt",
                "par_tbse", "par_ibt_1", "par_tbse_1", "par_ibt_2", "par_tbse_2", "par_ibt_3",
                "par_tbse_3", "seuil_depenses_trim_par_pct_3_r", "exces_dep_0_inclus_ibt",
                "exces_dep_0_inclus_tbse", "lz_ina_tbse_menage", "lz_ina_tbse_exces_dep_tbse",
                "lz_ina_tbse_rg_normalise", "lz_ina_tbse_alpha", "lz_ina_tbse_l_tbse",
                "cc_ina_nv_tbse_menage", "cc_ina_nv_tbse_nivvie_ocde", "cc_ina_nv_tbse_rg_nivvie",
                "cc_ina_nv_tbse_rg_ina_tbse", "cc_ina_nv_tbse_excdep_tbse", "cc_ina_nv_tbse_alpha",
                "cc_ina_nv_tbse_c_tbse", "lz_ina_ibt_menage", "lz_ina_ibt_exces_dep_ibt",
                "lz_ina_ibt_rg_normalise_ibt", "lz_ina_ibt_alpha", "lz_ina_ibt_l_ibt",
                "cc_ina_nivvie_ibt_menage", "cc_ina_nivvie_ibt_niveau_de_vie_ocde",
                "cc_ina_nivvie_ibt_rang_nor_niveau_de_vie", "cc_ina_nivvie_ibt_rg_inab_ibt",
                "cc_ina_nivvie_ibt_exces_dep_ibt", "cc_ina_nivvie_ibt_alpha", "cc_ina_nivvie_ibt_c_ibt",
                "cc_gen_rang", "cc_gen_cg_tbse", "cc_gen_cg_ibt"
            ]
            print("Utilisation des noms de colonnes manuels")
        
        self.column_names = column_names
        print(f"Noms de colonnes extraits: {len(column_names)} colonnes")
    
    def _find_data_start_row(self, df_raw):
        """Trouve la ligne où commencent les données réelles"""
        for row_idx in range(len(df_raw)):
            # Chercher une ligne avec des données numériques ou des ID
            row = df_raw.iloc[row_idx]
            if len(row.dropna()) > 3:  # Au moins 4 cellules non vides
                # Vérifier si c'est probablement une ligne de données
                if any(str(cell).isdigit() for cell in row if pd.notna(cell)):
                    print(f"Données trouvées à la ligne {row_idx}")
                    return row_idx
        return 0  # Commencer depuis le début si pas trouvé
    
    def validate_data(self):
        if self.df is None:
            raise ValueError("Aucune donnée chargée")
        
        print("=== VALIDATION ===")
        print(f"Shape: {self.df.shape}")
        print(f"Colonnes: {list(self.df.columns)}")
        print("\n=== TYPES ===")
        print(self.df.dtypes.head(10))
        print("\n=== ÉCHANTILLON ===")
        print(self.df.head(3))
    
    def convert_to_csv(self, index=False, encoding='utf-8-sig'):
        if self.df is None:
            raise ValueError("Aucune donnée chargée")
        
        try:
            # Assurer le chemin de sortie
            if not os.path.dirname(self.output_file_path):
                self.output_file_path = os.path.join(os.getcwd(), self.output_file_path)
            
            self.df.to_csv(self.output_file_path, index=index, encoding=encoding)
            print(f"✅ CSV créé: {self.output_file_path}")
            return self.output_file_path
        except Exception as e:
            print(f"❌ Erreur CSV: {e}")
            raise

# Méthode alternative plus simple
def convert_excel_direct():
    """Méthode directe pour lire le fichier complexe"""
    try:
        # Lire tout le fichier
        df = pd.read_excel("VARPARMENAGEV3.xls", engine='xlrd', header=None)
        
        # Trouver la ligne avec les en-têtes
        header_row = None
        for i in range(len(df)):
            if 'id_projet' in str(df.iloc[i, 1]):  # Chercher dans la deuxième colonne
                header_row = i
                break
        
        if header_row is not None:
            # Extraire les en-têtes
            headers = []
            for col in range(df.shape[1]):
                cell_value = df.iloc[header_row, col]
                if pd.notna(cell_value):
                    headers.append(str(cell_value).strip())
                else:
                    headers.append(f"col_{col}")
            
            # Lire les données
            data_df = pd.read_excel("VARPARMENAGEV3.xls", engine='xlrd', 
                                  header=None, skiprows=header_row + 1)
            data_df.columns = headers[:data_df.shape[1]]
            
            # Sauvegarder
            data_df.to_csv("VARPARMENAGEV3.csv", index=False, encoding='utf-8-sig')
            print("Conversion réussie avec méthode alternative")
            return data_df
        
    except Exception as e:
        print(f"Erreur méthode alternative: {e}")
        return None

def main():
    print("Début de la conversion...")
    
    # Essayer d'abord la méthode alternative
    print("1. Tentative avec méthode alternative...")
    result = convert_excel_direct()
    
    if result is not None:
        print("✅ Succès avec méthode alternative!")
        return
    
    # Sinon utiliser la classe
    print("2. Tentative avec la classe...")
    converter = ExcelToCSVConverter("VARPARMENAGEV3.xls")
    
    try:
        df = converter.read_excel_with_custom_header()
        converter.validate_data()
        converter.convert_to_csv()
        print("✅ Conversion terminée!")
        
    except Exception as e:
        print(f"❌ Échec: {e}")
        print("\n💡 Suggestions:")
        print("1. Ouvrez le fichier dans Excel et vérifiez sa structure")
        print("2. Enregistrez-le manuellement en CSV depuis Excel")
        print("3. Vérifiez que le fichier n'est pas corrompu")

if __name__ == "__main__":
    # Vérifier l'installation de xlrd
    try:
        import xlrd
    except ImportError:
        print("Installation de xlrd...")
        os.system("pip install xlrd")
    
    main()