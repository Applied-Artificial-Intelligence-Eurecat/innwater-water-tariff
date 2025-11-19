import pandas as pd
from ServiceASurplusAgrege import ServiceASurplusAgrege
from Effeco_DataFrameFilter import DataFrameFilter

class DataReaderExcel:
    def __init__(self, filepath: str, sheet_name: str = 0):
        self.filepath = filepath
        self.sheet_name = sheet_name
        self.data = None

    def load_data(self, convert_numeric: bool = True):
        """Charge les données Excel dans un DataFrame pandas."""
        try:
            self.data = pd.read_excel(self.filepath, sheet_name=self.sheet_name, dtype=str)
            print(f"✅ Données chargées : {self.data.shape[0]} lignes, {self.data.shape[1]} colonnes.")

            # Conversion automatique des colonnes numériques
            if convert_numeric:
                for col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors="ignore")
                print("🔹 Conversion automatique des colonnes numériques effectuée.")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du fichier : {e}")
            self.data = None

    def get_columns(self):
        if self.data is not None:
            return list(self.data.columns)
        return []

    def head(self, n: int = 5):
        return self.data.head(n) if self.data is not None else None

    def filter_by_column(self, column: str, value):
        if self.data is not None:
            if column in self.data.columns:
                return self.data[self.data[column] == value]
            else:
                print(f"⚠️ La colonne '{column}' n'existe pas.")
        return None
    

    def valeur_min_et_covariance(self, df: pd.DataFrame, col1: str, col2: str = None):
        """
        Affiche la plus petite valeur d'une colonne et sa covariance (optionnel).
        
        - Si col2 est None -> retourne min + variance de col1
        - Si col2 est donné -> retourne min + covariance col1/col2
        """
        if col1 not in df.columns:
            print(f"⚠️ Colonne '{col1}' introuvable.")
            return None

        min_val = df[col1].min()
        print(f"🔹 Valeur minimale de {col1} = {min_val}")

        if col2 is None:
            variance = df[col1].var()
            print(f"🔹 Variance de {col1} = {variance}")
            return {"min": min_val, "variance": variance}
        else:
            if col2 not in df.columns:
                print(f"⚠️ Colonne '{col2}' introuvable.")
                return {"min": min_val, "covariance": None}

            cov_val = df[[col1, col2]].cov().iloc[0,1]
            print(f"🔹 Covariance entre {col1} et {col2} = {cov_val}")
            return {"min": min_val, "covariance": cov_val}
        
    def sort_conso_asc(self, col: str = "conso_q_cout_complet_m3_trim", n: int = None):
        """
        Trie les données par consommation en ordre croissant.
        
        - col : nom de la colonne à trier (par défaut 'conso_q_cout_complet_m3_trim')
        - n   : si précisé, retourne seulement les n premières lignes
        """
        if self.data is not None:
            if col not in self.data.columns:
                print(f"⚠️ Colonne '{col}' introuvable.")
                return None

            df_sorted = self.data.sort_values(by=col, ascending=True)
            if n:
                return df_sorted.head(n)
            return df_sorted
        else:
            print("⚠️ Aucune donnée chargée.")
            return None


def main():
    filepath = "surplusagregeData3.xls"
    reader = DataReaderExcel(filepath)

    # Chargement avec conversion automatique des colonnes numériques
    reader.load_data(convert_numeric=True)

    if reader.data is not None:
        print("\n📌 Colonnes disponibles :")
        print(reader.get_columns())
        print("\n📌 Aperçu des 5 premières lignes :")
        print(reader.head())

        # Exemple de filtrage
        print("\n📌 Exemple de filtrage (menage == 12345) :")
        filtre = reader.filter_by_column("menage", 12345)
        print(filtre)

        # Création du service
        service = ServiceASurplusAgrege()

        # Choix de la colonne de consommation
        col_conso = "conso_q_cout_complet_m3_trim"
        col_delta_tbse_a_app= "delta_tbse_a_app"
        col_delta_ibt_a_approchee= "delta_ibt_a_approchee"
        col_t1_t2_euro_trim_ttc = "t1_t2_euro_trim_ttc"
        col_t1_t2_euro_trim_ter = "t1_t2_euro_trim_ter"
       

        

        nb_menages = service.compter_menages_distincts(reader.data, col_menage="menage")
        moyenne = service.moyenne_conso(reader.data, col_conso)

        print(f"\nNombre de ménages distincts : {nb_menages}")
        print(f"Moyenne de {col_conso} : {moyenne:.2f}")

        # 📊 Résumé des indicateurs
        resume = service.resume_statistiques(reader.data, col_conso)
        resumeZ6ZN = service.resume_statistiques(reader.data, col_delta_tbse_a_app)
        resume_delta_ibt_a_approchee = service.resume_statistiques(reader.data, col_delta_ibt_a_approchee)
        resume_col_t1_t2_euro_trim_ttc = service.resume_statistiques(reader.data, col_t1_t2_euro_trim_ttc)
        resume_col_t1_t2_euro_trim_ter = service.resume_statistiques(reader.data, col_t1_t2_euro_trim_ter)
         


        print("\n📊 Résumé des indicateurs statistiques : conso_q_cout_complet_m3_trim")
        print(resume.to_string(index=False))
        print("\n📊 HEAD")
        print(resume.head)


        print("\n📊 Résumé des indicateurs statistiques : col_delta_tbse_a_app")
        print(resumeZ6ZN.to_string(index=False))

        print("\n📊 Résumé des indicateurs statistiques : col_delta_ibt_a_approchee")
        print(resume_delta_ibt_a_approchee.to_string(index=False))

        print("\n📊 Résumé des indicateurs statistiques : t1_t2_euro_trim_ttc")
        print(resume_col_t1_t2_euro_trim_ttc.to_string(index=False))

        print("\n📊 Résumé des indicateurs statistiques : t1_t2_euro_trim_ter")
        print(resume_col_t1_t2_euro_trim_ter.to_string(index=False))


        ####################################################### tableau 2 ##########################################

        df_resume_short_t1_t2_euro_trim_ttc_Y = service.resume_short(reader.data, "t1_t2_euro_trim_ttc")
        df_resume_short_i1_ttc_U = service.resume_short(reader.data, "i1_ttc")
        df_resume_short_i2_ttc_V = service.resume_short(reader.data, "i2_ttc")
        df_resume_short_t1_t2_euro_trim_ter_CA = service.resume_short(reader.data, "t1_t2_euro_trim_ter")
        df_resume_short_i1_ter_BW = service.resume_short(reader.data, "i1_ter")
        df_resume_short_i2_ter_BX = service.resume_short(reader.data, "i2_ter")

        # Consolidation en un seul DataFrame
        tableau_2 = pd.DataFrame({
            "Delta Surplus Agrégé TBSE": df_resume_short_t1_t2_euro_trim_ttc_Y["Valeur"].values,
            "I1 (Delta surplus brut TBSE)": df_resume_short_i1_ttc_U["Valeur"].values,
            "I2 (Delta Coût TBSE)": df_resume_short_i2_ttc_V["Valeur"].values,
            "Delta Surplus Agrégé IBT-A": df_resume_short_t1_t2_euro_trim_ter_CA["Valeur"].values,
            "I1 (Delta surplus brut IBT)": df_resume_short_i1_ter_BW["Valeur"].values,
            "I2 (Delta Coût IBT)": df_resume_short_i2_ter_BX["Valeur"].values
        }, index=["Mean", "Median", "Variance", "Gini"])

        print("\n📊 TABLEAU 2 - Résumé consolidé")
        print("=" * 120)
        print(tableau_2)

        # Si vous voulez formater avec 2 décimales comme dans votre exemple
        print("\n📊 TABLEAU 2 - Version formatée (2 décimales)")
        print("=" * 120)
        print(tableau_2.round(2))


        # fin  Tableau 2 : 

        #Y6:Y463  t1_t2_euro_trim_ttc
        #U6:U463 i1_ttc
        #V6:V463 i2_ttc
        #CA6:CA463 t1_t2_euro_trim_ter
        #BW6:BW463 i1_ter
        #BX6:BX463 i2_ter
        print("\n📌 Creation des data frame filtrés :")
        ### Creation des data frame filtrés
        print("\n📌 <>0 ibt_moins :")
        #<>0 ibt_moins
        col_conso_ibt_moins = "ibt_moins"
        df_filtre_ibt_moins = reader.data[reader.data['ibt_moins'] != 0]
        print(df_filtre_ibt_moins)
        nombre_lignes = df_filtre_ibt_moins['menage'].count()
        print(nombre_lignes)
        resume_df_filtre_ibt_moins = service.resume_statistiques(df_filtre_ibt_moins, col_conso_ibt_moins)
        print(resume_df_filtre_ibt_moins.to_string(index=False))

        # ajouter a la classe de filtre
        print("\n📌 <>0 ibt_plus")
        #<>0 ibt_plus
        df_filtre_ibt_plus = reader.data[reader.data['ibt_plus'] != 0]
        print(df_filtre_ibt_plus)
        nombre_lignesibt_plus = df_filtre_ibt_plus['menage'].count()
        print(nombre_lignesibt_plus)


        print("\n📌 <>0 ds_a_moins")
        #<>0 ibt_plus
        df_filtre_ds_a_moins = reader.data[reader.data['ds_a_moins'] != 0]
        print(df_filtre_ds_a_moins)
        nombre_lignes_ds_a_moins= df_filtre_ds_a_moins['menage'].count()
        print(nombre_lignes_ds_a_moins)

        print("\n📌 <>0 ds_a_plus")
        #<>0 ibt_plus
        df_filtre_ds_a_plus = reader.data[reader.data['ds_a_plus'] != 0]
        print(df_filtre_ds_a_plus)
        nombre_lignes_ds_a_plus= df_filtre_ds_a_plus['menage'].count()
        print(nombre_lignes_ds_a_plus)


        # W à A 
        # CH6:CH463;<>0 ibt_moins
        # CI6:CI463;<>0 ibt_plus
        # CK6:CK463;<>0 ds_a_moins
        # CN6:CN463;<>0 ds_a_plus


        
        print("\n📌 Test des filtres")
        filter_obj = DataFrameFilter()
    
        
        filtered_df_EP = filter_obj.filter_data(reader.data, [("assaini", "==", 0)])
        print(filtered_df_EP)
        nombre_lignes_filtered_df_EP= filtered_df_EP['menage'].count()
        print(nombre_lignes_filtered_df_EP)

        print("\n📌 Delta IBT A+    CI6:CI253;<>0 et  (assaini, ==, 0)  ibt_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_ibt_plus = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("ibt_plus", "!=", 0) ])
        print(filtered_df_EP_ibt_plus)
        nombre_lignes_filtered_df_EP_ibt_plus= filtered_df_EP_ibt_plus['menage'].count()
        print(nombre_lignes_filtered_df_EP_ibt_plus)


        print("\n📌     Delta Surplus Agrégé IBT- A	 CK6:CK253;<>0  ds_a_moins")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_ds_a_moins = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("ds_a_moins", "!=", 0) ])
        print(filtered_df_EP_ds_a_moins)
        nombre_lignes_filtered_df_EP_ds_a_moins= filtered_df_EP_ds_a_moins['menage'].count()
        print(nombre_lignes_filtered_df_EP_ds_a_moins)

        print("\n📌     Delta Surplus Agrégé IBT- A	 CK6:CK253;<>0  ds_a_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_ds_a_plus = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("ds_a_plus", "!=", 0) ])
        print(filtered_df_EP_ds_a_plus)
        nombre_lignes_filtered_df_EP_ds_a_plus= filtered_df_EP_ds_a_plus['menage'].count()
        print(nombre_lignes_filtered_df_EP_ds_a_plus)

        ########################################################################### deuxiéme ensemble de colonne 

        print("\n📌     Delta Surplus Agrégé IBT A-	 CK6:CK253 <>0 et  (assaini, ==, 0)  ds_a_moins // OK")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_ds_a_moins = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("ds_a_moins", "!=", 0) ])
        print(filtered_df_EP_ds_a_moins)
        nombre_lignes_filtered_df_EP_ds_a_moins= filtered_df_EP_ds_a_moins['menage'].count()
        print(nombre_lignes_filtered_df_EP_ds_a_moins)
        ####

        print("\n📌    I1+ (Delta surplus brut IBT A-)	CL6:CL253;<>0 et  (assaini, ==, 0)  i1_a_moins)")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_i1_a_moins = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("i1_a_moins", "!=", 0) ])
        print(filtered_df_EP_i1_a_moins)
        nombre_lignes_filtered_df_i1_a_moins= filtered_df_EP_i1_a_moins['menage'].count()
        print(nombre_lignes_filtered_df_i1_a_moins)


        print("\n📌    I1+ (Delta surplus brut IBT A-)	CL6:CL253;<>0 et  (assaini, ==, 0)  i1_a_moins)")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_i2_a_moins = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("i2_a_moins", "!=", 0) ])
        print(filtered_df_EP_i2_a_moins)
        nombre_lignes_filtered_df_i2_a_moins= filtered_df_EP_i2_a_moins['menage'].count()
        print(nombre_lignes_filtered_df_i2_a_moins)

        ##
        print("\n📌     Delta Surplus Agrégé IBT A+	 CN6:CN253;<>0 et  (assaini, ==, 0) ds_a_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_ds_a_plus = filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("ds_a_plus", "!=", 0) ])
        print(filtered_df_EP_ds_a_plus)
        nombre_lignes_filtered_df_ds_a_plus= filtered_df_EP_ds_a_plus['menage'].count()
        print(nombre_lignes_filtered_df_ds_a_plus)


        print("\n📌     I1+ (Delta surplus brut IBT A+)	 CO6:CO253;<>0 et  (assaini, ==, 0)  i1_a_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_i1_a_plus= filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("i1_a_plus", "!=", 0) ])
        print(filtered_df_EP_i1_a_plus)
        nombre_lignes_filtered_df_i1_a_plus= filtered_df_EP_i1_a_plus['menage'].count()
        print(nombre_lignes_filtered_df_i1_a_plus)

        print("\n📌     I1+ (Delta surplus brut IBT A+)	 CO6:CO253;<>0 et  (assaini, ==, 0)  i1_a_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_i1_a_plus= filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("i1_a_plus", "!=", 0) ])
        print(filtered_df_EP_i1_a_plus)
        nombre_lignes_filtered_df_i1_a_plus= filtered_df_EP_i1_a_plus['menage'].count()
        print(nombre_lignes_filtered_df_i1_a_plus)


        print("\n📌      I2+ (Delta Coût IBT A+ CP6:CP253;<>0 et  (assaini, ==, 0) i2_a_plus")
        #Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus
        filtered_df_EP_i2_a_plus= filter_obj.filter_data(reader.data, [("assaini", "==", 0), ("i2_a_plus", "!=", 0) ])
        print(filtered_df_EP_i2_a_plus)
        nombre_lignes_filtered_df_i2_a_plus= filtered_df_EP_i2_a_plus['menage'].count()
        print(nombre_lignes_filtered_df_i2_a_plus)


        #Liste des fitres dans Groupe 1 
        # Delta IBT A-	CH6:CH253;"<>0 ET ("assaini", "==", 0) ->  ibt_moins // OK 
        # Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus // OK
        # Delta Surplus Agrégé IBT- A	 CK6:CK253;"<>0"  ds_a_moins // OK
        # Delta Surplus Agrégé IBT- A+ CN6:CN253;"<>0"  ds_a_plus

        ############################################################ deuxieme groupe d'indicateur 
        # Delta Surplus Agrégé IBT A-	 CK6:CK253 <>0 et  ("assaini", "==", 0)  ds_a_moins // OK
        # I1+ (Delta surplus brut IBT A-)	CL6:CL253;"<>0 et  ("assaini", "==", 0)  i1_a_moins // OK 
        # I2+ (Delta Coût IBT A-)	CM6:CM253;"<>0" et  ("assaini", "==", 0)  i2_a_moins // OK 
        # Delta Surplus Agrégé IBT A+	 CN6:CN253;"<>0" et  ("assaini", "==", 0) ds_a_plus // OK 
        # I1+ (Delta surplus brut IBT A+)	 CO6:CO253;"<>0" et  ("assaini", "==", 0)  i1_a_plus // OK 
        # I2+ (Delta Coût IBT A+ CP6:CP253;"<>0" et  ("assaini", "==", 0) i2_a_plus // OK 

        # col_conso = "conso_q_cout_complet_m3_trim"

        # # Exemple avec variance
        # result = service.valeur_min_et_covariance(reader.data, col_conso)

        print(reader.data.columns.tolist())

        print("conso_q_cout_complet_m3_trim")
        print(reader.data["conso_q_cout_complet_m3_trim"])

        print("t1_t2_euro_trim")
        print(reader.data["t1_t2_euro_trim"])
        


if __name__ == "__main__":
    main()
