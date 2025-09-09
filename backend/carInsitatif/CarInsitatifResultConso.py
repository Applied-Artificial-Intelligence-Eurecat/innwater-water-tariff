import sqlite3
import logging

class CarInsitatifResultConso:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Établit une connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connexion à la base de données {self.db_name} établie avec succès")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.logger.info("Connexion à la base de données fermée")
    
    def create_table(self):
        """Crée la table CarInsitatifResultConso avec la structure spécifiée"""
        try:
            # Définition de la requête SQL pour créer la table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS CarInsitatifResultConso (
                id_projet INTEGER,
                Type_indicateur TEXT,
                indicateur TEXT,
                t1_c_ab_ibt REAL,
                t1_c_ab_ibt_pp REAL,
                t1_c_ab_tbse REAL,
                t1_c_ab_surconso_effective REAL,
                t1_c_ab_surconso_par_tete REAL,
                t2_g1_ep_ibt REAL,
                t2_g1_ep_ibt_pp REAL,
                t2_g1_ep_tbse REAL,
                t2_g1_ep_surconso_effective REAL,
                t2_g1_ep_surconso_par_tete REAL,
                t3_g2_epa_ibt REAL,
                t3_g2_epa_ibt_pp REAL,
                t3_g2_epa_tbse REAL,
                t3_g2_epa_surconso_effective REAL,
                t3_g2_epa_surconso_par_tete REAL,
                t4_poor_ibt REAL,
                t4_poor_ibt_pp REAL,
                t4_poor_tbse REAL,
                t4_poor_surconso_eff REAL,
                t4_poor_surconso_tete REAL,
                t5_not_poor_ibt REAL,
                t5_not_poor_ibt_pp REAL,
                t5_not_poor_tbse REAL,
                t5_not_poor_surconso_eff REAL,
                t5_not_poor_surconso_tete REAL,
                t6_g1_poor_ibt REAL,
                t6_g1_poor_ibt_pp REAL,
                t6_g1_poor_tbse REAL,
                t6_g1_poor_surconso_eff REAL,
                t6_g1_poor_surconso_tete REAL,
                t7_g1_ep_non_poor_ibt REAL,
                t7_g1_ep_non_poor_ibt_pp REAL,
                t7_g1_ep_non_poor_tbse REAL,
                t7_g1_ep_non_poor_surconso_eff REAL,
                t7_g1_ep_non_poor_surconso_tete REAL,
                t8_g2_epa_poor_ibt REAL,
                t8_g2_epa_poor_ibt_pp REAL,
                t8_g2_epa_poor_tbse REAL,
                t8_g2_epa_poor_surconso_effective REAL,
                t8_g2_epa_poor_surconso_par_tete REAL,
                t9_g2_epa_non_poor_ibt REAL,
                t9_g2_epa_non_poor_ibt_pp REAL,
                t9_g2_epa_non_poor_tbse REAL,
                t9_g2_epa_non_poor_surconso_effective REAL,
                t9_g2_epa_non_poor_surconso_par_tete REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id_projet, Type_indicateur, indicateur)
            )
            """
            
            # Exécution de la requête
            self.cursor.execute(create_table_query)
            self.connection.commit()
            
            self.logger.info("Table 'CarInsitatifResultConso' créée avec succès")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la création de la table: {e}")
            return False
    
    def initialize_database(self):
        """Initialise la base de données en créant la table"""
        if self.connect():
            success = self.create_table()
            self.disconnect()
            return success
        return False

    def insert_data(self, data_dict):
        """Insère des données dans la table CarInsitatifResultConso"""
        try:
            if not self.connect():
                return False
            
            # Préparation des colonnes et valeurs
            columns = []
            placeholders = []
            values = []
            
            for key, value in data_dict.items():
                columns.append(key)
                placeholders.append("?")
                # Conversion des nombres avec virgule en format float
                if isinstance(value, str) and ',' in value:
                    try:
                        value = float(value.replace(',', '.'))
                    except ValueError:
                        pass
                values.append(value)
            
            # Construction de la requête SQL
            query = f"""
            INSERT OR REPLACE INTO CarInsitatifResultConso ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            """
            
            # Exécution de la requête
            self.cursor.execute(query, values)
            self.connection.commit()
            
            self.logger.info("Données insérées avec succès dans CarInsitatifResultConso")
            self.disconnect()
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'insertion des données: {e}")
            self.disconnect()
            return False

    def get_data(self, id_projet=None, Type_indicateur=None, indicateur=None):
        """Récupère des données de la table avec des filtres optionnels"""
        try:
            if not self.connect():
                return None
            
            query = "SELECT * FROM CarInsitatifResultConso WHERE 1=1"
            params = []
            
            if id_projet is not None:
                query += " AND id_projet = ?"
                params.append(id_projet)
            
            if Type_indicateur is not None:
                query += " AND Type_indicateur = ?"
                params.append(Type_indicateur)
            
            if indicateur is not None:
                query += " AND indicateur = ?"
                params.append(indicateur)
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
            self.disconnect()
            return results
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la récupération des données: {e}")
            self.disconnect()
            return None

    def get_all_data(self):
        """Récupère toutes les données de la table"""
        try:
            if not self.connect():
                return None
            
            self.cursor.execute("SELECT * FROM CarInsitatifResultConso")
            results = self.cursor.fetchall()
            
            self.disconnect()
            return results
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la récupération des données: {e}")
            self.disconnect()
            return None

    def delete_data(self, id_projet, Type_indicateur, indicateur):
        """Supprime des données spécifiques de la table"""
        try:
            if not self.connect():
                return False
            
            query = """
            DELETE FROM CarInsitatifResultConso 
            WHERE id_projet = ? AND Type_indicateur = ? AND indicateur = ?
            """
            
            self.cursor.execute(query, (id_projet, Type_indicateur, indicateur))
            self.connection.commit()
            
            self.logger.info("Données supprimées avec succès")
            self.disconnect()
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de la suppression des données: {e}")
            self.disconnect()
            return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une instance de la classe
    car_initiative = CarInsitatifResultConso()
    
    # Initialisation de la base de données et création de la table
    if car_initiative.initialize_database():
        print("Base de données initialisée avec succès!")
        
        # Exemple d'insertion de données basé sur l'exemple fourni
        sample_data = {
            'id_projet': 1,
            'Type_indicateur': 'consommation',
            'indicateur': 'Moyenne',
            't1_c_ab_ibt': 36.536,
            't1_c_ab_ibt_pp': 34.140,
            't1_c_ab_tbse': 47.471,
            't1_c_ab_surconso_effective': 2.434,
            't1_c_ab_surconso_par_tete': 0.871,
            't2_g1_ep_ibt': 40.134,
            't2_g1_ep_ibt_pp': 37.226,
            't2_g1_ep_tbse': 50.595,
            't2_g1_ep_surconso_effective': 2.920,
            't2_g1_ep_surconso_par_tete': 1.047,
            't3_g2_epa_ibt': 32.287,
            't3_g2_epa_ibt_pp': 30.495,
            't3_g2_epa_tbse': 43.782,
            't3_g2_epa_surconso_effective': 1.845,
            't3_g2_epa_surconso_par_tete': 0.659,
            't4_poor_ibt': 33.217,
            't4_poor_ibt_pp': 31.009,
            't4_poor_tbse': 42.598,
            't4_poor_surconso_eff': 2.249,
            't4_poor_surconso_tete': 0.697,
            't5_not_poor_ibt': 39.499,
            't5_not_poor_ibt_pp': 36.934,
            't5_not_poor_tbse': 51.820,
            't5_not_poor_surconso_eff': 2.597,
            't5_not_poor_surconso_tete': 1.026,
            't6_g1_poor_ibt': 37.222,
            't6_g1_poor_ibt_pp': 34.462,
            't6_g1_poor_tbse': 46.361,
            't6_g1_poor_surconso_eff': 3.027,
            't6_g1_poor_surconso_tete': 0.823,
            't7_g1_ep_non_poor_ibt': 42.494,
            't7_g1_ep_non_poor_ibt_pp': 39.466,
            't7_g1_ep_non_poor_tbse': 54.025,
            't7_g1_ep_non_poor_surconso_eff': 3.027,
            't7_g1_ep_non_poor_surconso_tete': 1.227,
            't8_g2_epa_poor_ibt': 28.982,
            't8_g2_epa_poor_ibt_pp': 27.359,
            't8_g2_epa_poor_tbse': 38.619,
            't8_g2_epa_poor_surconso_effective': 1.671,
            't8_g2_epa_poor_surconso_par_tete': 0.560,
            't9_g2_epa_non_poor_ibt': 35.593,
            't9_g2_epa_non_poor_ibt_pp': 33.631,
            't9_g2_epa_non_poor_tbse': 48.944,
            't9_g2_epa_non_poor_surconso_effective': 2.019,
            't9_g2_epa_non_poor_surconso_par_tete': 0.757
        }
        
        if car_initiative.insert_data(sample_data):
            print("Données insérées avec succès dans CarInsitatifResultConso!")
            
            # Récupération des données pour vérification
            results = car_initiative.get_data(id_projet=1, Type_indicateur='consommation')
            if results:
                print(f"{len(results)} enregistrement(s) trouvé(s) dans CarInsitatifResultConso")
                
            # Récupération de toutes les données
            all_data = car_initiative.get_all_data()
            if all_data:
                print(f"Total des enregistrements: {len(all_data)}")
        else:
            print("Erreur lors de l'insertion des données")
    else:
        print("Erreur lors de l'initialisation de la base de données")