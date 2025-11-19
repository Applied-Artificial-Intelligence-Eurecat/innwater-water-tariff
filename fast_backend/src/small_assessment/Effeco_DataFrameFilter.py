import pandas as pd

class DataFrameFilter:
    def __init__(self):
        pass

    def filter_data(self, df, filters):
        """
        Filtre les données d'un DataFrame selon plusieurs conditions.
        
        :param df: pandas DataFrame à filtrer
        :param filters: liste de tuples (colonne, opérateur, valeur)
        :return: DataFrame filtré
        """
        if not filters:
            return df
        
        mask = pd.Series([True] * len(df))
        for column, op, value in filters:
            if column not in df.columns:
                raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
            
            if op == "==":
                mask &= (df[column] == value)
            elif op == "!=":
                mask &= (df[column] != value)
            elif op == ">":
                mask &= (df[column] > value)
            elif op == "<":
                mask &= (df[column] < value)
            elif op == ">=":
                mask &= (df[column] >= value)
            elif op == "<=":
                mask &= (df[column] <= value)
            else:
                raise ValueError(f"Opérateur '{op}' non supporté.")
        
        return df[mask]
    

    def filtered_ibt_plus(self, reader):
        """
        Filtre les lignes de reader.data avec ibt_plus != 0.
        Affiche le DataFrame filtré et le nombre de lignes.
        
        :param reader: objet possédant un attribut .data (pandas DataFrame)
        :return: (DataFrame filtré, nombre de lignes)
        """
        print("\n📌 <>0 ibt_plus")
        df_filtre_ibt_plus = reader.data[reader.data['ibt_plus'] != 0]
        print(df_filtre_ibt_plus)
        nombre_lignesibt_plus = df_filtre_ibt_plus['menage'].count()
        print(nombre_lignesibt_plus)
        return df_filtre_ibt_plus, nombre_lignesibt_plus
    
     # W à A 
        # CH6:CH463;<>0 ibt_moins
        # CI6:CI463;<>0 ibt_plus
        # CK6:CK463;<>0 ds_a_moins
        # CN6:CN463;<>0 ds_a_plus


    def filtered_df_ibt_moins(self, df, service):
        """
        Filtre les lignes avec ibt_moins != 0, affiche le DataFrame, le nombre de lignes,
        et un résumé statistique via service.resume_statistiques.
        """
        print("\n📌 <>0 ibt_moins :")
        col_conso_ibt_moins = "ibt_moins"
        df_filtre_ibt_moins = df[df['ibt_moins'] != 0]
        nombre_lignes = df_filtre_ibt_moins['menage'].count()
        return df_filtre_ibt_moins, nombre_lignes
    

    def filtered_df_ibt_plus(self, df):
        """
        Filtre les lignes avec ibt_plus != 0, affiche le DataFrame et le nombre de lignes.
        """
        print("\n📌 <>0 ibt_plus")
        df_filtre_ibt_plus = df[df['ibt_plus'] != 0]
        nombre_lignesibt_plus = df_filtre_ibt_plus['menage'].count()
        print(nombre_lignesibt_plus)
        return df_filtre_ibt_plus, nombre_lignesibt_plus
    
    #Liste des fitres dans Groupe 1 
        # Delta IBT A-	CH6:CH253;"<>0 ET ("assaini", "==", 0) ->  ibt_moins // OK 
        # Delta IBT A+    CI6:CI253;"<>0 et  ("assaini", "==", 0)  ibt_plus // OK
        # Delta Surplus Agrégé IBT- A	 CK6:CK253;"<>0"  ds_a_moins // OK
        # Delta Surplus Agrégé IBT- A+ CN6:CN253;"<>0"  ds_a_plus
    
    def filtered_df_EP(self, df):
        """
        Filtre pour assaini == 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     EP - filtre : assaini == 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


    def filtered_df_EP_ibt_plus(self, df):
        """
        Filtre pour assaini == 0 et ibt_plus != 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     IBT+ - filtre : assaini == 0 et ibt_plus != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("ibt_plus", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes
 
    def filtered_df_EP_ds_a_moins_bis(self, df):
        """
        Filtre pour assaini == 0 et ds_a_moins != 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     DS A- - filtre : assaini == 0 et ds_a_moins != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("ds_a_moins", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes



    def filtered_df_EP_ds_a_plus(self, df):
        """
        Filtre pour assaini == 0 et ds_a_plus != 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     DS A+ - filtre : assaini == 0 et ds_a_plus != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("ds_a_plus", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes

    ######################################## bloc 2 
    

    def filtered_df_EP_ds_a_moins(self, df):
        """
        Filtre pour assaini == 0 et ds_a_moins != 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     DS A- - filtre : assaini == 0 et ds_a_moins != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("ds_a_moins", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes
    

    def filtered_df_EP_i1_a_moins(self, df):
        """
        Filtre pour assaini == 0 et i1_a_moins != 0
        Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
        """
        print("\n📌     I1- (Delta Coût IBT A-) - filtre : assaini == 0 et i1_a_moins != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("i1_a_moins", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes



    def filtered_df_EP_i2_a_moins(self, df):
            """
            Filtre pour assaini == 0 et i2_a_moins != 0
            Retourne le DataFrame filtré et le nombre de lignes de 'menage'.
            """
            print("\n📌     I2- (Delta Coût IBT A-) - filtre : assaini == 0 et i2_a_moins != 0")
            filtered_df = self.filter_data(df, [("assaini", "==", 0), ("i2_a_moins", "!=", 0)])
            print(filtered_df)
            nombre_lignes = filtered_df['menage'].count()
            print(nombre_lignes)
            return filtered_df, nombre_lignes


    def filtered_df_EP_i1_a_plus(self, df):
        """Filtre pour assaini == 0 et i1_a_plus != 0"""
        print("\n📌     I1+ (Delta surplus brut IBT A+) - filtre : assaini == 0 et i1_a_plus != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("i1_a_plus", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes

    def filtered_df_EP_i2_a_plus(self, df):
        """Filtre pour assaini == 0 et i2_a_plus != 0"""
        print("\n📌     I2+ (Delta Coût IBT A+) - filtre : assaini == 0 et i2_a_plus != 0")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("i2_a_plus", "!=", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


        # filtre pour Coûts environnementaux qui ne sont pas récupéré


        # C

        # D


        # F  menage_pauvre = 1
    def filtered_df_menage_pauvre_cenv(self, df):
        """Filtre pour menage_pauvre """
        print("\n📌     menage_pauvre")
        filtered_df = self.filter_data(df, [("menage_pauvre", "==", 1)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


        # G non menage_pauvre = 0

    def filtered_df_menage_npauvre_cenv(self, df):
        """Filtre pour menage_pauvre """
        print("\n📌     non menage_pauvre")
        filtered_df = self.filter_data(df, [("menage_pauvre", "==", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


        # H G1 poor

    def filtered_df_G1_poor(self, df):
        """Filtre pour G1 poor"""
        print("\n📌     G1 poor")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("menage_pauvre", "==", 1)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


        # I G2 poor

    def filtered_df_G2_poor(self, df):
        """Filtre pour G1 poor"""
        print("\n📌     G1 poor")
        filtered_df = self.filter_data(df, [("assaini", "==", 1), ("menage_pauvre", "==", 1)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes


        # J

    def filtered_df_G1_npoor(self, df):
        """Filtre pour G1 poor"""
        print("\n📌     G1 poor")
        filtered_df = self.filter_data(df, [("assaini", "==", 0), ("menage_pauvre", "==", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes



        # K

    def filtered_df_G2_npoor(self, df):
        """Filtre pour G1 poor"""
        print("\n📌     G1 poor")
        filtered_df = self.filter_data(df, [("assaini", "==", 1), ("menage_pauvre", "==", 0)])
        print(filtered_df)
        nombre_lignes = filtered_df['menage'].count()
        print(nombre_lignes)
        return filtered_df, nombre_lignes

# ===========================
# Exemple d'utilisation (main)
# ===========================
if __name__ == "__main__":
    # Jeu de données exemple
    data = {
        "menage": [1, 2, 3, 4, 5, 6],
        "assaini": [0, 1, 0, 0, 1, 0],
        "ds_a_plus": [0, 2, 5, 0, 3, 1],
        "i1_a_plus": [0, 2, 1, 3, 0, 0],
        "i2_a_plus": [0, 4, 0, 2, 5, 1],
    }

    df = pd.DataFrame(data)
    filter_obj = DataFrameFilter()

    # Tests des filtres
    filter_obj.filtered_df_EP_ds_a_plus(df)
    filter_obj.filtered_df_EP_i1_a_plus(df)
    filter_obj.filtered_df_EP_i2_a_plus(df)
