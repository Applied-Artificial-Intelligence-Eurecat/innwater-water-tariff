# --- Flask App et Endpoint ---

from flask import Flask, jsonify, abort
import sqlite3
import numpy as np
from datetime import datetime
from AFS_IncidenceCalc import AFS_IncidenceCalc
app = Flask(__name__)

@app.route('/api/incidence_calc/<int:project_id>', methods=['GET'])
def get_incidence_calc(project_id: int):
    try:
        # Instanciation de la classe pour le projet donné
        calc = AFS_IncidenceCalc(project_id)
        df = calc.build_dataframe()

        # Si le DataFrame est vide, renvoyer 404
        if df.empty:
            return jsonify({
                "status": "error",
                "message": f"Projet avec ID {project_id} introuvable."
            }), 404

        # Construction de la réponse
        metrics = []
        for _, row in df.iterrows():
            metrics.append({
                "category": row["category"],
                "headcount_ratio": row["headcount_ratio"],
                "par_ibt": row["par_ibt"],
                "par_tbse": row["par_tbse"],
                "delta_par": row["delta_par"]
            })

        response = {
            "status": "success",
            "project_id": project_id,
            "metrics": metrics,
            "metadata": {
                "source": calc.database_name,
                "table": calc.table_name
            }
        }
        return jsonify(response), 200

    except Exception as e:
        # Gestion des erreurs internes
        return jsonify({
            "status": "error",
            "message": f"Erreur interne du serveur : {str(e)}"
        }), 500

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True)
