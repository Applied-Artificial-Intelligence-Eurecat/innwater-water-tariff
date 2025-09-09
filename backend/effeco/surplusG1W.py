import sqlite3

class surplusG1W:
    def __init__(self, elasticite_prix_marginal=-0.31):
        self.elasticite_prix_marginal = elasticite_prix_marginal
        self.db_name = None
        self.table_name = None
    
    def init(self, db_name, table_name):
        """Initialise le nom de la base de données et de la table"""
        self.db_name = db_name
        self.table_name = table_name
    
    def mettre_a_jour_donnees(self, id_projet=1):
        """Met à jour la table pour un id_projet spécifique (1 par défaut)"""
        if self.db_name is None or self.table_name is None:
            raise ValueError("La base de données et la table doivent être initialisées avec la méthode init()")
        
        try:
            # Connexion à la base de données
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Exécution de la requête de mise à jour avec filtre sur id_projet
            query = f"""
            UPDATE {self.table_name}
            SET demande_inverse_bi = POWER(ai_m3_jour, 1.0 / ABS(?))
            WHERE id_projet = ?
            """
            
            cursor.execute(query, (self.elasticite_prix_marginal, id_projet))
            
            # Validation des changements et fermeture de la connexion
            conn.commit()
            print(f"Mise à jour effectuée pour id_projet={id_projet}. {cursor.rowcount} lignes modifiées.")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            if conn:
                conn.close()
    
    def mettre_a_jour_tous_projets(self):
        """Met à jour tous les projets de la table (version sans filtre)"""
        if self.db_name is None or self.table_name is None:
            raise ValueError("La base de données et la table doivent être initialisées avec la méthode init()")
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            query = f"""
            UPDATE {self.table_name}
            SET demande_inverse_bi = POWER(ai_m3_jour, 1.0 / ABS(?))
            """
            
            cursor.execute(query, (self.elasticite_prix_marginal,))
            conn.commit()
            
            print(f"Mise à jour globale effectuée. {cursor.rowcount} lignes modifiées.")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            if conn:
                conn.close()
    
    def mettre_a_jour_liste_projets(self, liste_id_projets):
        """Met à jour plusieurs projets spécifiques"""
        if self.db_name is None or self.table_name is None:
            raise ValueError("La base de données et la table doivent être initialisées avec la méthode init()")
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Création des placeholders pour la clause IN
            placeholders = ','.join('?' for _ in liste_id_projets)
            query = f"""
            UPDATE {self.table_name}
            SET demande_inverse_bi = POWER(ai_m3_jour, 1.0 / ABS(?))
            WHERE id_projet IN ({placeholders})
            """
            
            # Paramètres: elasticité + tous les id_projets
            params = [self.elasticite_prix_marginal] + liste_id_projets
            cursor.execute(query, params)
            conn.commit()
            
            print(f"Mise à jour effectuée pour {len(liste_id_projets)} projets. {cursor.rowcount} lignes modifiées.")
            
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            if conn:
                conn.close()


# Exemple d'utilisation dans le main
if __name__ == "__main__":
    # Création de l'instance avec la valeur par défaut
    surplus_manager = surplusG1W()
    
    # Initialisation avec les noms de base et table
    surplus_manager.init("database.db", "surplusG1TBSE")
    
    
    # Mise à jour pour un autre projet spécifique
    surplus_manager.mettre_a_jour_donnees(1)  # Pour le projet 1
    