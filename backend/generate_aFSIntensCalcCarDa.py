# app_flask.py

from flask import Flask, jsonify
from aFSIntensCalcCarDa import aFSIntensCalcCarDa
import sqlite3

app = Flask(__name__)

@app.route("/api/afs_incid_calc_car/<int:project_id>", methods=["GET"])
def get_aFSIntensCalcCarDa(project_id):
    try:
        db_path = 'database.db'
        table_name = 'aFSIntensCalcCarDa'
        
        # Initialisation de la classe avec l'id_projet
        calc = aFSIntensCalcCarDa(id_projet=project_id, db_path=db_path)
        
        # Crée la table si elle n'existe pas et insère les données
        calc.create_table(table_name=table_name)
        calc.insert_data(table_name=table_name)
        
        # Connexion pour récupérer les données filtrées par project_id
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT id_projet, Metric, CAR_IBT, CAR_TBSE, Delta_CAR 
                FROM {table_name}
                WHERE id_projet = ?
            """, (project_id,))
            
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                result.append({
                    "id_projet": row[0],
                    "Metric": row[1],
                    "CAR_IBT": row[2],
                    "CAR_TBSE": row[3],
                    "Delta_CAR": row[4]
                })
        
        return jsonify({
            "message": f"✅ Données récupérées pour le projet {project_id}.",
            "data": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
