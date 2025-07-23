# app_flask.py

from flask import Flask, request, jsonify
from aFSIntensCalcCarDa import aFSIntensCalcCarDa
import sqlite3

app = Flask(__name__)

@app.route('/aFSIntensCalcCarDa', methods=['POST'])
def generate_aFSIntensCalcCarDa():
    try:
        # Récupération des données JSON
        data = request.get_json()
        id_projet = data.get('id_projet', 1)
        db_path = data.get('db_path', 'database.db')
        table_name = 'aFSIntensCalcCarDa'
        
        # Initialisation de la classe
        calc = aFSIntensCalcCarDa(id_projet=id_projet, db_path=db_path)
        
        # Création de la table si elle n'existe pas
        calc.create_table(table_name=table_name)
        
        # Insertion des données
        calc.insert_data(table_name=table_name)
        
        # Connexion à la base pour récupérer les données filtrées par id_projet
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT id_projet, Metric, CAR_IBT, CAR_TBSE, Delta_CAR 
                FROM {table_name}
                WHERE id_projet = ?
            """, (id_projet,))
            
            rows = cursor.fetchall()
            
            # Transformation en liste de dictionnaires
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
            "message": f"✅ Données générées et récupérées pour le projet {id_projet}.",
            "data": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
