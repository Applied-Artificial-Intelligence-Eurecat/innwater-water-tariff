# --- app.py ---

from flask import Flask, jsonify, abort
import os
import sqlite3
import numpy as np
from datetime import datetime

# Import de tes classes métier
from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW
from AFS_IncidenceCalc import AFS_IncidenceCalc
from afs_Intensity import AFSIntensityCalc
from aFSPopHhInDiff import AFSPopHHDiff
from AFS_InequalityCalc import AFS_InequalityCalc  # Nouvelle importation

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

# --- Utility function ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Endpoint 1: Affordability Indicators (BW) ---
@app.route('/api/affordability-indicators/<int:project_id>', methods=['GET'])
def get_affordability_indicators(project_id):
    try:
        if not os.path.exists(DATABASE):
            abort(500, description="Base de données introuvable")

        if not AFS_AffordabilityIndicatorBW.project_exists(project_id, DATABASE):
            abort(404, description=f"Aucune donnée trouvée pour le projet ID {project_id}")

        with AFS_AffordabilityIndicatorBW(project_id, DATABASE) as db:
            data = db.get_project_stats()

            if not data['stats']:
                return jsonify({
                    "status": "success",
                    "project_id": project_id,
                    "message": "Aucune métrique disponible",
                    "metadata": data['metadata']
                })
            
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "metrics": data['stats'],
                "metadata": data['metadata']
            })

    except sqlite3.Error as e:
        abort(500, description=f"Erreur de base de données: {str(e)}")
    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")


# --- Endpoint 2: Affordability Indicator DW ---
@app.route('/api/affordability-dw/<int:project_id>', methods=['GET'])
def get_affordability_indicator_dw(project_id):
    try:
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
            abort(404, description=f"Project ID {project_id} not found in AFS_AffordabilityIndicatorDW.")

        # Extraction des valeurs
        par_ibt_values = [row["par_ibt"] for row in rows if row["par_ibt"] is not None]
        par_tbse_values = [row["par_tbse"] for row in rows if row["par_tbse"] is not None]

        # Calcul des statistiques
        def calculate_statistics(values):
            arr = np.array(values)
            return {
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "q1": float(np.percentile(arr, 25)),
                "q3": float(np.percentile(arr, 75)),
                "d1": float(np.percentile(arr, 10)),
                "d9": float(np.percentile(arr, 90)),
                "mean": float(np.mean(arr))
            }

        par_ibt_stats = calculate_statistics(par_ibt_values)
        par_tbse_stats = calculate_statistics(par_tbse_values)
        delta_par = par_tbse_stats["mean"] - par_ibt_stats["mean"]

        response = {
            "status": "success",
            "project_id": project_id,
            "metrics": [
                {"metric": "PAR IBT", **par_ibt_stats},
                {"metric": "PAR TBSE", **par_tbse_stats},
                {"metric": "Delta PAR", "value": round(delta_par, 4)}
            ],
            "metadata": {
                "computed_at": datetime.utcnow().isoformat() + "Z",
                "source": "AFS_AffordabilityIndicatorDW"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")


# --- Endpoint 3: Incidence Calculation ---
@app.route('/api/incidence-calc/<int:project_id>', methods=['GET'])
def get_incidence_calc(project_id):
    try:
        calc = AFS_IncidenceCalc(project_id)
        df = calc.build_dataframe()

        if df.empty:
            abort(404, description=f"Projet ID {project_id} introuvable.")

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
                "table": calc.table_name,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")


# --- Endpoint 4: Intensity Calculation ---
@app.route('/api/afs-intensity-calc/<int:project_id>', methods=['GET'])
def afs_intensity_calc_get_data(project_id):
    try:
        afs_calc = AFSIntensityCalc(project_id=project_id)
        afs_calc.build_dataframe()
        afs_calc.create_sqlite_table()
        afs_calc.insert_data()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM afs_intensitycalc WHERE project_id = ?", (project_id,))
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]

        return jsonify({
            "status": "success",
            "project_id": project_id,
            "data": data
        }), 200

    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")
        
# --- Endpoint 5: Population HH Difficulty ---
@app.route('/api/pop-hh-difficulty/<int:project_id>', methods=['GET'])
def get_pop_hh_difficulty(project_id):
    try:
        data_handler = AFSPopHHDiff(id_projet=project_id)
        data_handler.initialize_database()
        df = data_handler.get_data()

        if df.empty:
            abort(404, description=f"Aucune donnée trouvée pour le projet ID {project_id}.")

        data = df.to_dict(orient='records')
        response = {
            "status": "success",
            "project_id": project_id,
            "data": data,
            "metadata": {
                "source": "AFSPopHHDiff",
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")

# --- Endpoint 6: Inequality Calculation ---
@app.route('/api/inequality/<int:project_id>', methods=['GET', 'POST'])
def handle_inequality(project_id):
    try:
        calculator = AFS_InequalityCalc(project_id)
        
        if request.method == 'POST':
            # Création de la table et insertion des données
            table_success, table_msg = calculator.create_sqlite_table()
            if not table_success:
                return jsonify({"status": "error", "message": table_msg}), 500
            
            insert_success, insert_msg = calculator.insert_data()
            if not insert_success:
                return jsonify({"status": "error", "message": insert_msg}), 500
            
            return jsonify({
                "status": "success",
                "message": "Données d'inégalité initialisées",
                "project_id": project_id
            }), 201
        
        elif request.method == 'GET':
            # Récupération des données
            data = calculator.get_data_from_db()
            
            if data is None:
                return jsonify({
                    "status": "error",
                    "message": "Aucune donnée trouvée pour ce projet"
                }), 404
            
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": data,
                "metadata": {
                    "source": "AFS_InequalityCalc",
                    "generated_at": datetime.utcnow().isoformat() + "Z"
                }
            })

    except Exception as e:
        abort(500, description=f"Erreur serveur: {str(e)}")

# --- Error Handlers ---
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
        "message": str(e)
    }), 500


# --- Main ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)