import sqlite3
import logging
import math

class surplusG1TBSEYAF:
    def __init__(self, db_name='database.db', table_name='surplusG1TBSE', 
                 elasticite_revenu_virtuel=0.25, elasticite_prix_marginal=-0.31, 
                 prix_pi=0.9, cout_marginal_complet=5.9):
        """
        Initialise la classe avec les paramètres de configuration
        
        Args:
            db_name (str): Nom de la base de données (par défaut: 'database.db')
            table_name (str): Nom de la table (par défaut: 'surplusG1TBSE')
            elasticite_revenu_virtuel (float): Élasticité revenu virtuel (par défaut: 0.25)
            elasticite_prix_marginal (float): Élasticité prix marginal (par défaut: -0.31)
            prix_pi (float): Prix pi (par défaut: 0.9)
            cout_marginal_complet (float): Coût marginal complet (Cme) (par défaut: 5.9)
        """
        self.db_name = db_name
        self.table_name = table_name
        self.elasticite_revenu_virtuel = elasticite_revenu_virtuel
        self.elasticite_prix_marginal = elasticite_prix_marginal
        self.prix_pi = prix_pi
        self.cout_marginal_complet = cout_marginal_complet
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            # Ajout des fonctions mathématiques à SQLite
            self.connection.create_function("LN", 1, lambda x: math.log(x) if x > 0 else None)
            self.connection.create_function("EXP", 1, lambda x: math.exp(x) if x is not None else None)
            self.connection.create_function("POWER", 2, lambda x, y: math.pow(x, y) if x is not None and y is not None else None)
            self.connection.create_function("ABS", 1, lambda x: abs(x) if x is not None else None)
            self.cursor = self.connection.cursor()
            logging.info(f"Connexion à la base de données {self.db_name} établie avec succès")
            return True
        except sqlite3.Error as e:
            logging.error(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            logging.info("Connexion à la base de données fermée")
    
    def update_tbse_conso_ln(self, id_projet):
        """
        Met à jour la colonne tbse_conso_app_ln_qb pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour avec les paramètres dynamiques
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_conso_app_ln_qb = LN(c_m3_trim_1 / 90)
                              + (? * LN(revenu_net_mois / 30))
                              - (ABS(?) * LN(?))
            WHERE id_projet = ?
            """
            
            # Paramètres pour la requête
            params = (
                self.elasticite_revenu_virtuel,
                self.elasticite_prix_marginal,
                self.prix_pi,
                id_projet
            )
            
            # Exécution de la requête
            self.cursor.execute(update_query, params)
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour LN réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (LN)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour LN: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour LN: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_conso_exp(self, id_projet):
        """
        Met à jour la colonne tbse_conso_app_qb_m3_jour en appliquant EXP à tbse_conso_app_ln_qb
        pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_conso_app_qb_m3_jour = EXP(tbse_conso_app_ln_qb)
            WHERE id_projet = ?
            """
            
            # Exécution de la requête
            self.cursor.execute(update_query, (id_projet,))
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour EXP réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (EXP)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour EXP: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour EXP: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_conso_trim(self, id_projet):
        """
        Met à jour la colonne tbse_conso_app_qb_m3_trim en multipliant tbse_conso_app_qb_m3_jour par 90
        pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_conso_app_qb_m3_trim = tbse_conso_app_qb_m3_jour * 90
            WHERE id_projet = ?
            """
            
            # Exécution de la requête
            self.cursor.execute(update_query, (id_projet,))
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour TRIM réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (TRIM)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour TRIM: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour TRIM: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_ht_i1(self, id_projet):
        """
        Met à jour la colonne tbse_ht_i1 pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_i1 = (ABS(?) * demande_inverse_bi) / (1 - ABS(?))
                          * ( POWER(qstar_m3_jour, -(1 - ABS(?)) / ABS(?))
                            - POWER(tbse_conso_app_qb_m3_jour, -(1 - ABS(?)) / ABS(?)) )
            WHERE id_projet = ?
            """
            
            # Paramètres pour la requête (élasticité_prix_marginal répété pour chaque placeholder)
            params = (
                self.elasticite_prix_marginal,  # ABS(?)
                self.elasticite_prix_marginal,  # 1 - ABS(?)
                self.elasticite_prix_marginal,  # POWER(qstar..., -(1 - ABS(?))
                self.elasticite_prix_marginal,  # / ABS(?)
                self.elasticite_prix_marginal,  # POWER(tbse..., -(1 - ABS(?))
                self.elasticite_prix_marginal,  # / ABS(?)
                id_projet
            )
            
            # Exécution de la requête
            self.cursor.execute(update_query, params)
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour HT_I1 réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (HT_I1)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour HT_I1: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour HT_I1: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_ht_i2(self, id_projet):
        """
        Met à jour la colonne tbse_ht_i2 pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_i2 = ? * (tbse_conso_app_qb_m3_jour - qstar_m3_jour)
            WHERE id_projet = ?
            """
            
            # Paramètres pour la requête
            params = (
                self.cout_marginal_complet,
                id_projet
            )
            
            # Exécution de la requête
            self.cursor.execute(update_query, params)
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour HT_I2 réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (HT_I2)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour HT_I2: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour HT_I2: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_ht_t1(self, id_projet):
        """
        Met à jour la colonne tbse_ht_t1 en copiant la valeur de tbse_ht_i1
        pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_t1 = tbse_ht_i1
            WHERE id_projet = ?
            """
            
            # Exécution de la requête
            self.cursor.execute(update_query, (id_projet,))
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour HT_T1 réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (HT_T1)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour HT_T1: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour HT_T1: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_ht_t2(self, id_projet):
        """
        Met à jour la colonne tbse_ht_t2 en prenant l'opposé de tbse_ht_i2
        pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_t2 = -tbse_ht_i2
            WHERE id_projet = ?
            """
            
            # Exécution de la requête
            self.cursor.execute(update_query, (id_projet,))
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour HT_T2 réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (HT_T2)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour HT_T2: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour HT_T2: {e}")
            self.connection.rollback()
            return False
    
    def update_tbse_ht_t1_t2_euro_jour(self, id_projet):
        """
        Met à jour la colonne tbse_ht_t1_t2_euro_jour en additionnant tbse_ht_t1 et tbse_ht_t2
        pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            # Requête SQL de mise à jour
            update_query = f"""
            UPDATE {self.table_name}
            SET tbse_ht_t1_t2_euro_jour = tbse_ht_t1 + tbse_ht_t2
            WHERE id_projet = ?
            """
            
            # Exécution de la requête
            self.cursor.execute(update_query, (id_projet,))
            self.connection.commit()
            
            # Vérification si des lignes ont été affectées
            if self.cursor.rowcount > 0:
                logging.info(f"Mise à jour HT_T1_T2_EURO_JOUR réussie pour l'id_projet {id_projet}. {self.cursor.rowcount} ligne(s) affectée(s)")
                return True
            else:
                logging.warning(f"Aucune ligne trouvée pour l'id_projet {id_projet} (HT_T1_T2_EURO_JOUR)")
                return False
                
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la mise à jour HT_T1_T2_EURO_JOUR: {e}")
            self.connection.rollback()
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la mise à jour HT_T1_T2_EURO_JOUR: {e}")
            self.connection.rollback()
            return False
    
    def update_all_for_project(self, id_projet):
        """
        Met à jour les huit colonnes successivement pour un id_projet donné
        
        Args:
            id_projet: L'identifiant du projet à mettre à jour
            
        Returns:
            tuple: (success_ln, success_exp, success_trim, success_ht_i1, success_ht_i2, 
                    success_ht_t1, success_ht_t2, success_ht_t1_t2_euro_jour) résultats des huit mises à jour
        """
        success_ln = self.update_tbse_conso_ln(id_projet)
        if success_ln:
            success_exp = self.update_tbse_conso_exp(id_projet)
            if success_exp:
                success_trim = self.update_tbse_conso_trim(id_projet)
                if success_trim:
                    success_ht_i1 = self.update_tbse_ht_i1(id_projet)
                    if success_ht_i1:
                        success_ht_i2 = self.update_tbse_ht_i2(id_projet)
                        if success_ht_i2:
                            success_ht_t1 = self.update_tbse_ht_t1(id_projet)
                            if success_ht_t1:
                                success_ht_t2 = self.update_tbse_ht_t2(id_projet)
                                if success_ht_t2:
                                    success_ht_t1_t2_euro_jour = self.update_tbse_ht_t1_t2_euro_jour(id_projet)
                                    return (success_ln, success_exp, success_trim, success_ht_i1, 
                                            success_ht_i2, success_ht_t1, success_ht_t2, 
                                            success_ht_t1_t2_euro_jour)
                                return (success_ln, success_exp, success_trim, success_ht_i1, 
                                        success_ht_i2, success_ht_t1, success_ht_t2, False)
                            return (success_ln, success_exp, success_trim, success_ht_i1, 
                                    success_ht_i2, success_ht_t1, False, False)
                        return (success_ln, success_exp, success_trim, success_ht_i1, 
                                success_ht_i2, False, False, False)
                    return (success_ln, success_exp, success_trim, success_ht_i1, 
                            False, False, False, False)
                return (success_ln, success_exp, success_trim, False, 
                        False, False, False, False)
            return (success_ln, success_exp, False, False, 
                    False, False, False, False)
        return (False, False, False, False, 
                False, False, False, False)
    
    def __enter__(self):
        """Gestionnaire de contexte pour utiliser with"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Gestionnaire de contexte pour fermer la connexion"""
        self.disconnect()

# Exemple d'utilisation dans le main
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO)
    
    # Définition des variables avec les valeurs demandées
    elasticite_revenu_virtuel = 0.25
    elasticite_prix_marginal = -0.31
    prix_pi = 0.9
    cout_marginal_complet = 5.9  # Coût marginal complet (Cme)
    
    # Utilisation de la classe avec les paramètres
    try:
        # Création de l'instance avec les paramètres spécifiés
        surplus_db = surplusG1TBSEYAF(
            db_name='database.db', 
            table_name='surplusG1TBSE',
            elasticite_revenu_virtuel=elasticite_revenu_virtuel,
            elasticite_prix_marginal=elasticite_prix_marginal,
            prix_pi=prix_pi,
            cout_marginal_complet=cout_marginal_complet
        )
        
        # Connexion à la base
        if surplus_db.connect():
            # Mise à jour pour un id_projet spécifique
            id_projet_a_mettre_a_jour = 1  # Remplacez par l'id_projet souhaité
            
            # Première mise à jour : tbse_conso_app_ln_qb
            print("Mise à jour de tbse_conso_app_ln_qb...")
            success_ln = surplus_db.update_tbse_conso_ln(id_projet_a_mettre_a_jour)
            
            if success_ln:
                # Deuxième mise à jour : tbse_conso_app_qb_m3_jour (après la première)
                print("Mise à jour de tbse_conso_app_qb_m3_jour...")
                success_exp = surplus_db.update_tbse_conso_exp(id_projet_a_mettre_a_jour)
                
                if success_exp:
                    # Troisième mise à jour : tbse_conso_app_qb_m3_trim (après la deuxième)
                    print("Mise à jour de tbse_conso_app_qb_m3_trim...")
                    success_trim = surplus_db.update_tbse_conso_trim(id_projet_a_mettre_a_jour)
                    
                    if success_trim:
                        # Quatrième mise à jour : tbse_ht_i1 (après la troisième)
                        print("Mise à jour de tbse_ht_i1...")
                        success_ht_i1 = surplus_db.update_tbse_ht_i1(id_projet_a_mettre_a_jour)
                        
                        if success_ht_i1:
                            # Cinquième mise à jour : tbse_ht_i2 (après la quatrième)
                            print("Mise à jour de tbse_ht_i2...")
                            success_ht_i2 = surplus_db.update_tbse_ht_i2(id_projet_a_mettre_a_jour)
                            
                            if success_ht_i2:
                                # Sixième mise à jour : tbse_ht_t1 (après la cinquième)
                                print("Mise à jour de tbse_ht_t1...")
                                success_ht_t1 = surplus_db.update_tbse_ht_t1(id_projet_a_mettre_a_jour)
                                
                                if success_ht_t1:
                                    # Septième mise à jour : tbse_ht_t2 (après la sixième)
                                    print("Mise à jour de tbse_ht_t2...")
                                    success_ht_t2 = surplus_db.update_tbse_ht_t2(id_projet_a_mettre_a_jour)
                                    
                                    if success_ht_t2:
                                        # Huitième mise à jour : tbse_ht_t1_t2_euro_jour (après la septième)
                                        print("Mise à jour de tbse_ht_t1_t2_euro_jour...")
                                        success_ht_t1_t2_euro_jour = surplus_db.update_tbse_ht_t1_t2_euro_jour(id_projet_a_mettre_a_jour)
                                        
                                        if success_ht_t1_t2_euro_jour:
                                            print("Toutes les mises à jour effectuées avec succès!")
                                            print(f"Paramètres utilisés:")
                                            print(f"- Élasticité Revenu Virtuel: {elasticite_revenu_virtuel}")
                                            print(f"- Élasticité Prix Marginal: {elasticite_prix_marginal}")
                                            print(f"- Prix pi: {prix_pi}")
                                            print(f"- Coût marginal complet (Cme): {cout_marginal_complet}")
                                        else:
                                            print("La mise à jour HT_T1_T2_EURO_JOUR a échoué")
                                    else:
                                        print("La mise à jour HT_T2 a échoué")
                                else:
                                    print("La mise à jour HT_T1 a échoué")
                            else:
                                print("La mise à jour HT_I2 a échoué")
                        else:
                            print("La mise à jour HT_I1 a échoué")
                    else:
                        print("La mise à jour TRIM a échoué")
                else:
                    print("La mise à jour EXP a échoué")
            else:
                print("La mise à jour LN a échoué ou aucun enregistrement trouvé")
        
    except Exception as e:
        print(f"Erreur: {e}")
    
    finally:
        # Fermeture de la connexion
        surplus_db.disconnect()