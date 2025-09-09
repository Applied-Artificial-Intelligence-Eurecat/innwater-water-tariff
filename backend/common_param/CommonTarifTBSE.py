import pandas as pd

class CommonTarifTBSEModel:
    # Définition des colonnes comme attribut de classe (avec id_projet)
    COLUMNS = [
        "id_projet",
        "nature_tarif", 
        "type_tarif", 
        "prix_ht_op", 
        "redevances", 
        "prix_ht_tva", 
        "montant_tva_unite_service", 
        "prix_ttc"
    ]
    
    @classmethod
    def create_default_dataframe(cls, id_projet_default=1):
        """
        Crée un DataFrame avec les données par défaut des tarifs TBSE
        
        Args:
            id_projet_default (int): Valeur par défaut pour id_projet (défaut: 1)
            
        Returns:
            pandas.DataFrame: DataFrame avec données par défaut
        """
        default_data = [
            [id_projet_default, "TBSE EP", "Abonnement", 47.0249, 0.0000, 47.0249, 0.9875, 48.0124],
            [id_projet_default, "TBSE EP", "Prix unitaire (au mètre 3)", 0.9000, 0.1200, 1.0200, 0.0214, 1.0414],
            [id_projet_default, "TBSE A", "Abonnement", 59.2885, 0.0000, 59.2885, 5.9289, 65.2174],
            [id_projet_default, "TBSE A", "Prix unitaire (au mètre 3)", 0.4000, 0.0400, 0.4400, 0.0440, 0.4840],
            [id_projet_default, "TBSE EPA", "Abonnement", 106.3134, 0.0000, 106.3134, 6.9164, 113.2298],
            [id_projet_default, "TBSE EPA", "Prix unitaire (au mètre 3)", 1.3000, 0.1600, 1.4600, 0.0654, 1.5254]
        ]
        
        return pd.DataFrame(default_data, columns=cls.COLUMNS)
    
    @classmethod
    def create_empty_dataframe(cls):
        """
        Crée un DataFrame vide avec la structure des colonnes
        
        Returns:
            pandas.DataFrame: DataFrame vide avec structure
        """
        return pd.DataFrame(columns=cls.COLUMNS)
    
    @classmethod
    def add_row_to_dataframe(cls, df, nature_tarif, type_tarif, prix_ht_op, redevances, 
                           prix_ht_tva, montant_tva_unite_service, prix_ttc, id_projet=1):
        """
        Ajoute une ligne à un DataFrame existant
        
        Args:
            df (pandas.DataFrame): DataFrame cible
            nature_tarif (str): Nature du tarif
            type_tarif (str): Type de tarif
            prix_ht_op (float): Prix HT opérateur
            redevances (float): Redevances
            prix_ht_tva (float): Prix HT TVA
            montant_tva_unite_service (float): Montant TVA unité de service
            prix_ttc (float): Prix TTC
            id_projet (int): ID du projet (défaut: 1)
            
        Returns:
            pandas.DataFrame: DataFrame mis à jour
        """
        new_row = pd.DataFrame({
            "id_projet": [id_projet],
            "nature_tarif": [nature_tarif],
            "type_tarif": [type_tarif],
            "prix_ht_op": [prix_ht_op],
            "redevances": [redevances],
            "prix_ht_tva": [prix_ht_tva],
            "montant_tva_unite_service": [montant_tva_unite_service],
            "prix_ttc": [prix_ttc]
        })
        
        return pd.concat([df, new_row], ignore_index=True)

# Exemple d'utilisation dans le main
if __name__ == "__main__":
    print("=== Utilisation de CommonTarifTBSEModel avec id_projet ===")
    
    # Créer un DataFrame vide avec la structure (incluant id_projet)
    df_vide = CommonTarifTBSEModel.create_empty_dataframe()
    print("1. DataFrame vide avec colonne id_projet :")
    print(df_vide)
    print()
    
    # Créer le DataFrame avec les données par défaut et id_projet = 1
    df_tarifs = CommonTarifTBSEModel.create_default_dataframe(id_projet_default=1)
    print("2. DataFrame avec données par défaut et id_projet = 1 :")
    print(df_tarifs)
    print()
    
    # Vérification du type de id_projet
    print("3. Vérification de la colonne id_projet :")
    print(f"   Type de id_projet: {df_tarifs['id_projet'].dtype}")
    print(f"   Valeurs uniques: {df_tarifs['id_projet'].unique()}")
    print(f"   Valeur par défaut: {df_tarifs['id_projet'].iloc[0]}")
    
    # Ajouter une nouvelle ligne avec id_projet par défaut (1)
    df_tarifs = CommonTarifTBSEModel.add_row_to_dataframe(
        df_tarifs, "TBSE NOUVEAU", "Abonnement", 60.0000, 0.0000, 60.0000, 1.2000, 61.2000
    )
    print("\n4. Après ajout d'une ligne avec id_projet par défaut :")
    print(df_tarifs)
    
    # Ajouter une ligne avec id_projet différent
    df_tarifs = CommonTarifTBSEModel.add_row_to_dataframe(
        df_tarifs, "TBSE PROJET2", "Prix unitaire (au mètre 3)", 1.5000, 0.1500, 1.6500, 0.0330, 1.6830, id_projet=2
    )
    print("\n5. Après ajout d'une ligne avec id_projet = 2 :")
    print(df_tarifs)