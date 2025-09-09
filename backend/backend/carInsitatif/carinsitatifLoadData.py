import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from CarInsitatifSvrInsert import CarInsitatifSvrInsert

class ExcelDataReader:
    def __init__(self):
        self.data = None
        self.file_path = None
        
    def read_excel_file(self, file_path: str, sheet_name: str = 0) -> Optional[pd.DataFrame]:
        """
        Lit un fichier Excel avec la structure spécifiée
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            sheet_name (str): Nom ou index de la feuille à lire (défaut: 0)
            
        Returns:
            pd.DataFrame: DataFrame contenant les données ou None en cas d'erreur
        """
        try:
            # Lecture du fichier Excel
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            self.file_path = file_path
            
            # Vérification des colonnes attendues
            expected_columns = [
                'id_projet', 'household_id', 'is_connected_sewage', 'is_poor_household',
                'household_size', 'household_income', 'water_consumption_tbse',
                'water_consumption_ibt_pp', 'water_consumption_ibt', 'overconsumption_volume',
                'is_overconsuming', 'overconsumption_per_capita', 'bill_amount_ibt',
                'bill_amount_ibt_pp', 'bill_amount_tbse', 'overconsumption_expenditure',
                'per_capita'
            ]
            
            # Vérification que toutes les colonnes attendues sont présentes
            missing_columns = set(expected_columns) - set(self.data.columns)
            if missing_columns:
                print(f"Avertissement : Colonnes manquantes : {missing_columns}")
            
            # Conversion des types de données appropriés
            self._convert_data_types()
            
            print(f"Fichier '{file_path}' lu avec succès")
            print(f"Nombre de lignes : {len(self.data)}")
            print(f"Colonnes disponibles : {list(self.data.columns)}")
            
            return self.data
            
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{file_path}' n'a pas été trouvé")
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {str(e)}")
            return None
    
    def _convert_data_types(self) -> None:
        """Convertit les types de données pour optimiser la mémoire et le traitement"""
        if self.data is not None:
            # Colonnes booléennes
            bool_columns = ['is_connected_sewage', 'is_poor_household', 'is_overconsuming']
            for col in bool_columns:
                if col in self.data.columns:
                    self.data[col] = self.data[col].astype('bool')
            
            # Colonnes entières
            int_columns = ['id_projet', 'household_id', 'household_size']
            for col in int_columns:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')
            
            # Colonnes numériques (flottantes)
            numeric_columns = [
                'household_income', 'water_consumption_tbse', 'water_consumption_ibt_pp',
                'water_consumption_ibt', 'overconsumption_volume', 'overconsumption_per_capita',
                'bill_amount_ibt', 'bill_amount_ibt_pp', 'bill_amount_tbse',
                'overconsumption_expenditure', 'per_capita'
            ]
            for col in numeric_columns:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('float64')
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Retourne un résumé statistique des données
        
        Returns:
            Dict: Dictionnaire contenant les statistiques descriptives
        """
        if self.data is None:
            print("Aucune donnée chargée")
            return {}
        
        summary = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'numeric_stats': self.data.describe().to_dict() if not self.data.empty else {}
        }
        
        return summary
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Retourne les données chargées
        
        Returns:
            pd.DataFrame: Les données ou None si aucune donnée n'est chargée
        """
        return self.data
    
    def save_processed_data(self, output_path: str) -> None:
        """
        Sauvegarde les données traitées dans un nouveau fichier Excel
        
        Args:
            output_path (str): Chemin de sortie pour le fichier
        """
        if self.data is not None:
            try:
                self.data.to_excel(output_path, index=False)
                print(f"Données sauvegardées dans : {output_path}")
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {str(e)}")
        else:
            print("Aucune donnée à sauvegarder")

# Exemple d'utilisation
if __name__ == "__main__":
    # Création de l'instance
    # Initialisation
    reader = ExcelDataReader()

    # Lecture du fichier (assurez-vous qu'il est dans le même dossier ou donnez le chemin complet)
    data = reader.read_excel_file("dataintermed.xls")

    # Ou avec chemin complet
    # data = reader.read_excel_file("C:/chemin/complet/vers/dataintermed.xls")
    db_insert = CarInsitatifSvrInsert("database.db")
    
    # Afficher les informations de la table
    db_insert.get_table_info()
    
    # Création d'un DataFrame d'exemple conforme au schéma
   
    
    df = pd.DataFrame(data)
    
    # Insertion du DataFrame
    inserted_ids = db_insert.insert_dataframe(df, batch_size=100)
    print(f"IDs des enregistrements insérés: {inserted_ids}")