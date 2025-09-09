import sqlite3
import traceback
from typing import List, Dict, Any, Optional
from .commonAbSrvCreate import c_Ab_srvCreate
from common_param.CommonTBSETable import CommonTBSETable
from common_param.comonNordinCreateSrv import comonNordinCreateSrv
from common_param.comonTarifTableCreateSrv import comonTarifTableCreateSrv
from common_param.ComonTvaRedevance import ComonTvaRedevance
from common_param.comonTvaRedTBSECreateSrv import comonTvaRedTBSECreateSrv

class DatabaseTableManagerP:
    """
    Gestionnaire centralisé pour l'instanciation et la création de toutes les tables.
    Gère les différents patterns utilisés dans vos classes.
    """
    
    def __init__(self, db_name: str = "database.db"):
        self.db_name = db_name
        self.results = {}
        self.errors = {}
    
    def create_all_tables(self):
        """Crée toutes les tables nécessaires et logge les succès/erreurs."""
        print("🗂️  GESTIONNAIRE DE TABLES DE BASE DE DONNÉES")
        print("=" * 50)
        
        try:
            # Abonnement
            ab_creator = c_Ab_srvCreate(self.db_name)
            ab_creator.create_table()
            ab_creator.close()
            self.results['commonAb'] = "✅ Table 'commonAb' recréée avec succès"
            print(self.results['commonAb'])
        except Exception as e:
            self.errors['commonAb'] = str(e)
            print(f"❌ Erreur création table 'commonAb' : {e}")
            traceback.print_exc()
        
        try:
            # TBSE TARIF
            tarse_table = CommonTBSETable()
            tarse_table.recreate_table()
            self.results['CommonTBSETable'] = "✅ Table 'CommonTBSETable' recréée"
            print(self.results['CommonTBSETable'])
        except Exception as e:
            self.errors['CommonTBSETable'] = str(e)
            print(f"❌ Erreur création table 'CommonTBSETable' : {e}")
            traceback.print_exc()
        
        try:
            # Nordin
            srv = comonNordinCreateSrv()
            srv.create_table()
            self.results['comonNordin'] = "✅ Table 'comonNordin' recréée"
            print(self.results['comonNordin'])
        except Exception as e:
            self.errors['comonNordin'] = str(e)
            print(f"❌ Erreur création table 'comonNordin' : {e}")
            traceback.print_exc()
        
        try:
            # Tarif
            table_creator = comonTarifTableCreateSrv()
            table_creator.create_table()
            self.results['comonTarif'] = "✅ Table 'comonTarif' recréée"
            print(self.results['comonTarif'])
        except Exception as e:
            self.errors['comonTarif'] = str(e)
            print(f"❌ Erreur création table 'comonTarif' : {e}")
            traceback.print_exc()
        
        try:
            # TVA et Redevance
            db = ComonTvaRedevance()
            db.close()
            self.results['ComonTvaRedevance'] = "✅ Table 'ComonTvaRedevance' traitée"
            print(self.results['ComonTvaRedevance'])
        except Exception as e:
            self.errors['ComonTvaRedevance'] = str(e)
            print(f"❌ Erreur création table 'ComonTvaRedevance' : {e}")
            traceback.print_exc()
        
        try:
            # TVA et redevance TBSE
            service = comonTvaRedTBSECreateSrv()
            service.create_table()
            self.results['comonTvaRedTBSE'] = "✅ Table 'comonTvaRedTBSE' recréée"
            print(self.results['comonTvaRedTBSE'])
        except Exception as e:
            self.errors['comonTvaRedTBSE'] = str(e)
            print(f"❌ Erreur création table 'comonTvaRedTBSE' : {e}")
            traceback.print_exc()


if __name__ == "__main__":
    manager = DatabaseTableManagerP("database.db")
    manager.create_all_tables()
