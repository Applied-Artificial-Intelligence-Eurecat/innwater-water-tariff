import sqlite3
import traceback
import pandas as pd 
from typing import List, Dict, Any, Optional
from commonAbSrvCreate import c_Ab_srvCreate
from CommonTBSETable import CommonTBSETable
from comonNordinCreateSrv import comonNordinCreateSrv
from comonTarifTableCreateSrv import comonTarifTableCreateSrv
from ComonTvaRedevance import ComonTvaRedevance
from comonTvaRedTBSECreateSrv import comonTvaRedTBSECreateSrv
from CommoAbsrvinsert import CommoAbsrvinsert
from commonAbDataframe import CommonAbDataframe
from CommonTarifTBSE import CommonTarifTBSEModel
from comonNordinInsertSrv import comonNordinInsert
from ComonTarifTableInsertSrv import ComonTarifTableInsert
from CommonTarifTBSESrv import CommonTarifTBSESrv
from ComonTvaRedevanceInsertSrv import ComonTavaRedevanceInsertSrv
from ComonTvaRedTBSEInsertSrv import ComonTvaRedTBSEInsertSrv


# Importez vos classes existantes ici
# from your_module import c_Ab_srvCreate, CommonTBSETable, comonNordinCreateSrv, etc.

class DatabaseInsertParameter:
    """
    Gestionnaire centralisé pour l'instanciation et la création de toutes les tables.
    Gère les différents patterns utilisés dans vos classes.
    """
    
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.results = {}
        self.errors = {}
        



def main():
    """Fonction principale avec exemples d'utilisation."""
    
    # Création du gestionnaire
    manager = DatabaseInsertParameter("database.db")
    
    print("🗂️  GESTIONNAIRE DE TABLES DE BASE DE DONNÉES")
    print("=" * 50)
    
    # Abonnment 
    
    projet_df = CommonAbDataframe()
    df = projet_df.create_dataframe()
    print("✅ DataFrame généré :")
    print(df)

        # Insérer dans la base
    inserter = CommoAbsrvinsert("database.db")
    inserter.insert_dataframe(df)
    inserter.close()
    print("✅ Insertion terminée dans la table 'commonAb'")

 

    # TBSE TARIF

     # Créer le DataFrame avec les données par défaut et id_projet = 1
    df_tarifs = CommonTarifTBSEModel.create_default_dataframe(id_projet_default=1)
    print("2. DataFrame avec données par défaut et id_projet = 1 :")
    print(df_tarifs)
    print()
    
    service = CommonTarifTBSESrv("database.db")
    try:
        # Persister le DataFrame par défaut avec id_projet = 1
        inserted_ids = service.persist_default_dataframe(id_projet_default=1)
        print(f"Tarifs insérés avec les IDs : {inserted_ids}")
    except sqlite3.OperationalError as e:
        print(f"Erreur de base de données : {e}")
        print("Vérifiez que la table CommonTarifTBSEModel existe dans database.db")
    except Exception as e:
        print(f"Erreur générale : {e}")

    #Nordin

    data = {
        "id_projet": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "type_nordin": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP", "EP"],
        "num_tranche": ["T1", "T2", "T3", "T1", "T2", "T3", "T4", "T1", "T2", "T3", "T4"],
        "d_nordin_op": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
        "d_nordin_redevances_ht": ["0", "26,715", "57,285", "0", "12,3", "15", "32,4", "0", "14,415", "42,285", "139,005"],
        "d_nordin_ttc": ["0", "28,247715", "59,672985", "0", "13,53", "16,5", "35,64", "0", "14,717715", "43,172985", "141,924105"],
    }

    df = pd.DataFrame(data)

    inserter = comonNordinInsert("database.db")
    inserter.insert_dataframe(df)

    # Affichage du contenu de la table
    result = inserter.fetch_all()
    print(result)
    
    #Tarif

    db_path = "database.db"

    data = {
        "id_projet": [1]*10,
        "type_tarif": ["EPA", "EPA", "EPA", "A", "A", "A", "A", "EP", "EP", "EP"],
        "indice": ["k0", "k1", "k2", "k0", "k1", "k2", "k3", "k0", "k1", "k2"],
        "bornes": [0, 15, 30, 0, 15, 30, 60, 0, 15, 30],
        "prix_ht_op": [2.178, 3.959, 4.978, 1.3, 2.12, 2.21, 2.5, 0.878, 1.839, 2.768],
        "redevances": [0.16, 0.16, 0.16, 0.04, 0.04, 0.04, 0.04, 0.12, 0.12, 0.12],
        "prix_htva": [2.338, 4.119, 5.138, 1.34, 2.16, 2.25, 2.54, 0.998, 1.959, 2.888],
        "montant_tva_unite_service": [0.154958, 0.257139, 0.285648, 0.134, 0.216, 0.225, 0.254, 0.020958, 0.041139, 0.060648],
        "prix_ttc": [2.492958, 4.376139, 5.423648, 1.474, 2.376, 2.475, 2.794, 1.018958, 2.000139, 2.948648]
    }

    df = pd.DataFrame(data)
    service = ComonTarifTableInsert(db_path)
    service.create_table()
    service.insert_dataframe(df)

    print("✅ Données insérées avec succès dans la table comon_tarif.")
    
    # TVA et Redevance

     # Maintenant utiliser le service d'insertion
    data = {
        'id_projet': [1, 1, 1],
        'type_taxe': ['EPA', 'A', 'EP'],
        'taux_tva_pourcent': [0, 10, 2.1],
        'redevances_accise_euro_m3': [0.16, 0.04, 0.12]
    }
    df = pd.DataFrame(data)
    
    inserter = ComonTavaRedevanceInsertSrv()

    inserter.insert_from_dataframe(df)
    print("Insertion terminée avec succès !")

    # TVA et redevance TBSE

    df = pd.DataFrame({
        'id_projet': [1, 1, 1],
        'type_tva': ['EPA', 'A', 'EPA'],
        'taux_tva_pct': [0, 10, 2.1],
        'redevances_accise_eur_m3': [0.16, 0.04, 0.12]
    })

    # Insertion dans la base
    inserter = ComonTvaRedTBSEInsertSrv('database.db')
    inserter.insert_dataframe(df)
    inserter.close()


if __name__ == "__main__":
    main()