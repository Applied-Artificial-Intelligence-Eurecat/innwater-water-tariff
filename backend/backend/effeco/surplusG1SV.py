import sqlite3

class surplusG1SV:
    def __init__(self, db_name="database.db", elasticite_revenu_virtuel=0.25, 
                 cout_marginal_complet=5.9, elasticite_prix_marginal=-0.31):
        self.db_name = db_name
        self.elasticite_revenu_virtuel = elasticite_revenu_virtuel
        self.cout_marginal_complet = cout_marginal_complet
        self.elasticite_prix_marginal = elasticite_prix_marginal
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connexion à {self.db_name} établie avec succès")
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            print("Connexion fermée")
    
    def update_ai_m3_jour(self, id_projet=1):
        """
        Met à jour la colonne ai_m3_jour selon la formule spécifiée
        
        Args:
            id_projet (int): ID du projet spécifique à mettre à jour. Par défaut 1.
        """
        if not self.connection:
            print("Veuillez d'abord établir une connexion avec connect()")
            return False
        
        try:
            # Construction de la requête avec id_projet
            update_query = f"""
            UPDATE surplusG1TBSE
            SET ai_m3_jour = (c_m3_trim_1 / 90.0) * POWER((revenu_net_mois / 30.0), {self.elasticite_revenu_virtuel})
            WHERE id_projet = {id_projet}
            """
            
            self.cursor.execute(update_query)
            self.connection.commit()
            
            rows_updated = self.cursor.rowcount
            print(f"Mise à jour de ai_m3_jour terminée pour id_projet {id_projet}. {rows_updated} lignes modifiées.")
            print(f"Élasticité Revenu Virtuel utilisée: {self.elasticite_revenu_virtuel}")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de ai_m3_jour: {e}")
            self.connection.rollback()
            return False

    def update_qstar_m3_jour(self, id_projet=1):
        """
        Met à jour la colonne qstar_m3_jour après le calcul de ai_m3_jour
        
        Args:
            id_projet (int): ID du projet spécifique à mettre à jour. Par défaut 1.
        """
        if not self.connection:
            print("Veuillez d'abord établir une connexion avec connect()")
            return False
        
        try:
            # Construction de la requête avec id_projet
            update_query = f"""
            UPDATE surplusG1TBSE
            SET qstar_m3_jour = ai_m3_jour / POWER({self.cout_marginal_complet}, ABS({self.elasticite_prix_marginal}))
            WHERE id_projet = {id_projet}
            """
            
            self.cursor.execute(update_query)
            self.connection.commit()
            
            rows_updated = self.cursor.rowcount
            print(f"Mise à jour de qstar_m3_jour terminée pour id_projet {id_projet}. {rows_updated} lignes modifiées.")
            print(f"Paramètres utilisés - Coût marginal complet: {self.cout_marginal_complet}, Élasticité prix marginal: {self.elasticite_prix_marginal}")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de qstar_m3_jour: {e}")
            self.connection.rollback()
            return False

    def update_conso_qstar_cout_complet(self, id_projet=1):
        """
        Met à jour la colonne conso_qstar_cout_complet_m3_trim après le calcul de qstar_m3_jour
        
        Args:
            id_projet (int): ID du projet spécifique à mettre à jour. Par défaut 1.
        """
        if not self.connection:
            print("Veuillez d'abord établir une connexion avec connect()")
            return False
        
        try:
            # Construction de la requête avec id_projet
            update_query = f"""
            UPDATE surplusG1TBSE
            SET conso_qstar_cout_complet_m3_trim = qstar_m3_jour * 90.0
            WHERE id_projet = {id_projet}
            """
            
            self.cursor.execute(update_query)
            self.connection.commit()
            
            rows_updated = self.cursor.rowcount
            print(f"Mise à jour de conso_qstar_cout_complet_m3_trim terminée pour id_projet {id_projet}. {rows_updated} lignes modifiées.")
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de conso_qstar_cout_complet_m3_trim: {e}")
            self.connection.rollback()
            return False
    
    def set_elasticite_revenu_virtuel(self, nouvelle_elasticite):
        """Modifie la valeur de l'élasticité revenu virtuel"""
        self.elasticite_revenu_virtuel = nouvelle_elasticite
        print(f"Élasticité Revenu Virtuel mise à jour: {nouvelle_elasticite}")
    
    def set_cout_marginal_complet(self, nouveau_cout):
        """Modifie la valeur du coût marginal complet"""
        self.cout_marginal_complet = nouveau_cout
        print(f"Coût marginal complet mis à jour: {nouveau_cout}")
    
    def set_elasticite_prix_marginal(self, nouvelle_elasticite):
        """Modifie la valeur de l'élasticité prix marginal"""
        self.elasticite_prix_marginal = nouvelle_elasticite
        print(f"Élasticité prix marginal mise à jour: {nouvelle_elasticite}")
    
    def get_elasticite_revenu_virtuel(self):
        """Retourne la valeur actuelle de l'élasticité revenu virtuel"""
        return self.elasticite_revenu_virtuel
    
    def get_cout_marginal_complet(self):
        """Retourne la valeur actuelle du coût marginal complet"""
        return self.cout_marginal_complet
    
    def get_elasticite_prix_marginal(self):
        """Retourne la valeur actuelle de l'élasticité prix marginal"""
        return self.elasticite_prix_marginal
    
    def execute_full_update(self, id_projet=1):
        """
        Méthode complète pour exécuter les trois mises à jour en séquence
        
        Args:
            id_projet (int): ID du projet spécifique à mettre à jour. Par défaut 1.
        """
        if self.connect():
            # 1. Mettre à jour ai_m3_jour
            success1 = self.update_ai_m3_jour(id_projet)
            
            # 2. Mettre à jour qstar_m3_jour (seulement si la première mise à jour a réussi)
            success2 = False
            if success1:
                success2 = self.update_qstar_m3_jour(id_projet)
            
            # 3. Mettre à jour conso_qstar_cout_complet_m3_trim (seulement si les deux premières ont réussi)
            success3 = False
            if success1 and success2:
                success3 = self.update_conso_qstar_cout_complet(id_projet)
                
            self.disconnect()
            return success1 and success2 and success3
        return False

# Exemple d'utilisation dans le main
if __name__ == "__main__":
    # Définition des paramètres dans le main
    ID_PROJET = 1  # ID du projet fixé à 1
    
    # Paramètres économiques avec valeurs par défaut
    Cout_marginal_complet = 5.9
    Elasticite_prix_marginal = -0.31
    Elasticite_Revenu_Virtuel = 0.25
    
    print("=== Test avec id_projet = 1 et paramètres dans le constructeur ===\n")
    
    # Test avec valeurs par défaut
    print("1. Test avec toutes les valeurs par défaut:")
    surplus_updater1 = surplusG1SV()
    print(f"ID Projet: {ID_PROJET}")
    print(f"Élasticité Revenu Virtuel: {surplus_updater1.get_elasticite_revenu_virtuel()}")
    print(f"Coût marginal complet: {surplus_updater1.get_cout_marginal_complet()}")
    print(f"Élasticité prix marginal: {surplus_updater1.get_elasticite_prix_marginal()}")
    surplus_updater1.execute_full_update(ID_PROJET)
    print()
    
    if surplus_updater1.connect():
        surplus_updater1.update_ai_m3_jour(ID_PROJET)
        surplus_updater1.update_qstar_m3_jour(ID_PROJET)
        surplus_updater1.update_conso_qstar_cout_complet(ID_PROJET)
        surplus_updater1.disconnect()
    print()
    
