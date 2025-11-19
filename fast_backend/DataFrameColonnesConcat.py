import pandas as pd
from stubsubtax import ExcelLister

class DataFrameColonnesConcat:
    def __init__(self, excel_path):
        # Liste directe des colonnes concaténées
        self.colonnes_source = [
            "menage_A11",
            "assaini_B11",
            "c_t1_C11",
            "c_t2_D11",
            "c_t3_E11",
            "c_t4_F11",
            "somme_conso_G11",
            "droit_acces_ep_t1_H11",
            "t1_ep_I11",
            "t2_ep_J11",
            "t3_ep_K11",
            "t4_ep_L11",
            "total_ep_M11",
            "droit_acces_2_ep_t1_N11",
            "t1_2_ep_O11",
            "t2_2_ep_P11",
            "t3_2_ep_Q11",
            "t4_2_ep_R11",
            "total_2_ep_S11",
            "droit_acces_3_ep_t1_T11",
            "t1_3_ep_U11",
            "t2_3_ep_V11",
            "t3_3_ep_W11",
            "t4_3_ep_X11",
            "total_3_ep_Y11",
            "abo_ttc_ep_Z11",
            "tranche1_ep_AA11",
            "tranche2_ep_AB11",
            "tranche3_ep_AC11",
            "tranche4_ep_AD11",
            "total_sub_tax_ttc_c_captive_ep_dae_AE11",
            "total_sub_tax_ttc_c_captive_ep_dai_AF11",
            "droit_acces_a_dae_t1_AI11",
            "t1_4_a_AJ11",
            "t2_4_a_AK11",
            "t3_4_a_AL11",
            "t4_4_a_AM11",
            "total_4_a_AN11",
            "droit_acces_a_dae_t2_AO11",
            "t1_5_a_AP11",
            "t2_5_a_AQ11",
            "t3_5_a_AR11",
            "t4_5_a_AS11",
            "total_5_a_AT11",
            "droit_acces_a_dae_t3_AU11",
            "t1_6_a_AV11",
            "t2_6_a_AW11",
            "t3_6_a_AX11",
            "t4_6_a_AY11",
            "total_6_a_AZ11",
            "abo_ttc_a_BA11",
            "tranche1_a_BB11",
            "tranche2_a_BC11",
            "tranche3_a_BD11",
            "tranche4_a_BE11",
            "total_sub_tax_ttc_c_captive_a_dae_BF11",
            "total_sub_tax_ttc_c_captive_a_dai_BG11",
            "droit_acces_epa_dae_t4_BJ11",
            "t1_7_epa_BK11",
            "t2_7_epa_BL11",
            "t3_7_epa_BM11",
            "t4_7_epa_BN11",
            "total_7_epa_BO11",
            "droit_acces_epa_dae_t5_BP11",
            "t1_8_epa_BQ11",
            "t2_8_epa_BR11",
            "t3_8_epa_BS11",
            "t4_8_epa_BT11",
            "total_8_epa_BU11",
            "droit_acces_epa_dae_t6_BV11",
            "t1_9_epa_BW11",
            "t2_9_epa_BX11",
            "t3_9_epa_BY11",
            "t4_9_epa_BZ11",
            "total_9_epa_CA11",
            "abo_ttc_epa_CB11",
            "tranche1_epa_CC11",
            "tranche2_epa_CD11",
            "tranche3_epa_CE11",
            "tranche4_epa_CF11",
            "total_sub_tax_ttc_c_captive_epa_dae_CG11",
            "total_sub_tax_ttc_c_captive_epa_dai_CH11"
        ]

        # Lecture du fichier Excel avec ExcelLister
        df_excel = pd.read_excel('subTaxInputCom.xls')

        # 2️⃣ Renommer les colonnes selon ton mapping
        # Exemple : on renomme les 6 premières colonnes
        df_excel.rename(columns={
            df_excel.columns[0]: 'menage_A11',
            df_excel.columns[1]: 'assaini_B11',
            df_excel.columns[2]: 'c_t1_C11',
            df_excel.columns[3]: 'c_t2_D11',
            df_excel.columns[4]: 'c_t3_E11',
            df_excel.columns[5]: 'c_t4_F11'
        }, inplace=True)

        # 3️⃣ Créer un nouveau DataFrame avec seulement ces colonnes (les premières)
        df_new = df_excel[['menage_A11', 'assaini_B11', 'c_t1_C11', 'c_t2_D11', 'c_t3_E11', 'c_t4_F11']].copy()

        # 4️⃣ Vérifier le résultat
        print(df_new.head())
        # Crée le DataFrame avec la ligne initialisée
        self.df = df_new

    def afficher(self):
        """Affiche uniquement les colonnes menage_A11 à c_t4_F11"""
        colonnes_a_afficher = [
            "menage_A11",
            "assaini_B11",
            "c_t1_C11",
            "c_t2_D11",
            "c_t3_E11",
            "c_t4_F11"
        ]
        # Vérifie que les colonnes existent dans le DataFrame
        colonnes_existantes = [col for col in colonnes_a_afficher if col in self.df.columns]
        print(self.df[colonnes_existantes].to_string(index=False))


# Exemple d’utilisation
if __name__ == "__main__":
    file_path = "subTaxInputCom.xls"
    data = DataFrameColonnesConcat(file_path)
    data.afficher()


    ### cacluml du total
    data.df['somme_conso_G11'] = data.df[['c_t1_C11', 'c_t2_D11', 'c_t3_E11', 'c_t4_F11']].sum(axis=1)

    colonnes_a_afficher = [
            "menage_A11",
            "assaini_B11",
            "c_t1_C11",
            "c_t2_D11",
            "c_t3_E11",
            "c_t4_F11", 
             "somme_conso_G11"
        ]
        # Vérifie que les colonnes existent dans le DataFrame
    colonnes_existantes = [col for col in colonnes_a_afficher if col in data.df.columns]
    print(data.df[colonnes_existantes].to_string(index=False))

    ## caulcul du total 


    
