class NordinLine:
    """
    Représente une ligne de données avec deux séries de valeurs :
    une principale et une secondaire.
    """

    def __init__(self, numero_tranche,
                 operateur1, agence1, etat1, total1,
                 operateur2=None, agence2=None, etat2=None, total2=None):
        self.numero_tranche = numero_tranche
        self.operateur1 = operateur1
        self.agence1 = agence1
        self.etat1 = etat1
        self.total1 = total1
        self.operateur2 = operateur2
        self.agence2 = agence2
        self.etat2 = etat2
        self.total2 = total2

    def __repr__(self):
        return (f"NordinLine({self.numero_tranche!r}, "
                f"{self.operateur1}, {self.agence1}, {self.etat1}, {self.total1}, "
                f"{self.operateur2}, {self.agence2}, {self.etat2}, {self.total2})")

    def to_dict(self):
        """Retourne les données sous forme de dictionnaire."""
        return {
            "N° Tranche": self.numero_tranche,
            "Opérateur_1": self.operateur1,
            "Agence_1": self.agence1,
            "État_1": self.etat1,
            "Total_1": self.total1,
            "Opérateur_2": self.operateur2,
            "Agence_2": self.agence2,
            "État_2": self.etat2,
            "Total_2": self.total2
        }

    def total_general(self):
        """Retourne la somme des deux totaux si disponibles."""
        total = 0
        if self.total1 is not None:
            total += self.total1
        if self.total2 is not None:
            total += self.total2
        return total


class NordinTable:
    """
    Représente une table composée de plusieurs objets NordinLine.
    """

    def __init__(self):
        self.lignes = []

    def ajouter_ligne(self, nordin_line):
        """Ajoute un objet NordinLine à la table."""
        if not isinstance(nordin_line, NordinLine):
            raise TypeError("L’objet ajouté doit être une instance de NordinLine.")
        self.lignes.append(nordin_line)

    def total_general(self):
        """Calcule la somme totale de tous les totaux."""
        return sum(l.total_general() for l in self.lignes)

    def afficher(self):
        """Affiche la table sous forme lisible."""
        print(f"{'Tranche':<8} {'Op1':>10} {'Ag1':>10} {'Etat1':>10} {'Tot1':>10} | {'Op2':>10} {'Ag2':>10} {'Etat2':>10} {'Tot2':>10}")
        print("-" * 90)
        for l in self.lignes:
            print(f"{l.numero_tranche:<8} {l.operateur1:>10.4f} {l.agence1:>10.4f} {l.etat1:>10.4f} {l.total1:>10.4f} | "
                  f"{l.operateur2:>10.4f} {l.agence2:>10.4f} {l.etat2:>10.4f} {l.total2:>10.4f}")

    def to_dict_list(self):
        """Retourne la table sous forme de liste de dictionnaires."""
        return [l.to_dict() for l in self.lignes]
    



class NordinAccessLine:
    """
    Représente une ligne simple de données :
    Opérateur | Agence | État | Total
    Exemple :
        -30.4366 | 0.0000 | -0.6392 | -31.0758
    """

    def __init__(self, operateur, agence, etat, total):
        self.operateur = operateur
        self.agence = agence
        self.etat = etat
        self.total = total

    def __repr__(self):
        return (f"NordinAccessLine(Opérateur={self.operateur}, "
                f"Agence={self.agence}, État={self.etat}, Total={self.total})")

    def to_dict(self):
        """Retourne la ligne sous forme de dictionnaire."""
        return {
            "Opérateur": self.operateur,
            "Agence": self.agence,
            "État": self.etat,
            "Total": self.total
        }

    def somme(self):
        """Calcule la somme de tous les champs numériques."""
        return (self.operateur or 0) + (self.agence or 0) + (self.etat or 0) + (self.total or 0)

    def afficher(self):
        """Affiche la ligne sous forme formatée."""
        print(f"{'Opérateur':<12}{'Agence':<10}{'État':<10}{'Total':<10}")
        print("-" * 42)
        print(f"{self.operateur:>10.4f} {self.agence:>10.4f} {self.etat:>10.4f} {self.total:>10.4f}")




def main():
    ### creation de l'acces line : 

     # Création d'une ligne d'accès Nordin
    ligne = NordinAccessLine(-30.4366, 0.0000, -0.6392, -31.0758)

    # Affichage lisible
    print("\n=== NORDIN ACCESS LINE ===")
    ligne.afficher()

    # Dictionnaire
    print("\nDonnées en dictionnaire :")
    print(ligne.to_dict())

    # Somme simple
    print("\nSomme totale des valeurs :", ligne.somme())
    
    
    # Création de la table



    table = NordinTable()

    # Ajout des lignes fournies
    table.ajouter_ligne(NordinLine("T1", -30.4366, 0.0000, -0.6392, -31.0758, -0.0220, 0.0000, -0.0005, -0.0225))
    table.ajouter_ligne(NordinLine("T2", -44.8516, 0.0000, -0.9419, -45.7935,  0.9390, 0.0000,  0.0197,  0.9587))
    table.ajouter_ligne(NordinLine("T3", -72.7216, 0.0000, -1.5272, -74.2488,  1.8680, 0.0000,  0.0392,  1.9072))
    table.ajouter_ligne(NordinLine("T4", -169.4416, 0.0000, -3.5583, -172.9999,  3.4800, 0.0000,  0.0731,  3.5531))

    # Affichage de la table
    print("\n=== TABLE NORDIN ===")
    table.afficher()

    # Calcul et affichage du total général
    print("\nTotal général de la table :", round(table.total_general(), 4))

    # Export en dictionnaire
    print("\n=== Représentation en dictionnaire ===")
    for ligne_dict in table.to_dict_list():
        print(ligne_dict)


if __name__ == "__main__":
    main()