class TarifLine:
    """
    Représente une ligne individuelle d'une table tarifaire.
    """
    def __init__(self, indice: str, seuil: float, prix_ht_operateur: float , 
                 redevance_accise_eur_m3: float = 0.12, taux_tva_pct: float = 2.1):
        self.indice = indice
        self.seuil = seuil
        self.prix_ht_operateur = prix_ht_operateur
        self.redevance = redevance_accise_eur_m3
        self.prix_htva = prix_ht_operateur + redevance_accise_eur_m3
        self.montant_tva_unite = self.prix_htva *(taux_tva_pct/100)
        self.prix_ttc = self.prix_htva + self.montant_tva_unite

    def __repr__(self):
        return (f"TarifLine(indice='{self.indice}', seuil={self.seuil}, "
                f"prix_ht_operateur={self.prix_ht_operateur}, redevance={self.redevance}, "
                f"prix_htva={self.prix_htva}, montant_tva_unite={self.montant_tva_unite}, "
                f"prix_ttc={self.prix_ttc})")


class TarifTab:
    """
    Représente la table complète des tarifs (ensemble de lignes),
    avec la redevance et le taux de TVA associés.
    """
    def __init__(self, redevance_accise_eur_m3: float = 0.12, taux_tva_pct: float = 2.1):
        self.redevance_accise_eur_m3 = redevance_accise_eur_m3
        self.taux_tva_pct = taux_tva_pct
        self.lignes = []

    def ajouter_ligne(self, ligne: TarifLine):
        self.lignes.append(ligne)

    def __repr__(self):
        return (f"TarifTab(redevance_accise_eur_m3={self.redevance_accise_eur_m3}, "
                f"taux_tva_pct={self.taux_tva_pct}, "
                f"lignes={len(self.lignes)})")

    def afficher_table(self):
        print(f"Table tarifaire (redevance_accise_eur_m3={self.redevance_accise_eur_m3}, taux_tva_pct={self.taux_tva_pct})")
        print("indice | seuil | prix_ht_operateur | redevance | prix_htva | montant_tva_unite | prix_ttc")
        print("-" * 90)
        for l in self.lignes:
            print(f"{l.indice:>5} | {l.seuil:>5} | {l.prix_ht_operateur:>17.3f} | {l.redevance:>9.3f} | "
                  f"{l.prix_htva:>9.3f} | {l.montant_tva_unite:>17.6f} | {l.prix_ttc:>8.6f}")
            

class TarifTabMerger:
    """
    Fusionne plusieurs grilles tarifaires progressives (ex : Eau + Assainissement),
    en additionnant toutes les composantes tarifaires tranche à tranche.
    """

    def __init__(self, *tables: TarifTab):
        """
        tables : une ou plusieurs instances de TarifTab
        """
        self.tables = tables

    def merge(self):
        """
        Fusionne les grilles selon leurs seuils et additionne toutes les valeurs :
        redevance, prix_ht_operateur, prix_htva, montant_tva_unite, prix_ttc.
        Retourne une nouvelle instance de TarifTab.
        """
        # 1️⃣ Rassembler tous les seuils uniques
        seuils = sorted(set(l.seuil for t in self.tables for l in t.lignes))

        merged_table = TarifTab()

        for i, s in enumerate(seuils):
            # 2️⃣ Calculer la somme de chaque composante
            total_redevance = sum(self._get_val(t, s, "redevance") for t in self.tables)
            total_prix_ht_op = sum(self._get_val(t, s, "prix_ht_operateur") for t in self.tables)
            total_prix_htva   = sum(self._get_val(t, s, "prix_htva") for t in self.tables)
            total_tva_unite   = sum(self._get_val(t, s, "montant_tva_unite") for t in self.tables)
            total_prix_ttc    = sum(self._get_val(t, s, "prix_ttc") for t in self.tables)

            # 3️⃣ Construire une ligne fusionnée
            merged_line = TarifLine(
                indice=f"k{i}",
                seuil=s,
                prix_ht_operateur=total_prix_ht_op,
                redevance_accise_eur_m3=total_redevance,
                taux_tva_pct=0.0  # pas de recalcul : valeurs déjà TTC
            )

            # ⚙️ Écrasement des champs calculés pour refléter la somme exacte
            merged_line.prix_htva = total_prix_htva
            merged_line.montant_tva_unite = total_tva_unite
            merged_line.prix_ttc = total_prix_ttc

            merged_table.ajouter_ligne(merged_line)

        return merged_table

    # Fonction auxiliaire
    def _get_val(self, table: TarifTab, seuil: float, attr: str) -> float:
        """
        Récupère la valeur de l'attribut (prix_ht, prix_ttc, etc.) 
        pour le seuil donné dans une table tarifaire.
        """
        lignes = table.lignes
        for i in range(len(lignes) - 1):
            if lignes[i].seuil <= seuil < lignes[i + 1].seuil:
                return getattr(lignes[i], attr)
        return getattr(lignes[-1], attr)



def main():
    # Création de la table avec les valeurs par défaut (0.12 et 2.1)
    table = TarifTab()

    # Si besoin, tu peux changer les valeurs ici :
    # table = TarifTab(redevance_accise_eur_m3=0.15, taux_tva_pct=5.5)

    # Ajout des lignes
    table.ajouter_ligne(TarifLine("k0", 0, 0.878,  redevance_accise_eur_m3 = 0.12, taux_tva_pct= 2.1))
    table.ajouter_ligne(TarifLine("k1", 15, 1.839, redevance_accise_eur_m3 = 0.12, taux_tva_pct= 2.1))
    table.ajouter_ligne(TarifLine("k2", 30, 2.768, redevance_accise_eur_m3 = 0.12, taux_tva_pct= 2.1))
    table.ajouter_ligne(TarifLine("k3", 60, 4.38, redevance_accise_eur_m3 = 0.12, taux_tva_pct= 2.1))

    # Affichage
    table.afficher_table()



    
    tableA = TarifTab(redevance_accise_eur_m3=0.04, taux_tva_pct=10.0)

    # Ajout des lignes (nouvelles valeurs)
    tableA.ajouter_ligne(TarifLine("k0", 0, 1.3, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k1", 15, 2.12,redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k2", 30, 2.21, redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))
    tableA.ajouter_ligne(TarifLine("k3", 60, 2.5,redevance_accise_eur_m3=0.04, taux_tva_pct=10.0))

    # Affichage
    tableA.afficher_table()


    # --- Fusion des deux tables ---
    # Supposons que ta classe de fusion s'appelle TarifTabMerger
    merger = TarifTabMerger(table, tableA)
    table_fusionnee = merger.merge()

    print("\n=== Grille Fusionnée Eau + Assainissement ===")
    table_fusionnee.afficher_table()


if __name__ == "__main__":
    main()
