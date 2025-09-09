import sqlite3
from typing import Optional

class Var_PAR_menages_ACAH:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> None:
        """Établir la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            print(f"Connexion à la base de données {self.db_path} établie avec succès")
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def disconnect(self) -> None:
        """Fermer la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")
    
    def update_sepa_columns(self, id_projet: int) -> bool:
        """
        Met à jour les colonnes sepa_* pour un projet spécifique
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        if not self.connection:
            print("Aucune connexion à la base de données")
            return False
        
        try:
            # Requête SQL pour mettre à jour les colonnes sepa_*
            query = """
            UPDATE VarParMenageResult
            SET 
                sepa_t0_ibt = sep_t0_ibt_ep + a_t0_ibt,
                sepa_tmin_ibt = sep_tmin_ibt_ep + a_tmin_ibt,
                sepa_t_ibt = sep_t_ibt_ep + a_t_ibt,
                sepa_t_ibt_pp = sep_t_ibt_pp_ep + a_t_ibt_pp,
                sepa_t0_tbse = sep_t0_tbse_ep + a_t0_tbse,
                sepa_tmin_tbse = sep_tmin_tbse_ep + a_tmin_tbse,
                sepa_t_tbse = sep_t_tbse_ep + a_t_tbse
            WHERE id_projet = ?
            """
            
            cursor = self.connection.cursor()
            cursor.execute(query, (id_projet,))
            
            # Valider la transaction
            self.connection.commit()
            
            # Afficher le nombre de lignes affectées
            rows_affected = cursor.rowcount
            print(f"Mise à jour réussie pour le projet ID {id_projet}")
            print(f"Nombre de lignes affectées: {rows_affected}")
            
            cursor.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")
            # Annuler la transaction en cas d'erreur
            self.connection.rollback()
            return False
    
    def execute_with_context(self, id_projet: int) -> bool:
        """
        Méthode utilitaire pour exécuter avec gestion automatique de la connexion
        
        Args:
            id_projet (int): L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            self.connect()
            return self.update_sepa_columns(id_projet)
        except Exception as e:
            print(f"Erreur lors de l'exécution: {e}")
            return False
        finally:
            self.disconnect()

# Exemple d'utilisation de la classe
if __name__ == "__main__":
    # Créer une instance de la classe
    menages_acah = Var_PAR_menages_ACAH("database.db")
    
    # ID du projet à mettre à jour (à adapter selon vos besoins)
    projet_id = 1
    
    # Méthode 1: Utilisation avec gestion manuelle de la connexion
    try:
        menages_acah.connect()
        success = menages_acah.update_sepa_columns(projet_id)
        if success:
            print("Opération terminée avec succès")
        else:
            print("L'opération a échoué")
    finally:
        menages_acah.disconnect()
    
    # Méthode 2: Utilisation avec gestion automatique de la connexion
    success = menages_acah.execute_with_context(projet_id)
    if success:
        print("Opération terminée avec succès (méthode 2)")
    else:
        print("L'opération a échoué (méthode 2)")