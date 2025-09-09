import sqlite3
import traceback
from typing import List, Dict, Any, Optional
from commonAbSrvCreate import c_Ab_srvCreate
from CommonTBSETable import CommonTBSETable
from comonNordinCreateSrv import comonNordinCreateSrv
from comonTarifTableCreateSrv import comonTarifTableCreateSrv
from ComonTvaRedevance import ComonTvaRedevance
from comonTvaRedTBSECreateSrv import comonTvaRedTBSECreateSrv

# Importez vos classes existantes ici
# from your_module import c_Ab_srvCreate, CommonTBSETable, comonNordinCreateSrv, etc.

class DatabaseTableManager:
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
    manager = DatabaseTableManager("database.db")
    
    print("🗂️  GESTIONNAIRE DE TABLES DE BASE DE DONNÉES")
    print("=" * 50)
    
    # Abonnment 
    ab_creator = c_Ab_srvCreate("database.db")
    ab_creator.create_table()
    ab_creator.close()
    print("Table 'commonAb' recréée avec succès ✅")

     # TBSE TARIF
    tarse_table = CommonTBSETable()
    tarse_table.recreate_table()

    #Nordin
    srv = comonNordinCreateSrv()
    srv.create_table()
    
    #Tarif
    table_creator = comonTarifTableCreateSrv()
    
    # TVA et Redevance
    db = ComonTvaRedevance()
    db.close()

    # TVA et redevance TBSE
    service = comonTvaRedTBSECreateSrv()
    service.create_table()


if __name__ == "__main__":
    main()