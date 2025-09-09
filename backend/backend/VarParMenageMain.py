# main_var_par_menages.py

from VarParMenageTabCreator import VarParMenageTabCreator
from ExcelFileReloader import ExcelFileReloader
from Var_PAR_menages_NT import VarParMenageNT
from Var_PAR_menages_UAA import Var_PAR_menages_UAA
from Var_PAR_menages_ACAH import Var_PAR_menages_ACAH
from Var_PAR_menages_AIAJ import DatabaseManager
from Var_PAR_menages_ALAM import Var_PAR_menages_ALAM


class VarParMenageMain:
    def __init__(self):

        db_path = "database.db"                    # ta base SQLite
        excel_path = "Var_PAR_menages_NT.xls"  # ton fichier Excel

        self.tab_creator = VarParMenageTabCreator()
        self.excel_reloader = ExcelFileReloader()

        # Initialisation des variables spécifiques
        self.nt = VarParMenageNT(db_path, excel_path)
        self.uaa =Var_PAR_menages_UAA()
        self.acah = Var_PAR_menages_ACAH()
        self.aiaj =DatabaseManager()
        self.alam = Var_PAR_menages_ALAM(database="database.db",
        table_name="VarParMenageResult",
        id_projet=1)

    def run(self, projet_id):

        ##############################NT############################
        print("=== Démarrage du traitement des ménages ===")

        try:
            

            # Lecture du fichier Excel
            self.nt.read_excel()

            # Sauvegarde brute dans une table temporaire
            self.nt.save_to_db("VarParMenageExcel")

            # Mise à jour de la table des résultats
            self.nt.update_results_in_db("VarParMenageResult")

        except Exception as e:
            print(f"Erreur globale : {e}")


        ###############################UAA###########################

         
    
        # Exemple 2: Lecture du fichier Excel Var_PAR_menages_UAA.xls (première feuille automatiquement)
        print("\nExemple 2: Lecture du fichier Var_PAR_menages_UAA.xls (feuille 1 automatique)")
        try:
            file_path = "Var_PAR_menages_UAA.xls"
            df_excel =  self.uaa .read_excel_file(file_path)
            print(f"DataFrame lu depuis {file_path} (feuille 1):")
            print(df_excel.head())
            print(f"\nNombre de lignes: {len(df_excel)}")
            
        except FileNotFoundError:
            print(f"Fichier '{file_path}' non trouvé. Veuillez vérifier le chemin.")
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
        
        # Exemple 6: Mise à jour de la table VarParMenageResult
        print("\nExemple 6: Mise à jour de la table VarParMenageResult")
        self.uaa .update_varparmenageresult_table(df_excel)

        ##################################################################################################

    
        # ID du projet à mettre à jour (à adapter selon vos besoins)

        # Méthode 1: Utilisation avec gestion manuelle de la connexion
        try:
            self.acah.connect()
            success = self.acah.update_sepa_columns(projet_id)
            if success:
                print("Opération terminée avec succès")
            else:
                print("L'opération a échoué")
        finally:
            self.acah.disconnect()


        ##################################################################################################


    
        try:
            # Vérification des données existantes
            print("=== VÉRIFICATION DES DONNÉES EXISTANTES ===")
            self.aiaj.check_existing_data("VarParMenageResult", 10)
            
            # Si la table n'existe pas, la créer et insérer des données de test
            # Décommentez les lignes suivantes si vous voulez créer la table et insérer des données de test
            # db_manager.create_table_if_not_exists("VarParMenageResult")
            # db_manager.insert_sample_data("VarParMenageResult")
            
            # Mise à jour d'un projet spécifique (exemple avec projet ID 1)
            print("\n=== MISE À JOUR PROJET SPÉCIFIQUE (ID 1) ===")
            rows_affected = self.aiaj.update_par_columns(1, "VarParMenageResult")

        except Exception as e:
            print(f"Erreur dans le main: {e}")
    
        finally:
            # Fermeture propre de la connexion
            self.aiaj.disconnect()

        #print("NT :", self.nt.compute()) OK
        #print("UAA :", self.uaa.compute())
        #print("ACAH :", self.acah.compute())
        #print("AIAJ :", self.aiaj.compute())
        #print("ALAM :", self.alam.compute())


        print("=== Fin du traitement ===")


if __name__ == "__main__":
    main = VarParMenageMain()
    main.run()
