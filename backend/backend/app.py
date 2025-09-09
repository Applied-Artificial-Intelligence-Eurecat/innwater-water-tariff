from fastapi import FastAPI
from common_param.DatabaseInsertParameterP import DatabaseInsertParameterP
from common_param.DatabaseTableManagerP import DatabaseTableManagerP
from VarParMenageMain import VarParMenageMain

app = FastAPI()

@app.get("/lunch-simulation")
def lunch_simulation():
    try:
        # Étape 1 : création des tables
        table_manager = DatabaseTableManagerP("database.db")
        table_manager.create_all_tables()
        # table result to migrate in table manager
        # Étape 2 : insertion des données
        insert_manager = DatabaseInsertParameterP("database.db")
        insert_manager.run_all_insertions()

        # Étape 3 : exécution de la logique principale
        main = VarParMenageMain()
        main.run()

        return {
            "status": "success",
            "message": "Tables créées, données insérées et traitement exécuté avec succès."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
