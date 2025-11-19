import pandas as pd

from src.initial.schemas import *
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.calculator_service import SimulationFinished
from src.small_assessment.effeco_suruplusG2_RB import effeco_suruplusG2_CP
from src.small_assessment.rex_service import create_mock_simulation
from src.small_assessment.spaDfFservice import SpaDfFservice
from src.small_assessment.surplusG1CP import surplusG1CP

if __name__ == '__main__':
    simulation_payload: SimulationPayload = create_mock_simulation()

    finished = SimulationFinished(4, simulation_payload)
    print(affordability_general(finished.df))
    print("affichage du contenu de la DF")

    dfsource = pd.DataFrame(columns=[
        "menage",
        "assaini",
        "revenu_net_mois",
        "c_m3_trim",
        "c_m3_trim_2",
        "c_ibt",
        "c_ibt_pp",
        "c_tbse",
        "consom_nordin_trim",
        "consom_taylor_trim",
        "sur_conso_1",
        "sur_conso_2",
        "surconso"
    ])

    # Affichage pour vérifier

    dfsource["menage"] = finished.df['i_new']
    dfsource["assaini"] = finished.df['Assainissement Collectif (1 = oui)']
    dfsource["revenu_net_mois"] = finished.df['Revenu_Imputé_2']
    dfsource["c_m3_trim_2"] = finished.df['Partie_Base_C_et_Fact Q']
    dfsource["c_m3_trim"] = finished.df['Partie_Base_C_et_Fact Q'] * 90
    dfsource["c_ibt"] = finished.df['C_EP_BCP GB']
    dfsource["c_ibt_pp"] = finished.df['C_PP BM']
    dfsource["c_tbse"] = finished.df['C_et_F_TBSE P']
    dfsource["consom_nordin_trim"] = finished.df['C_PP BM']
    dfsource["consom_taylor_trim"] = finished.df['C_Taylor Q']
    dfsource["sur_conso_1"] = finished.df['C_EP_BCP GB'] - finished.df['C_PP BM']
    dfsource["sur_conso_2"] = finished.df['C_EP_BCP GB'] - finished.df['C_PP BM']
    dfsource["surconso"] = finished.df['C_EP_BCP GB'] - finished.df['C_PP BM']


    #### instanciation des element qui vont permettre de constuire surplusG1, SuplusG2 
    #### surplus agrégée
    ### suplus du consommateur


     # Instanciation directe de dfsource
    dfsource2 = pd.DataFrame({
        "menage": [101, 102, 103, 104],
        "assaini": [1, 0, 1, 0],
        "revenu_net_mois": [2200, 1800, 2500, 2000],
        "c_m3_trim_2": [12.5, 8.3, 15.0, 9.2],
        "c_m3_trim": [12.5*90, 8.3*90, 15.0*90, 9.2*90],
        "c_ibt": [14.0, 9.5, 16.0, 10.0],
        "c_ibt_pp": [12.0, 8.0, 13.0, 9.0],
        "c_tbse": [0.30, 0.25, 0.35, 0.28],
        "consom_nordin_trim": [12.0, 8.0, 13.0, 9.0],
        "consom_taylor_trim": [11.8, 8.2, 14.2, 9.1],
        "sur_conso_1": [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0],
        "sur_conso_2": [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0],
        "surconso":   [14.0-12.0, 9.5-8.0, 16.0-13.0, 10.0-9.0]
    })

    # Affichage pour vérification
    print(dfsource2)


    surplus = surplusG1CP(dfsource)
    print("Debut traitement surplus G1")
    _surplusG1CP = surplusG1CP(dfsource)

    _effeco_suruplusG2_CP = effeco_suruplusG2_CP(dfsource)
    # # Chemin pour exporter le DataFrame final (optionnel)
    # fichier_export = "resultats/surplus_G2_complet.xlsx"

    # Appel de la fonction pipeline
    df_final = _effeco_suruplusG2_CP.pipeline()

    print("Lise de colonne de surplus G2")
    print(list(df_final))

    # Avec affichage détaillé (comportement par défaut)
    df = surplus.run_full_pipeline()

    # print("Lise de colonne de surplus G1")
    # print(list(df))

    # OU sans affichage (pour exécution silencieuse)
    # df = surplus.run_full_pipeline("surplusG1_data.xls", verbose=False)

    # Vous pouvez ensuite utiliser df pour d'autres analyses
    print("\n" + "=" * 50)
    print("Pipeline terminé. DataFrame final disponible.")
    print("=" * 50)

    # Diviser le DataFrame en deux groupes indépendants
    dfG1 = df[df["assaini"] == 0].copy()  # Ménages SANS assainissement collectif
    dfG2 = df_final[df_final["assaini"] == 1].copy()  # Ménages AVEC assainissement collectif

    print("Colonnes du DF dfG1:")
    print(dfG1.columns.tolist())

    print("Colonnes du DF dfG2:")
    print(dfG2.columns.tolist())

    print("df_nouveau")
    # Créer un nouveau DF avec 2 colonnes spécifiques
    df_nouveau = finished.df[['i_new', 'poor']]
    df_nouveau = df_nouveau.rename(columns={
        # Colonnes de base
        'poor': 'menage_pauvre',
        'i_new': 'menage',
    })
    print(df_nouveau)

    df_nouveau["menage_pauvre"] = df_nouveau["menage_pauvre"].replace({True: 1, False: 0})
    print(df_nouveau)

    # Ajouter menage_pauvre à dfG1
    dfG1 = dfG1.merge(
        df_nouveau[['menage', 'menage_pauvre']],
        on='menage',
        how='left'
    )
    print("dfG1 avec menage pauvre ")
    print(dfG1.head())

    dfG2 = dfG2.merge(
        df_nouveau[['menage', 'menage_pauvre']],
        on='menage',
        how='left'
    )
    print("dfG2 avec menage pauvre ")
    print(dfG2.head())

    # Vérification
    print(f"dfG1 (sans assainissement) : {len(dfG1)} ménages")
    print(f"dfG2 (avec assainissement) : {len(dfG2)} ménages")
    print(f"Total : {len(dfG1) + len(dfG2)} ménages (sur {len(dfsource)} au départ)")

    #### construction du data frame de suprlus agrrégé
    service = SpaDfFservice(dfG1, dfG2)

    # Étape 1 : Empilement
    print("\n🔹 Étape 1 : Empilement de DF1 et DF2")
    df_empile = service.empiler_dataframes()
    print(df_empile)

    # Étape 2 : Construction du DF cible
    print("\n🔹 Étape 2 : Construction du DF3 cible selon le schéma")
    df3 = service.construire_df_cible()
    print(df3.head())

    print("delta_tbse_a_app")
    print(df3["delta_tbse_a_app"])

    print("\n✅ Programme terminé avec succès !")

    colonnes_toutes_none = df3.columns[df3.isnull().all()].tolist()
    print("Colonnes où toutes les valeurs sont None :", colonnes_toutes_none)

    ####

    # TODO: Fill this values using the computed dataframe

    FINAL_RESULT = {
        "Consumption": {
            "Average": None,
            "First Best": None,
            "Delta IBT PP": None,
            "Impact Sur Co": None,
            "Delta TBSE": None,
            "Delta Surplus M": None,
        },
        "Delta W": {
            "Average": None,
            "First Best": None,
            "Delta IBT PP": None,
            "Impact Sur Co": None,
            "Delta TBSE": None,
            "Delta Surplus M": None,
        },

    }

    ####
    assert False
    #####

    print(dfsource)

    table = TarifTab()

    # Si besoin, tu peux changer les valeurs ici :
    # table = TarifTab(redevance_accise_eur_m3=0.15, taux_tva_pct=5.5)

    # Ajout des lignes
    table.ajouter_ligne(TarifLine("k0", 0, 0.878, redevance_accise_eur_m3=0.12, taux_tva_pct=2.1))
    table.ajouter_ligne(TarifLine("k1", 15, 1.839, redevance_accise_eur_m3=0.12, taux_tva_pct=2.1))
    table.ajouter_ligne(TarifLine("k2", 30, 2.768, redevance_accise_eur_m3=0.12, taux_tva_pct=2.1))
    table.ajouter_ligne(TarifLine("k3", 60, 4.38, redevance_accise_eur_m3=0.12, taux_tva_pct=2.1))

    # Affichage
    table.afficher_table()

    tableA = TarifTab(redevance_accise_eur_m3=0.04, taux_tva_pct=10.0)

    # Ajout des lignes (nouvelles valeurs)
    tableA.ajouter_ligne(TarifLine("k0", 0, 1.3, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k1", 15, 2.12, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k2", 30, 2.21, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k3", 60, 2.5, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))

    # Affichage
    tableA.afficher_table()

    # --- Fusion des deux tables ---
    # Supposons que ta classe de fusion s'appelle TarifTabMerger
    merger = TarifTabMerger(table, tableA)
    table_fusionnee = merger.merge()

    # "c_m3_trim"		Partie Captive C et Fact'!R11  -- OK
    # "c_m3_trim_2"		Partie Base C et Fact'!Q11  -- OK
    # "c_ibt"		C_EP_BCP!HM23 GB23   -- OK
    # "c_ibt_pp"		C_PP!BM10   -- OK
    # "c_tbse"		C_et F_TBSE'!P12   -- OK
    # "consom_nordin_trim"		C_PP!BM10  -- OK
    # "consom_taylor_trim"		C_Taylor!Q20  -- OK
    # "sur_conso_1"		C_EP_BCP!HM23-C_PP!BM10 -- OK
    # "sur_conso_2"		C_EP_BCP!HM23-C_PP!BM10
    # "surconso		C_EP_BCP!HM23-C_PP!BM10
