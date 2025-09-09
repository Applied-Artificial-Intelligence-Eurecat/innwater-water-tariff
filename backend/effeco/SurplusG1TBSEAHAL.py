import sqlite3

class SurplusG1TBSEAHAL:
    def __init__(self, database_name="database.db", table_name="surplusG1TBSE"):
        """
        Constructeur de la classe SurplusG1TBSEAHAL
        
        Args:
            database_name (str): Nom de la base de données
            table_name (str): Nom de la table
        """
        self.database_name = database_name
        self.table_name = table_name
    
    def mettre_a_jour_tbse_ht_trim_i1(self, id_projet):
        """
        Met à jour la colonne tbse_ht_trim_i1 en fonction de l'id_projet
        
        Args:
            id_projet (int): Identifiant du projet pour filtrer la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            # Construction de la requête SQL avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_trim_i1 = tbse_ht_i1 * 90
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(query, (id_projet,))
            
            # Validation des modifications
            conn.commit()
            
            # Vérification du nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour tbse_ht_trim_i1 réussie. {rows_affected} ligne(s) affectée(s).")
            
            # Fermeture de la connexion
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de tbse_ht_trim_i1 : {e}")
            return False
    
    def mettre_a_jour_tbse_ht_trim_i2(self, id_projet):
        """
        Met à jour la colonne tbse_ht_trim_i2 en fonction de l'id_projet
        À exécuter après la mise à jour de tbse_ht_trim_i1
        
        Args:
            id_projet (int): Identifiant du projet pour filtrer la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            # Construction de la requête SQL avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_trim_i2 = tbse_ht_i2 * 90
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(query, (id_projet,))
            
            # Validation des modifications
            conn.commit()
            
            # Vérification du nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour tbse_ht_trim_i2 réussie. {rows_affected} ligne(s) affectée(s).")
            
            # Fermeture de la connexion
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de tbse_ht_trim_i2 : {e}")
            return False
    
    def mettre_a_jour_tbse_ht_trim_t1(self, id_projet):
        """
        Met à jour la colonne tbse_ht_trim_t1 en fonction de l'id_projet
        À exécuter après les mises à jour de tbse_ht_trim_i1 et tbse_ht_trim_i2
        
        Args:
            id_projet (int): Identifiant du projet pour filtrer la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            # Construction de la requête SQL avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_trim_t1 = tbse_ht_trim_i1
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(query, (id_projet,))
            
            # Validation des modifications
            conn.commit()
            
            # Vérification du nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour tbse_ht_trim_t1 réussie. {rows_affected} ligne(s) affectée(s).")
            
            # Fermeture de la connexion
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de tbse_ht_trim_t1 : {e}")
            return False
    
    def mettre_a_jour_tbse_ht_trim_t2(self, id_projet):
        """
        Met à jour la colonne tbse_ht_trim_t2 en fonction de l'id_projet
        À exécuter après les mises à jour de tbse_ht_trim_i1, tbse_ht_trim_i2 et tbse_ht_trim_t1
        
        Args:
            id_projet (int): Identifiant du projet pour filtrer la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            # Construction de la requête SQL avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_trim_t2 = -tbse_ht_trim_i2
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(query, (id_projet,))
            
            # Validation des modifications
            conn.commit()
            
            # Vérification du nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour tbse_ht_trim_t2 réussie. {rows_affected} ligne(s) affectée(s).")
            
            # Fermeture de la connexion
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de tbse_ht_trim_t2 : {e}")
            return False
    
    def mettre_a_jour_tbse_ht_t1_t2_trim_euro_jour(self, id_projet):
        """
        Met à jour la colonne tbse_ht_t1_t2_trim_euro_jour en fonction de l'id_projet
        À exécuter après les mises à jour de tbse_ht_trim_i1, tbse_ht_trim_i2, tbse_ht_trim_t1 et tbse_ht_trim_t2
        
        Args:
            id_projet (int): Identifiant du projet pour filtrer la mise à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            # Construction de la requête SQL avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_t1_t2_trim_euro_jour = tbse_ht_trim_t1 + tbse_ht_trim_t2
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(query, (id_projet,))
            
            # Validation des modifications
            conn.commit()
            
            # Vérification du nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour tbse_ht_t1_t2_trim_euro_jour réussie. {rows_affected} ligne(s) affectée(s).")
            
            # Fermeture de la connexion
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de tbse_ht_t1_t2_trim_euro_jour : {e}")
            return False
    
    def mettre_a_jour_sequence_complete(self, id_projet):
        """
        Exécute la séquence complète de mise à jour :
        1. Mise à jour de tbse_ht_trim_i1
        2. Mise à jour de tbse_ht_trim_i2
        3. Mise à jour de tbse_ht_trim_t1
        4. Mise à jour de tbse_ht_trim_t2
        5. Mise à jour de tbse_ht_t1_t2_trim_euro_jour
        
        Args:
            id_projet (int): Identifiant du projet
            
        Returns:
            bool: True si les cinq mises à jour ont réussi, False sinon
        """
        print(f"Début de la séquence de mise à jour pour le projet {id_projet}")
        
        # Étape 1: Mise à jour de tbse_ht_trim_i1
        success_i1 = self.mettre_a_jour_tbse_ht_trim_i1(id_projet)
        
        if not success_i1:
            print("Échec de la mise à jour de tbse_ht_trim_i1. Arrêt de la séquence.")
            return False
        
        # Étape 2: Mise à jour de tbse_ht_trim_i2 (après i1)
        success_i2 = self.mettre_a_jour_tbse_ht_trim_i2(id_projet)
        
        if not success_i2:
            print("Échec de la mise à jour de tbse_ht_trim_i2.")
            return False
        
        # Étape 3: Mise à jour de tbse_ht_trim_t1 (après i1 et i2)
        success_t1 = self.mettre_a_jour_tbse_ht_trim_t1(id_projet)
        
        if not success_t1:
            print("Échec de la mise à jour de tbse_ht_trim_t1.")
            return False
        
        # Étape 4: Mise à jour de tbse_ht_trim_t2 (après i1, i2 et t1)
        success_t2 = self.mettre_a_jour_tbse_ht_trim_t2(id_projet)
        
        if not success_t2:
            print("Échec de la mise à jour de tbse_ht_trim_t2.")
            return False
        
        # Étape 5: Mise à jour de tbse_ht_t1_t2_trim_euro_jour (après i1, i2, t1 et t2)
        success_euro_jour = self.mettre_a_jour_tbse_ht_t1_t2_trim_euro_jour(id_projet)
        
        if not success_euro_jour:
            print("Échec de la mise à jour de tbse_ht_t1_t2_trim_euro_jour.")
            return False
        
        print("Séquence de mise à jour complète terminée avec succès!")
        return True
    
    def mettre_a_jour_tous_projets_i1(self):
        """
        Met à jour tbse_ht_trim_i1 pour tous les projets (sans filtre)
        """
        return self._mettre_a_jour_tous_projets("tbse_ht_trim_i1", "tbse_ht_i1 * 90")
    
    def mettre_a_jour_tous_projets_i2(self):
        """
        Met à jour tbse_ht_trim_i2 pour tous les projets (sans filtre)
        """
        return self._mettre_a_jour_tous_projets("tbse_ht_trim_i2", "tbse_ht_i2 * 90")
    
    def mettre_a_jour_tous_projets_t1(self):
        """
        Met à jour tbse_ht_trim_t1 pour tous les projets (sans filtre)
        """
        return self._mettre_a_jour_tous_projets("tbse_ht_trim_t1", "tbse_ht_trim_i1")
    
    def mettre_a_jour_tous_projets_t2(self):
        """
        Met à jour tbse_ht_trim_t2 pour tous les projets (sans filtre)
        """
        return self._mettre_a_jour_tous_projets("tbse_ht_trim_t2", "-tbse_ht_trim_i2")
    
    def mettre_a_jour_tous_projets_euro_jour(self):
        """
        Met à jour tbse_ht_t1_t2_trim_euro_jour pour tous les projets (sans filtre)
        """
        return self._mettre_a_jour_tous_projets("tbse_ht_t1_t2_trim_euro_jour", "tbse_ht_trim_t1 + tbse_ht_trim_t2")
    
    def _mettre_a_jour_tous_projets(self, colonne_cible, valeur_calcul):
        """
        Méthode privée pour mettre à jour une colonne pour tous les projets
        
        Args:
            colonne_cible (str): Nom de la colonne à mettre à jour
            valeur_calcul (str): Expression SQL pour calculer la valeur
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            
            query = f"""
            UPDATE {self.table_name}
            SET {colonne_cible} = {valeur_calcul}
            """
            
            cursor.execute(query)
            conn.commit()
            
            rows_affected = cursor.rowcount
            print(f"Mise à jour {colonne_cible} réussie pour tous les projets. {rows_affected} ligne(s) affectée(s).")
            
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de {colonne_cible} : {e}")
            return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance de la classe
    surplus_manager = SurplusG1TBSEAHAL("database.db", "surplusG1TBSE")
    
    # Mise à jour séquentielle complète pour un projet spécifique
    id_projet = 123
    success = surplus_manager.mettre_a_jour_sequence_complete(id_projet)
    
    if success:
        print("Mise à jour séquentielle complète terminée avec succès!")
    else:
        print("Erreur lors de la mise à jour séquentielle.")
    
    # Ou utilisation individuelle des méthodes dans l'ordre spécifié
    print("\nMise à jour individuelle dans l'ordre:")
    id_projet_2 = 456
    
    # Étape 1: Mise à jour de tbse_ht_trim_i1
    surplus_manager.mettre_a_jour_tbse_ht_trim_i1(id_projet_2)
    
    # Étape 2: Mise à jour de tbse_ht_trim_i2
    surplus_manager.mettre_a_jour_tbse_ht_trim_i2(id_projet_2)
    
    # Étape 3: Mise à jour de tbse_ht_trim_t1 (après i1 et i2)
    surplus_manager.mettre_a_jour_tbse_ht_trim_t1(id_projet_2)
    
    # Étape 4: Mise à jour de tbse_ht_trim_t2 (après i1, i2 et t1)
    surplus_manager.mettre_a_jour_tbse_ht_trim_t2(id_projet_2)
    
    # Étape 5: Mise à jour de tbse_ht_t1_t2_trim_euro_jour (après i1, i2, t1 et t2)
    surplus_manager.mettre_a_jour_tbse_ht_t1_t2_trim_euro_jour(id_projet_2)
    
    print("Mise à jour individuelle terminée!")