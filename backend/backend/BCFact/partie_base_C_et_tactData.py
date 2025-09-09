import pandas as pd
import numpy as np
from BC_Fact_service import BC_Fact_service

class VexpDataFrameBuilder:
    """
    Classe pour construire un DataFrame avec les colonnes spécifiées pour vexp_cc
    à partir du fichier Excel partie_base_C_et_tact.xls
    """
    
    # Définition des colonnes attendues (avec espaces comme dans Excel)
    COLUMNS_EXCEL = [
        'vexp_cc men',
        'vexp_cc ass', 
        'vexp_cc const',
        'vexp_cc tfam',
        'vexp_cc snwa',
        'vexp_cc swim',
        'vexp_cc gwt'
    ]
    
    # Définition des colonnes pour SQLite (avec underscores)
    COLUMNS_SQL = [
        'vexp_cc_men',
        'vexp_cc_ass', 
        'vexp_cc_const',
        'vexp_cc_tfam',
        'vexp_cc_snwa',
        'vexp_cc_swim',
        'vexp_cc_gwt'
    ]
    
    def __init__(self, fichier_excel="partie_base_C_et_tact.xls"):
        self.fichier_excel = fichier_excel
        self.df_original = None
    
    def charger_excel(self, feuille=0):
        try:
            self.df_original = pd.read_excel(self.fichier_excel, sheet_name=feuille)
            print(f"Fichier Excel chargé avec succès. Shape: {self.df_original.shape}")
            return self.df_original
        except Exception as e:
            print(f"Erreur lors du chargement du fichier Excel: {e}")
            return None
    
    def construire_dataframe_cible(self):
        """
        Construit un DataFrame avec la structure de colonnes demandée
        et convertit les noms de colonnes pour SQLite
        """
        if self.df_original is None:
            print("Veuillez d'abord charger le fichier Excel avec charger_excel()")
            return None
        
        df_cible = pd.DataFrame()
        
        # Mapping des noms de colonnes Excel -> SQL
        colonne_mapping = {}
        for excel_col, sql_col in zip(self.COLUMNS_EXCEL, self.COLUMNS_SQL):
            colonne_mapping[excel_col] = sql_col
            
            if excel_col in self.df_original.columns:
                df_cible[sql_col] = self.df_original[excel_col]
            else:
                print(f"Attention: Colonne '{excel_col}' non trouvée dans le fichier Excel")
                df_cible[sql_col] = np.nan
        
        return df_cible
    
    def get_colonnes_disponibles(self):
        if self.df_original is None:
            print("Veuillez d'abord charger le fichier Excel")
            return []
        return list(self.df_original.columns)
    
    def analyser_structure(self):
        if self.df_original is None:
            print("Veuillez d'abord charger le fichier Excel")
            return
        
        print("=== ANALYSE DU FICHIER EXCEL ===")
        print(f"Shape: {self.df_original.shape}")
        print(f"Colonnes totales: {len(self.df_original.columns)}")
        print()
        
        print("Colonnes demandées vs Disponibles:")
        for colonne in self.COLUMNS_EXCEL:
            disponible = "✓" if colonne in self.df_original.columns else "✗"
            print(f"{disponible} {colonne}")
    
    def inserer_dans_base(self, db_path="database.db", table_name="partie_base_c_et_fact_table"):
        """
        Construit le DataFrame et l'insère dans la base de données SQLite
        après conversion des noms de colonnes
        """
        if self.df_original is None:
            print("Veuillez d'abord charger le fichier Excel")
            return False
        
        try:
            # Construire le DataFrame cible avec les bons noms de colonnes
            df_cible = self.construire_dataframe_cible()
            
            if df_cible.empty:
                print("Le DataFrame cible est vide")
                return False
            
            print("\n=== DATAFRAME POUR SQLITE ===")
            print(f"Shape: {df_cible.shape}")
            print("Colonnes SQL:", list(df_cible.columns))
            print("\nAperçu des données:")
            print(df_cible.head())
            
            # Créer une instance du service
            service = BC_Fact_service(db_path, table_name)
            
            # Insérer le DataFrame dans la base
            service.insert_dataframe(df_cible)
            
            print(f"✅ Insertion réussie : {len(df_cible)} lignes insérées")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion dans la base : {e}")
            return False

def main():
    # Créer une instance du builder avec votre fichier Excel
    builder = VexpDataFrameBuilder("partie_base_C_et_tact.xls")
    
    # Charger le fichier Excel
    df_original = builder.charger_excel()
    
    if df_original is not None:
        # Analyser la structure du fichier
        builder.analyser_structure()
        
        # Insérer le DataFrame dans la base de données
        print("\n=== INSERTION DANS LA BASE DE DONNÉES ===")
        success = builder.inserer_dans_base()
        
        if success:
            print("✅ Processus terminé avec succès")
        else:
            print("❌ Échec du processus")

if __name__ == "__main__":
    main()