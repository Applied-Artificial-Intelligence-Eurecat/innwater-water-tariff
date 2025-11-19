import pandas as pd

class subTaxRow:
    """Représente une ligne de la table SubTax"""
    def __init__(self, indice, seuil, prix_m3, volume, taux_tva=0.2, redevance=0.0):
        self.indice = indice
        self.seuil = seuil
        self.prix_m3 = prix_m3
        self.volume = volume
        self.taux_tva = taux_tva
        self.redevance = redevance

        # --- Calculs automatiques ---
        self.sub_ht_op = self.volume * self.prix_m3
        self.sub_redev = self.volume * self.redevance
        self.sub_hors_tva = self.sub_ht_op + self.sub_redev
        self.sub_tva = self.sub_hors_tva * self.taux_tva
        self.sub_ttc = self.sub_hors_tva + self.sub_tva

    def to_dict(self):
        """Convertit la ligne en dictionnaire pour pandas ou SQL"""
        return {
            "indice": self.indice,
            "seuil": self.seuil,
            "prix_m3": self.prix_m3,
            "volume": self.volume,
            "Sub_Tax_HT_Op": self.sub_ht_op,
            "Sub_Tax_Redevances": self.sub_redev,
            "Sub_Tax_Hors_TVA": self.sub_hors_tva,
            "Sub_Tax_TVA": self.sub_tva,
            "Sub_Tax_TTC": self.sub_ttc
        }


class subTaxTable:
    """Contient un ensemble de SubTaxRow, initialisé à partir d'une liste de paliers (tiers)"""
    def __init__(self, tiers=None, volume=15, couts_du_Service_EP=0.9,
                taux_tva=0.2, redevance=0.05, redevance_ep=0.12, redance_TBSE_EP=0.12, mnt_TVA_unite_service_pu=0.02142):
        """
        Initialise la table de sous-taxes à partir d'une liste de paliers (tiers)
        et des paramètres économiques associés.
        """
        # Si aucun palier n'est fourni, on prend la grille par défaut
        if tiers is None:
            self.tiers = [
                {"seuil": 0.0, "prix": 0.878},
                {"seuil": 15.0, "prix": 1.839},
                {"seuil": 30.0, "prix": 2.768},
                {"seuil": 60.0, "prix": 4.38}
            ]
        else:
            self.tiers = tiers

        # 🔹 Définition des attributs utilisés dans les méthodes suivantes
        self.redevance_ep = redevance_ep
        self.taux_tva = taux_tva
        self.rows = []

        # 🔹 Construction des lignes à partir des paliers
        self._build_from_tiers(
            self.tiers,
            volume,
            couts_du_Service_EP,
            taux_tva,
            redevance,
            redevance_ep,
            redance_TBSE_EP
        )

        # 🔹 Calculs après initialisation complète UTIL
        self.prix_h_tva = self.calculer_prix_h_tva()
        self.montant_tva_unite = self.calculer_montant_tva_unite()
        self.mnt_TVA_unite_service_pu= mnt_TVA_unite_service_pu
        
        self.Sub_Tax_TTC= self.calculer_sub_tva(mnt_TVA_unite_service_pu)

        


    def _build_from_tiers(self, tiers, volume, couts_du_Service_EP,  taux_tva, redevance, redevance_ep=0.12, redance_TBSE_EP=0.12):
        """Construit la table à partir des données de paliers"""
        for i, tier in enumerate(tiers, start=1):
            row = subTaxRow(
                indice=i,
                seuil=tier["seuil"],
                prix_m3=tier["prix"],
                volume=volume,
                taux_tva=taux_tva,
                redevance=redevance
            )
            row.sub_ht_op= tier["prix"]- couts_du_Service_EP
            row.sub_redev = redevance_ep - redance_TBSE_EP
            row.sub_hors_tva= row.sub_ht_op + row.sub_redev
           
            self.rows.append(row)


    def to_dataframe(self):
        """Convertit la table entière en DataFrame pandas"""
        if not self.rows:
            return pd.DataFrame()
        return pd.DataFrame([r.to_dict() for r in self.rows])

    def show(self):
        """Affiche le contenu de la table"""
        df = self.to_dataframe()
        if df.empty:
            print("Table vide.")
        else:
            print(df.to_string(index=False))

    def calculer_prix_h_tva(self):
        """
        Calcule le 'Prix H TVA' pour chaque tier :
        prix × redevance_ep
        et stocke le résultat dans self.prix_h_tva
        """
        self.prix_h_tva = [round(t["prix"] + self.redevance_ep, 3) for t in self.tiers]
        return self.prix_h_tva

    def calculer_montant_tva_unite(self):
        """
        Calcule le montant de TVA par unité de service :
        (prix + redevance) × (taux_tva / 100)
        = prix × (1 + redevance_ep) × (taux_tva / 100)
        """
        self.montant_tva_unite = [
            round(prix_h_tva *  (self.taux_tva / 100), 6)
            for prix_h_tva in self.prix_h_tva
        ]
        return self.montant_tva_unite
    
    def calculer_sub_tva(self, mnt_TVA_unite_service_pu):
        """
        Calcule le montant TTC par unité de service :
        TTC = Prix Hors TVA + Montant TVA
        """
        valuesTTCs = []
        for pht  in self.montant_tva_unite:
            
            valuesTTC = round(pht - mnt_TVA_unite_service_pu, 6)
            print(f'pht:{pht} ; mntTva : {0.2142}; valuesTTC: {valuesTTC}')
            valuesTTCs.append(valuesTTC)
        
        self.Sub_Tax_TTC = valuesTTCs
        for row, val in zip(self.rows, valuesTTCs):
            # Mise à jour de la ligne individuelle
            row.sub_tva = val
        return valuesTTCs
    
    def calculer_Sub_Tax_TTC(self):
        """
        Calcule le montant TTC par unité de service :
        TTC = Prix Hors TVA + Montant TVA
        """
        for row, val in zip(self.rows):
            # Mise à jour de la ligne individuelle
            row.sub_ttc= row.sub_hors_tva + row.sub_tva

    def get_all_sub_ht_op(self):
        """
        Retourne un ensemble (set) des valeurs de l'attribut sub_ht_op
        pour toutes les lignes de la table.
        """
        return {row.sub_ht_op for row in self.rows}
    
    def get_sub_ht_op_dict(self):
        """
        Retourne un dictionnaire {J1: val1, J2: val2, ..., Jn: valn}
        basé sur les valeurs sub_ht_op dans l'ordre des lignes.
        """
        return {f'J{i+1}': row.sub_ht_op for i, row in enumerate(self.rows)}
    

    def get_sub_tax_redevances(self):
        """
        Retourne une liste des valeurs de Sub Tax Redevances (sub_redev)
        pour toutes les lignes de la table.
        
        Returns:
            list: Liste des valeurs sub_redev arrondies à 4 décimales
        """
        return [round(row.sub_redev, 4) for row in self.rows]


    # Alternative : Si vous voulez aussi un dictionnaire
    def get_sub_tax_redevances_dict(self):
        """
        Retourne un dictionnaire {J1: val1, J2: val2, ..., Jn: valn}
        basé sur les valeurs sub_redev dans l'ordre des lignes.
        
        Returns:
            dict: Dictionnaire avec les clés J1, J2, etc.
        """
        return {f'J{i+1}': round(row.sub_redev, 4) for i, row in enumerate(self.rows)}


    def get_sub_tax_tva(self):
        """
        Retourne une liste des valeurs de Sub Tax TVA (sub_tva)
        pour toutes les lignes de la table.
        
        Returns:
            list: Liste des valeurs sub_tva arrondies à 4 décimales
        """
        return [round(row.sub_tva, 4) for row in self.rows]


    # Alternative : Si vous voulez aussi un dictionnaire
    def get_sub_tax_tva_dict(self):
        """
        Retourne un dictionnaire {J1: val1, J2: val2, ..., Jn: valn}
        basé sur les valeurs sub_tva dans l'ordre des lignes.
        
        Returns:
            dict: Dictionnaire avec les clés J1, J2, etc.
        """
        return {f'J{i+1}': round(row.sub_tva, 4) for i, row in enumerate(self.rows)}


    # Exemple d'utilisation   classe :
    # """
    # table = subTaxTable()

    # # Récupérer la liste des redevances
    # redevances = table.get_sub_tax_redevances()
    # print(redevances)
    # # Output: [0.0, 0.0, 0.0, 0.0]

    # # Ou sous forme de dictionnaire
    # redevances_dict = table.get_sub_tax_redevances_dict()
    # print(redevances_dict)
    # # Output: {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0}

    # # Récupérer la liste des TVA
    # tva = table.get_sub_tax_tva()
    # print(tva)
    # # Output: [-0.595, -0.0005, 0.0197, 0.0392, 0.0731]

    # # Ou sous forme de dictionnaire
    # tva_dict = table.get_sub_tax_tva_dict()
    # print(tva_dict)
    # # Output: {'J1': -0.595, 'J2': -0.0005, 'J3': 0.0197, 'J4': 0.0392, 'J5': 0.0731}
    # """
   

# --- Exemple d’utilisation ---
if __name__ == "__main__":
    table = subTaxTable()
    table.add_row(subTaxRow("k0", 0, -0.0220, 0.0000, -0.0220, -0.0005, -0.0225))
    table.add_row(subTaxRow("k1", 15, 0.9390, 0.0000, 0.9390, 0.0197, 0.9587))
    table.add_row(subTaxRow("k2", 30, 1.8680, 0.0000, 1.8680, 0.0392, 1.9072))
    table.add_row(subTaxRow("k3", 60, 3.4800, 0.0000, 3.4800, 0.0731, 3.5531))

    table.show()
    ##table.insert_into_db()
