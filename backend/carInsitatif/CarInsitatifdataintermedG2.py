import sqlite3
from typing import Optional, Dict, Any, List

class CarInsitatifdataintermedG2:
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.connection = None
    
    def connect(self) -> None:
        """Établit la connexion à la base de données"""
        self.connection = sqlite3.connect(self.db_name)
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def drop_table_if_exists(self) -> bool:
        """Supprime la table si elle existe déjà"""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS CarInsitatifdataintermedG2")
            self.connection.commit()
            print("✅ Table supprimée si elle existait")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la suppression de la table: {e}")
            return False
        finally:
            self.disconnect()
    
    def create_table(self) -> bool:
        """Crée la table avec la structure spécifiée"""
        # D'abord supprimer la table si elle existe
        self.drop_table_if_exists()
        
        create_table_query = """
        CREATE TABLE CarInsitatifdataintermedG2 (
            id_projet INTEGER,
            household_id INTEGER,
            is_connected_sewage INTEGER,
            is_poor_household INTEGER,
            household_size INTEGER,
            household_income REAL,
            water_consumption_tbse REAL,
            water_consumption_ibt_pp REAL,
            water_consumption_ibt REAL,
            overconsumption_volume REAL,
            is_overconsuming INTEGER,
            overconsumption_per_capita REAL,
            bill_amount_ibt REAL,
            bill_amount_ibt_pp REAL,
            bill_amount_tbse REAL,
            overconsumption_expenditure REAL,
            per_capita REAL
        )
        """
        
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("✅ Table 'CarInsitatifdataintermedG2' créée avec succès!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la création de la table: {e}")
            return False
        
        finally:
            self.disconnect()
    
    def insert_data(self, data: Dict[str, Any]) -> Optional[int]:
        """Insère des données dans la table"""
        insert_query = """
        INSERT INTO CarInsitatifdataintermedG2 (
            id_projet, household_id, is_connected_sewage, is_poor_household, 
            household_size, household_income, water_consumption_tbse,
            water_consumption_ibt_pp, water_consumption_ibt, overconsumption_volume,
            is_overconsuming, overconsumption_per_capita, bill_amount_ibt,
            bill_amount_ibt_pp, bill_amount_tbse, overconsumption_expenditure, per_capita
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (
                data.get('id_projet'),
                data['household_id'],
                data['is_connected_sewage'],
                data['is_poor_household'],
                data['household_size'],
                data['household_income'],
                data['water_consumption_tbse'],
                data['water_consumption_ibt_pp'],
                data['water_consumption_ibt'],
                data['overconsumption_volume'],
                data['is_overconsuming'],
                data['overconsumption_per_capita'],
                data['bill_amount_ibt'],
                data['bill_amount_ibt_pp'],
                data['bill_amount_tbse'],
                data['overconsumption_expenditure'],
                data['per_capita']
            ))
            self.connection.commit()
            inserted_id = cursor.lastrowid
            print(f"✅ Données insérées avec l'ID de ligne: {inserted_id}")
            return inserted_id
            
        except sqlite3.IntegrityError as e:
            print(f"❌ Erreur d'intégrité (doublon ou contrainte violée): {e}")
            return None
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de l'insertion: {e}")
            return None
        finally:
            self.disconnect()
    
    def insert_sample_data(self) -> None:
        """Insère les données d'exemple"""
        sample_data = [
            {
                'id_projet': 1,
                'household_id': 1,
                'is_connected_sewage': 0,
                'is_poor_household': 1,
                'household_size': 4,
                'household_income': 226.88,
                'water_consumption_tbse': 24.073,
                'water_consumption_ibt_pp': 19.994,
                'water_consumption_ibt': 21.539,
                'overconsumption_volume': 1.545,
                'is_overconsuming': 1,
                'overconsumption_per_capita': 0.386,
                'bill_amount_ibt': 47.45,
                'bill_amount_ibt_pp': 44.36,
                'bill_amount_tbse': 73.08,
                'overconsumption_expenditure': 3.09,
                'per_capita': 0.77
            },
            {
                'id_projet': 2,
                'household_id': 2,
                'is_connected_sewage': 0,
                'is_poor_household': 1,
                'household_size': 4,
                'household_income': 840.21,
                'water_consumption_tbse': 34.543,
                'water_consumption_ibt_pp': 28.340,
                'water_consumption_ibt': 29.846,
                'overconsumption_volume': 1.506,
                'is_overconsuming': 1,
                'overconsumption_per_capita': 0.376,
                'bill_amount_ibt': 64.06,
                'bill_amount_ibt_pp': 61.05,
                'bill_amount_tbse': 83.99,
                'overconsumption_expenditure': 3.01,
                'per_capita': 0.75
            }
        ]
        
        success_count = 0
        for data in sample_data:
            if self.insert_data(data) is not None:
                success_count += 1
        
        print(f"📊 {success_count}/{len(sample_data)} enregistrements insérés avec succès")
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """Récupère toutes les données de la table"""
        select_query = "SELECT * FROM CarInsitatifdataintermedG2 ORDER BY household_id"
        
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            rows = cursor.fetchall()
            
            # Récupérer les noms des colonnes
            columns = [description[0] for description in cursor.description]
            
            # Convertir en liste de dictionnaires
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            
            return result
            
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des données: {e}")
            return []
        finally:
            self.disconnect()
    
    def display_table_info(self) -> None:
        """Affiche des informations sur la table et son contenu"""
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Compter le nombre d'enregistrements
            cursor.execute("SELECT COUNT(*) FROM CarInsitatifdataintermedG2")
            count = cursor.fetchone()[0]
            
            print(f"\n📋 Informations de la table 'CarInsitatifdataintermedG2':")
            print(f"   Nombre d'enregistrements: {count}")
            
            if count > 0:
                # Afficher les colonnes disponibles
                cursor.execute("PRAGMA table_info(CarInsitatifdataintermedG2)")
                columns_info = cursor.fetchall()
                print(f"\n📝 Structure de la table:")
                for col in columns_info:
                    print(f"   - {col[1]} ({col[2]})")
                
                # Afficher les premières lignes
                cursor.execute("SELECT * FROM CarInsitatifdataintermedG2 LIMIT 3")
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                print(f"\n🔍 Premiers enregistrements:")
                print("   " + " | ".join(columns[:5]) + " | ...")
                for row in rows:
                    print("   " + " | ".join(str(x) for x in row[:5]) + " | ...")
            
        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des informations: {e}")
        finally:
            self.disconnect()
    
    def clear_table(self) -> bool:
        """Vide la table de toutes ses données"""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM CarInsitatifdataintermedG2")
            self.connection.commit()
            print("✅ Table vidée avec succès!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erreur lors du vidage de la table: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """Fonction principale pour tester la classe"""
    print("🚀 Initialisation de la base de données...")
    
    # Créer une instance de la classe
    db = CarInsitatifdataintermedG2()
    
    # Créer la table
    if not db.create_table():
        print("❌ Échec de la création de la table")
        return

if __name__ == "__main__":
    main()