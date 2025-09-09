import sqlite3

class surplusG1TBSEAM:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def update_diff_qb_app_conso_tbse_pct(self, id_projet):
        """
        Met à jour le champ diff_qb_app_conso_tbse_pct pour un projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        cursor = None
        try:
            if not self.connection:
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            
            # Requête de mise à jour avec condition WHERE pour id_projet
            update_query = """
            UPDATE surplusG1TBSE
            SET diff_qb_app_conso_tbse_pct = 
                ((tbse_conso_app_qb_m3_trim - c_tbse) / NULLIF(c_tbse, 0)) * 100
            WHERE id_projet = ?
            """
            
            # Exécution de la requête avec le paramètre id_projet
            cursor.execute(update_query, (id_projet,))
            
            # Validation des changements
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if cursor.rowcount > 0:
                print(f"Mise à jour réussie pour le projet ID {id_projet}. {cursor.rowcount} ligne(s) modifiée(s).")
                return True
            else:
                print(f"Aucune ligne trouvée pour le projet ID {id_projet}.")
                return False
                
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance de la classe
    surplus_manager = surplusG1TBSEAM('database.db')
    
    # Mise à jour pour un projet spécifique
    id_projet = 1  # Remplacez par l'ID réel du projet
    success = surplus_manager.update_diff_qb_app_conso_tbse_pct(id_projet)
    
    # Mise à jour de tous les projets (optionnel)
    # success = surplus_manager.update_all_projects()
    
    # Fermeture de la connexion
    surplus_manager.disconnect()