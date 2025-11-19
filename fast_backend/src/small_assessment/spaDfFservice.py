import pandas as pd

class SpaDfFservice:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame):
        """
        Initialise le service avec deux DataFrames.
        """
        self.df1 = df1
        self.df2 = df2
        self.df_empile = None  # contiendra le DF1 + DF2 empilés
        self.df3 = None        # contiendra le DF final construit

        # Schéma cible complet
        self.colonnes_cibles = [
    "menage", "assaini", "menage_pauvre",
    "conso_q_cout_complet_m3_trim", "qb_m3_trim",
    "i1", "i2", "t1", "t2", "t1_t2_euro_trim",
    "qb_sans_tva", "i1_sans_tva", "i2_sans_tva", "t1_sans_tva",
    "t2_sans_tva", "t1_t2_euro_trim_sans_tva", "qb_ttc", "i1_ttc",
    "i2_ttc", "t1_ttc", "t2_ttc", "t1_t2_euro_trim_ttc",
    "delta_tbse_a_app", "conso_ht_m3_trim_pp", "surconso",
    "conso_ht_avec_surconso_m3_trim", "i1.1", "i2.1", "t1.1",
    "t2.1", "t1_t2_euro_trim.1", "i1_bis", "i2_bis", "t1_bis",
    "t2_bis", "t1_t2_euro_trim_bis", "conso_sans_tva",
    "surconso_sans_tva", "conso_mauvaise_perception",
    "i1_sans_tva.1", "i2_sans_tva.1", "t1_sans_tva.1",
    "t2_sans_tva.1", "t1_t2_euro_trim_sans_tva.1", "i1.2",
    "i2.2", "t1.2", "t2.2", "t1_t2_euro_trim.2",
    "conso_finale_redevance_tva", "surconso.1",
    "conso_mauvaise_perception.1", "delta_ibt_a_approchee",
    "cout_env_non_recuperes", "recupere_flag", "non_recupere_flag",
    "i1_bis.1", "i2_bis.1", "t1_bis.1", "t2_bis.1",
    "t1_t2_euro_trim_bis.1", "i1_ter", "i2_ter", "t1_ter",
    "t2_ter", "t1_t2_euro_trim_ter", "d1_a_moins", "d1_b_plus",
    "d1_c_eq", "conso_trop", "conso_pas", "ibt_moins", "ibt_plus",
    "ds_a_moins", "i1_a_moins", "i2_a_moins", "ds_a_plus",
    "i1_a_plus", "i2_a_plus"
]

    # === Étape 1 : empiler DF1 et DF2 ===
    def empiler_dataframes(self) -> pd.DataFrame:
        """
        Empile df1 et df2 verticalement et conserve le résultat dans self.df_empile.
        """
        self.df_empile = pd.concat([self.df1, self.df2], ignore_index=True)
        return self.df_empile

    # === Étape 2 : construire DF3 à partir du DF empilé ===
    def construire_df_cible(self) -> pd.DataFrame:
        """
        Construit le DF cible (DF3) à partir du DF empilé (DF1 + DF2),
        en respectant le schéma cible défini dans self.colonnes_cibles.
        """
        if self.df_empile is None:
            raise ValueError("⚠️ Vous devez d'abord appeler empiler_dataframes() avant de construire le DF cible.")

        # Créer une copie du DF empilé
        df_base = self.df_empile.copy()
        df_base.columns = df_base.columns.str.strip()

        df_base = df_base.rename(columns={
        # Colonnes de base
        'i1_1': 'i1',
        'i2_1': 'i2',
        't1_1': 't1',
        't2_1': 't2',
        't1_t2_eur_trim': 't1_t2_euro_trim',
        
        # Sans TVA
        'qb_redev_sans_tva': 'qb_sans_tva',
        'i1_3': 'i1_sans_tva',
        'i2_3': 'i2_sans_tva',
        't1_3': 't1_sans_tva',
        't2_3': 't2_sans_tva',
        't1_t2_eur_trim_1': 't1_t2_euro_trim_sans_tva',
        
        # TTC
        'i1_5': 'i1_ttc',
        'i2_5': 'i2_ttc',
        't1_5': 't1_ttc',
        't2_5': 't2_ttc',
        't1_t2_eur_trim_2': 't1_t2_euro_trim_ttc',
        
        # Consommation et surconsommation
        'conso_hrt_m3_trim_val': 'conso_ht_m3_trim_pp',
        'sur_conso_1': 'surconso',
        'conso_mauvaise_percep_m3_trim': 'conso_ht_avec_surconso_m3_trim',
        
        # Variantes avec points
        'i1_7': 'i1.1',
        'i2_7': 'i2.1',
        't1_7': 't1.1',
        't2_7': 't2.1',
        't1_t2_eur_trim_3': 't1_t2_euro_trim.1',
        
        # Variantes bis
        'i1_9': 'i1_bis',
        'i2_9': 'i2_bis',
        't1_9': 't1_bis',
        't2_9': 't2_bis',
        't1_t2_eur_trim_4': 't1_t2_euro_trim_bis',
        
        # Consommation sans TVA
        'conso_sans_tva_val': 'conso_sans_tva',
        'sur_conso_2': 'surconso_sans_tva',
        'conso_mauvaise_percep': 'conso_mauvaise_perception',
        
        # Variantes sans TVA avec points
        'i1_11': 'i1_sans_tva.1',
        'i2_11': 'i2_sans_tva.1',
        't1_11': 't1_sans_tva.1',
        't2_11': 't2_sans_tva.1',
        't1_t2_eur_trim_5': 't1_t2_euro_trim_sans_tva.1',
        
        # Variantes avec .2
        'i1_13': 'i1.2',
        'i2_13': 'i2.2',
        't1_13': 't1.2',
        't2_13': 't2.2',
        't1_t2_eur_trim_6': 't1_t2_euro_trim.2',
        
        # Consommation finale TVA
        'conso_tva_val': 'conso_finale_redevance_tva',
        'conso_mauvaise': 'conso_mauvaise_perception.1',
        
        # Variantes bis.1
        'i1_15': 'i1_bis.1',
        'i2_15': 'i2_bis.1',
        't1_15': 't1_bis.1',
        't2_15': 't2_bis.1',
        't1_t2_euro_trim': 't1_t2_euro_trim_bis.1',
        
        # Variantes ter
        'i1_17': 'i1_ter',
        'i2_17': 'i2_ter',
        't1_17': 't1_ter',
        't2_17': 't2_ter',
        't1_t2_euro_trim_1': 't1_t2_euro_trim_ter',
        'cout_env_non_recup': 'cout_env_non_recuperes',
            'surconso' : 'surconso.1'
        
    })


        # Ajouter les colonnes manquantes si besoin
        for col in self.colonnes_cibles:
            print("------------------")
            print(f'{col} : {col not in df_base.columns}')
            #print(col not in df_base.columns)

            if col not in df_base.columns:
                df_base[col] = None

        # Filtrer et réordonner selon le schéma cible
        self.df3 = df_base[self.colonnes_cibles].copy()

        self.df3["delta_tbse_a_app"]=self.df3["conso_q_cout_complet_m3_trim"]- self.df3["qb_ttc"]
        self.df3["delta_ibt_a_approchee"]=self.df3["conso_finale_redevance_tva"]- self.df3["qb_ttc"]
        ##### TRaitement de colonne manquante #####
        print("self.df3[surconso]")
        print(self.df3["surconso"])
                # d1_a_moins : SI(@surconso<@conso_q_cout_complet_m3_trim;1;0) -- ✅ OK 
        self.df3["d1_a_moins"] = (self.df3["surconso"] < self.df3["conso_q_cout_complet_m3_trim"]).astype(int)

        # # d1_b_plus : SI(@surconso>@conso_q_cout_complet_m3_trim;1;0) -- ✅ OK 
        self.df3["d1_b_plus"] = (self.df3["surconso"] > self.df3["conso_q_cout_complet_m3_trim"]).astype(int)

        # # d1_c_eq : SI(@surconso=@conso_q_cout_complet_m3_trim;1;0) -- ✅ OK 
        self.df3["d1_c_eq"] = (self.df3["surconso"] == self.df3["conso_q_cout_complet_m3_trim"]).astype(int)

        # # conso_trop : @d1_b_plus*@surconso -- ✅ OK
        self.df3["conso_trop"] = self.df3["d1_b_plus"] * self.df3["surconso"]

        # # conso_pas : @d1_a_moins*@surconso -- ✅ OK
        self.df3["conso_pas"] = self.df3["d1_a_moins"] * self.df3["surconso"]

        # # ibt_moins : (@conso_pas-@conso_q_cout_complet_m3_trim)*@d1_a_moins -- ✅ OK
        self.df3["ibt_moins"] = (self.df3["conso_pas"] - self.df3["conso_q_cout_complet_m3_trim"]) * self.df3["d1_a_moins"]

        # # ibt_plus : (@conso_trop-@conso_q_cout_complet_m3_trim)*@d1_b_plus -- ✅ OK
        self.df3["ibt_plus"] = (self.df3["conso_trop"] - self.df3["conso_q_cout_complet_m3_trim"]) * self.df3["d1_b_plus"]

        # # ds_a_moins : @d1_a_moins*@t1_t2_euro_trim_ter -- ✅ OK 
        self.df3["ds_a_moins"] = self.df3["d1_a_moins"] * self.df3["t1_t2_euro_trim_ter"]

        # # i1_a_moins : @d1_a_moins*@i1_ter -- ✅ OK 
        self.df3["i1_a_moins"] = self.df3["d1_a_moins"] * self.df3["i1_ter"]

        # # i2_a_moins : @d1_a_moins*@i2_ter -- ✅ OK 
        self.df3["i2_a_moins"] = self.df3["d1_a_moins"] * self.df3["i2_ter"]

        # # ds_a_plus : @d1_b_plus*@t1_t2_euro_trim_ter -- ✅ CORRIGÉ
        self.df3["ds_a_plus"] = self.df3["d1_b_plus"] * self.df3["t1_t2_euro_trim_ter"]

        # # i1_a_plus : @d1_b_plus*@i1_ter -- ✅ OK
        self.df3["i1_a_plus"] = self.df3["d1_b_plus"] * self.df3["i1_ter"]

        # # i2_a_plus : @d1_b_plus*@i2_ter -- ✅ OK
        self.df3["i2_a_plus"] = self.df3["d1_b_plus"] * self.df3["i2_ter"]
        

        print(f'{"qb_sans_tva "} : {"qb_sans_tva " not in df_base.columns}')
        print(f'{"qb_redev_sans_tva"} : {"qb_redev_sans_tva" not in df_base.columns}')
        
        return self.df3
    
    def construire_df_cibleV2(self) -> pd.DataFrame:
        """
        Construit le DF cible (DF3) à partir du DF empilé (DF1 + DF2),
        en respectant le schéma cible défini dans self.colonnes_cibles.
        """
        if self.df_empile is None:
            raise ValueError("⚠️ Vous devez d'abord appeler empiler_dataframes() avant de construire le DF cible.")
        
        print("Colonnes du DF empilé:")
        print(self.df_empile.columns.tolist())
        
        # Créer une copie du DF empilé
        df_base = self.df_empile.copy()
        df_base.columns = df_base.columns.str.strip()
        
        # Mapping entre colonnes sources et colonnes cibles
        mapping_colonnes = {
            # Colonnes existantes dans df_empile -> noms dans colonnes_cibles
            "menage": "menage",
            "assaini": "assaini",
            "c_m3_trim": "conso_q_cout_complet_m3_trim",  # À ajuster selon vos données
            "surconso": "surconso",
            "qb_m3_trim": "qb_m3_trim",
            
            # Ajoutez ici toutes les correspondances
        }

        print("qb_m3_trim")
        print("qb_m3_trim" not in df_base.columns)
        
        
        # Renommer les colonnes selon le mapping
        df_base = df_base.rename(columns=mapping_colonnes)
        
        # Ajouter les colonnes manquantes avec None
        for col in self.colonnes_cibles:
            if col not in df_base.columns:
                df_base[col] = None
        
        # Filtrer et réordonner selon le schéma cible
        self.df3 = df_base[self.colonnes_cibles].copy()
        
        return self.df3


# -----------------------------
# Programme principal
# -----------------------------
def main():
    print("=== DEMARRAGE DU PROGRAMME ===")

    # Création de deux DataFrames simulées
    df1 = pd.DataFrame({
        "menage": [1, 2],
        "assaini": [True, False],
        "i1": [10, 20],
        "t1": [5, 6],
        "conso_q_cout_complet_m3_trim": [100, 120]
    })

    df2 = pd.DataFrame({
        "menage": [3, 4],
        "assaini": [True, True],
        "i1": [15, 25],
        "t1": [7, 8],
        "conso_q_cout_complet_m3_trim": [130, 150]
    })

    # Création du service
    service = SpaDfFservice(df1, df2)

    # Étape 1 : Empilement
    print("\n🔹 Étape 1 : Empilement de DF1 et DF2")
    df_empile = service.empiler_dataframes()
    print(df_empile)

    # Étape 2 : Construction du DF cible
    print("\n🔹 Étape 2 : Construction du DF3 cible selon le schéma")
    df3 = service.construire_df_cible()
    print(df3.head())

    print("\n✅ Programme terminé avec succès !")


# -----------------------------
# Point d'entrée du script
# -----------------------------
if __name__ == "__main__":
    main()