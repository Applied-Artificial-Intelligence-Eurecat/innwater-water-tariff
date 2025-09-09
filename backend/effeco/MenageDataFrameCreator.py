import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3
import sys

class MenageDataFrameCreator:
    """
    Classe pour lire des DataFrames Excel et les stocker en SQLite
    """
    
    def __init__(self, db_name='database.db'):
        # Ajout de 'id_projet' au début du schéma
        self.schema = [
            'id_projet', 'menage', 'assaini', 'revenu_net_mois', 'c_m3_trim_1', 'c_m3_trim_2',
            'c_ibt', 'c_ibt_pp', 'c_tbse', 'consom_nordin_trim', 'consom_taylor_trim',
            'c_captive_jour', 'c_nordin_jour', 'c_taylor_jour', 'ln_c_captive_jour',
            'ln_c_nordin_jour', 'ln_c_taylor_jour', 'sur_consommation_pct'
        ]
        
        self.db_name = db_name
        self.table_name = 'menage_data'
        
        # Mapping des noms de colonnes Excel (inchangé)
        self.excel_mapping = {
            'Ménage': 'menage',
            'Assaini': 'assaini',
            'Revenu net mois': 'revenu_net_mois',
            'C_m3 / trim': 'c_m3_trim_1',
            'C_m3 / trim.1': 'c_m3_trim_2',
            'C_IBT': 'c_ibt',
            'C_IBT_PP': 'c_ibt_pp',
            'C_TBSE': 'c_tbse',
            'Consom Nordin Trim': 'consom_nordin_trim',
            'Consom Taylor Trim': 'consom_taylor_trim',
            'C_Captive_Jour': 'c_captive_jour',
            'C_Nordin_Jour': 'c_nordin_jour',
            'C_Taylor_Jour': 'c_taylor_jour',
            'ln C Captive Jour': 'ln_c_captive_jour',
            'ln C Nordin Jour': 'ln_c_nordin_jour',
            'ln C Taylor J': 'ln_c_taylor_jour',
            'Sur-consommation en %': 'sur_consommation_pct'
        }
    
    def read_excel_file(self, file_path, sheet_name=0, id_projet=1):
        """
        Lit un fichier Excel et le transforme selon le schéma standard
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            sheet_name (str/int): Nom ou index de la feuille à lire
            id_projet (int): Identifiant du projet (défaut: 1)
            
        Returns:
            pandas.DataFrame: DataFrame formaté
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
        # Lecture du fichier Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Renommage des colonnes selon le mapping
        df = df.rename(columns=self.excel_mapping)
        
        # Ajout de la colonne id_projet avec la valeur par défaut
        df['id_projet'] = id_projet
        
        # Ajout des colonnes manquantes si nécessaire
        missing_columns = set(self.schema) - set(df.columns)
        for col in missing_columns:
            df[col] = np.nan
        
        # Réorganisation des colonnes selon le schéma
        available_columns = [col for col in self.schema if col in df.columns]
        df = df[available_columns]
        
        # Conversion des types de données
        df = self._convert_data_types(df)
        
        print(f"Fichier Excel lu: {df.shape[0]} lignes, {df.shape[1]} colonnes")
        print(f"ID projet assigné: {id_projet}")
        return df
    
    def _convert_data_types(self, df):
        """
        Convertit les types de données pour assurer la cohérence
        """
        type_conversions = {
            'id_projet': 'int64',  # Ajout du type pour id_projet
            'menage': 'int64',
            'assaini': 'int64',
            'revenu_net_mois': 'float64',
            'c_m3_trim_1': 'float64',
            'c_m3_trim_2': 'float64',
            'c_ibt': 'float64',
            'c_ibt_pp': 'float64',
            'c_tbse': 'float64',
            'consom_nordin_trim': 'float64',
            'consom_taylor_trim': 'float64',
            'c_captive_jour': 'float64',
            'c_nordin_jour': 'float64',
            'c_taylor_jour': 'float64',
            'ln_c_captive_jour': 'float64',
            'ln_c_nordin_jour': 'float64',
            'ln_c_taylor_jour': 'float64',
            'sur_consommation_pct': 'float64'
        }
        
        for col, dtype in type_conversions.items():
            if col in df.columns:
                if col == 'id_projet':
                    # Pour id_projet, on s'assure que c'est un entier
                    df[col] = df[col].astype(dtype)
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)
        
        return df
    
    def create_sqlite_table(self, df, if_exists='replace'):
        """
        Crée une table SQLite et insère les données du DataFrame
        
        Args:
            df (pandas.DataFrame): DataFrame à stocker
            if_exists (str): 'replace' supprime la table si elle existe
        """
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_name)
        
        # Suppression de la table si elle existe et si demandé
        if if_exists == 'replace':
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            conn.commit()
            print(f"Table existante supprimée: {self.table_name}")
        
        # Création de la table et insertion des données
        df.to_sql(
            name=self.table_name,
            con=conn,
            if_exists=if_exists,
            index=False
        )
        
        # Vérification du nombre de lignes insérées
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        row_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"Table créée: {self.table_name}")
        print(f"Lignes insérées: {row_count}")
        print(f"Base de données: {self.db_name}")

def main():
    """
    Fonction principale simplifiée
    """
    # Création de l'instance
    creator = MenageDataFrameCreator('database.db')
    
    # Chemin vers le fichier Excel
    excel_file_path = "surplusG1.xls"
    
    try:
        # 1. Lecture du fichier Excel avec id_projet par défaut = 1
        print("1. Lecture du fichier Excel...")
        df = creator.read_excel_file(excel_file_path, id_projet=1)
        
        # 2. Construction du DataFrame (déjà fait dans read_excel_file)
        print("2. DataFrame construit avec succès")
        
        # 3. Insertion dans la table SQLite
        print("3. Insertion dans la base de données...")
        creator.create_sqlite_table(df, if_exists='replace')
        
        print("\n✅ Opération terminée avec succès!")
        return df
        
    except FileNotFoundError:
        print(f"\n❌ Erreur: Le fichier '{excel_file_path}' n'existe pas")
        print("Veuillez placer le fichier Excel dans le même dossier que ce script")
        return None
        
    except Exception as e:
        print(f"\n❌ Erreur lors du traitement: {e}")
        return None

if __name__ == "__main__":
    # Exécution simple et directe
    dataframe = main()
    
    if dataframe is not None:
        print(f"\nRésumé:")
        print(f"- Fichier traité: surplusG1.xls")
        print(f"- Lignes importées: {len(dataframe)}")
        print(f"- Colonnes: {len(dataframe.columns)}")
        print(f"- Base de données créée: database.db")
        print(f"- Table créée: menage_data")
        print(f"- ID projet par défaut: {dataframe['id_projet'].iloc[0] if len(dataframe) > 0 else 'N/A'}")
    else:
        print("\n❌ L'opération a échoué")
        sys.exit(1)