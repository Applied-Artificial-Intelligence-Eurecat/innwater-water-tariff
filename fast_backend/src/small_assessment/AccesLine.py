class AccesLine:
    """Représente une ligne de Droit d’Accès avec ses valeurs de sous-taxes."""
    
    def __init__(self, sub_ht_op, sub_redev, sub_hors_tva, sub_tva, sub_ttc):
        self.sub_ht_op = sub_ht_op
        self.sub_redev = sub_redev
        self.sub_hors_tva = sub_hors_tva
        self.sub_tva = sub_tva
        self.sub_ttc = sub_ttc

    def __repr__(self):
        """Affichage lisible de la ligne."""
        return (f"AccesLine(Sub_Tax_HT_Op={self.sub_ht_op:.4f}, "
                f"Sub_Tax_Redevances={self.sub_redev:.4f}, "
                f"Sub_Tax_Hors_TVA={self.sub_hors_tva:.4f}, "
                f"Sub_Tax_TVA={self.sub_tva:.4f}, "
                f"Sub_Tax_TTC={self.sub_ttc:.4f})")

    def to_dict(self):
        """Convertit la ligne en dictionnaire (utile pour pandas ou SQLite)."""
        return {
            "Sub_Tax_HT_Op": self.sub_ht_op,
            "Sub_Tax_Redevances": self.sub_redev,
            "Sub_Tax_Hors_TVA": self.sub_hors_tva,
            "Sub_Tax_TVA": self.sub_tva,
            "Sub_Tax_TTC": self.sub_ttc
        }
