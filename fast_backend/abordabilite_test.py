import pandas as pd

from src.initial.graphics_service import generate_ibt_pens_parade_consumptions_plot, generate_tbse_consumption_deviation_losses_cost_recovery_plot, generate_tbse_pens_parade_consumptions_plot
from src.initial.schemas import *
from src.small_assessment.affordability_service import affordability_general
from src.small_assessment.calculator_service import SimulationCalculator, SimulationFinished
from src.small_assessment.rex_service import create_mock_simulation
from src.small_assessment.subtax import subTaxTable, subTaxRow
from stubsubtax import ExcelLister
from src.small_assessment.Sub_Tax_Input_Consom import Sub_Tax_Input_Consom
from src.small_assessment.AccesLine  import AccesLine
from src.small_assessment.ServicePayload import ServicePayload
from src.small_assessment.sub_Tax_Input_Consom_service import sub_Tax_Input_Consom_service
from src.small_assessment.subTInConsoDF import SubTInConsoDF


if __name__ == '__main__':
    simulation_payload: SimulationPayload = create_mock_simulation()
   
    finished = SimulationFinished(4, simulation_payload)
    print(affordability_general(finished.df))
    print("affichage du contenu de la DF")
    #print(finished.df)
    #print(list(finished.df))


    #generate_ibt_pens_parade_consumptions_plot(finished.df)
    #generate_tbse_pens_parade_consumptions_plot(finished.df)
    #generate_tbse_consumption_deviation_losses_cost_recovery_plot(finished, 'C_et_F_TBSE P', 'TBSE')
    #generate_tbse_consumption_deviation_losses_cost_recovery_plot(finished, 'C_EP_BCP HM', 'IBT')
    


    # print(finished.df['Assainissement Collectif (1 = oui)'])
    # print(finished.df['i_new'])
    # print(finished.df['Facture_IBT_C_BCP F'])
    # print(finished.df['Facture_IBT_C_BCP H'])
    # print(finished.df['Facture_IBT_C_BCP J'])
    # print(finished.df['Facture_IBT_C_BCP K'])


    service = sub_Tax_Input_Consom_service(finished.df)
    sub_df = service.get_sub_dataframe()

    print("✅ Sous-DataFrame extraite :")
    print(sub_df)
    
 


    #### test 
    print("###################################service payload#################################################")
    service_payload = ServicePayload.from_simulation_payload(simulation_payload)
    
    # Afficher les données
    print(service_payload)
    print("\nDictionnaire:", service_payload.to_dict())
    
    # Accéder aux attributs normalisés
    print(f"\nAbonnement EP: {service_payload.description_tarif_ibt4_c2}€")
    print(f"Coûts fixes EP: {service_payload.couts_service_ep_epa_c11}€")

    print("###################################service payload#################################################")

    print("Description_Tarif_IBT4_C3")
    tbse_ep_variable_prix= simulation_payload.tbse_ep_variable_prix
    variable_costs= simulation_payload.primitives.drinking_water.variable_costs
    description_Tarif_IBT4_D3 = simulation_payload.primitives.taxation.drinking_water.fees
    couts_du_service_EP_EPA_D12 = simulation_payload.primitives.taxation.drinking_water.fees
    tvaep = simulation_payload.primitives.taxation.drinking_water.vat

    #-> tbse_ep_variable_prix: 1.02
    print(f"tbse_ep_variable_prix: {tbse_ep_variable_prix}")
    print(f"variable_costs: {variable_costs}")
    print(f"description_Tarif_IBT4_D3: {description_Tarif_IBT4_D3}")
    print(f"couts_du_service_EP_EPA_D12: {couts_du_service_EP_EPA_D12}")
    print(f"tvaep: {tvaep}")


    _mnt_TVA_unite_service_pu = tbse_ep_variable_prix*tvaep/100

    print(f"mnt_TVA_unite_service_pu: {_mnt_TVA_unite_service_pu}")
    

    tiers = simulation_payload.tariff.drinking_water.usage_tiers
    for tier in tiers:
        print(f"Seuil: {tier.threshold}, Prix: {tier.price}")

    

    tiers = [
        {"seuil": 0.0, "prix": 0.878},
        {"seuil": 15.0, "prix": 1.839},
        {"seuil": 30.0, "prix": 2.768},
        {"seuil": 60.0, "prix": 4.38}
    ]

    table = subTaxTable(tiers, volume=15, couts_du_Service_EP=variable_costs,  taux_tva=2.1, redevance=0.05, mnt_TVA_unite_service_pu= _mnt_TVA_unite_service_pu)
    table.show()

    #### 
    print("---------------")
    print(table.calculer_prix_h_tva())
    print(f"la bonne donnée : {table.calculer_montant_tva_unite()}")

    ##### PREPARATION DE PARAMETRES ##############
    # J=table.
    # J$3
    # J$4
    # J$5
    # J$6
    print("liste de sub_ht_op : all_sub_ht_op" )
    all_sub_ht_op= table.get_all_sub_ht_op
    print(f'liste de sub_ht_op : {all_sub_ht_op}' )


  
    print(table.calculer_sub_tva(_mnt_TVA_unite_service_pu))

    ####################################################################################
    file_path = "subTaxInputCom.xls"



    try:
        # Création de l'objet ExcelLister
        excel_lister = ExcelLister(file_path)

        # Récupération du DataFrame lu
        df_excel = excel_lister.data

        # Création d'un DataFrame final avec toutes les colonnes nécessaires
        colonnes_source = [
            "menage_A11", "assaini_B11", "c_t1_C11", "c_t2_D11", "c_t3_E11", "c_t4_F11",
            "somme_conso_G11"
            # Ajouter ici les autres colonnes calculées ou initialisées à 0
        ]

        df_final = pd.DataFrame(columns=colonnes_source)

        # Renommer et affecter les colonnes principales depuis df_excel
        df_final["menage_A11"] = df_excel["Menage"]
        df_final["assaini_B11"] = df_excel["Assaini"]
        df_final["c_t1_C11"] = df_excel["C_T1"]
        df_final["c_t2_D11"] = df_excel["C_T2"]
        df_final["c_t3_E11"] = df_excel["C_T3"]
        df_final["c_t4_F11"] = df_excel["C_T4"]


        data = SubTInConsoDF(df_final)
        data["somme_conso_G11"] = data[["c_t1_C11", "c_t2_D11", "c_t3_E11", "c_t4_F11"]].sum(axis=1)
        data.afficher()


        # Calcul automatique de somme_conso_G11
        

        # Initialisation des autres colonnes à 0
        for col in colonnes_source:
            if col not in df_final.columns:
                df_final[col] = 0

        # Affichage du DataFrame final
        print("\n📊 DataFrame final :")
        print(df_final.head())

    except Exception as e:
        print(f"\n🚨 Erreur : {e}")

    #### block a renmplcer et a strandardiser 
    acces_line = AccesLine(
    sub_ht_op=-28.3349,
    sub_redev=0.0000,
    sub_hors_tva=-28.3349,
    sub_tva=-0.5950,
    sub_ttc=-28.9299
    )

    # Affichage lisible
    print(acces_line)

    # Conversion en dictionnaire
    print(acces_line.to_dict())


    # df_final["droit_acces_ep_t1_H11"] = acces_line.sub_ht_op
    # df_final["t1_ep_I11"]
    # df_final["t2_ep_J11"]
    # df_final["t3_ep_K11"]
    # df_final["t4_ep_L11"]
    # df_final["total_ep_M11"]