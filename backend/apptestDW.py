from flask import Flask, jsonify, abort
import sqlite3
import numpy as np
from datetime import datetime

app = Flask(__name__)
DATABASE = "database.db"  # Ta base de données SQLite

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_statistics(values):
    """Calcule les statistiques nécessaires à partir d'une liste de valeurs numériques."""
    arr = np.array(values)
    stats = {
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "q1": float(np.percentile(arr, 25)),
        "q3": float(np.percentile(arr, 75)),
        "d1": float(np.percentile(arr, 10)),
        "d9": float(np.percentile(arr, 90)),
        "mean": float(np.mean(arr))
    }
    return stats

@app.route('/api/affordability-dw/<int:project_id>', methods=['GET'])
def get_affordability_indicator_dw(project_id):
    """Récupère les statistiques d'accessibilité financière depuis la table AFS_AffordabilityIndicatorDW."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT par_ibt, par_tbse
        FROM AFS_AffordabilityIndicatorDW
        WHERE id_projet = ?
    """, (project_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        abort(404, description=f"Project with id {project_id} not found in AFS_AffordabilityIndicatorDW.")

    # Extraction des valeurs
    par_ibt_values = [row["par_ibt"] for row in rows if row["par_ibt"] is not None]
    par_tbse_values = [row["par_tbse"] for row in rows if row["par_tbse"] is not None]

    # Calcul des statistiques
    par_ibt_stats = calculate_statistics(par_ibt_values)
    par_tbse_stats = calculate_statistics(par_tbse_values)

    # Calcul du Delta PAR (moyenne TBSE - moyenne IBT)
    delta_par = par_tbse_stats["mean"] - par_ibt_stats["mean"]

    # Construction de la réponse
    response = {
        "status": "success",
        "project_id": project_id,
        "metrics": [
            {
                "metric": "PAR IBT",
                **par_ibt_stats
            },
            {
                "metric": "PAR TBSE",
                **par_tbse_stats
            },
            {
                "metric": "Delta PAR",
                "value": round(delta_par, 4)
            }
        ],
        "metadata": {
            "computed_at": datetime.utcnow().isoformat() + "Z",
            "source": "AFS_AffordabilityIndicatorDW"
        }
    }

    return jsonify(response), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": str(e)
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "status": "error",
        "message": "Une erreur interne est survenue. Contactez l'administrateur."
    }), 500

if __name__ == '__main__':
    app.run(debug=True)
