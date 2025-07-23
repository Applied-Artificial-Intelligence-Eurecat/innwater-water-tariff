from flask import Flask, jsonify, abort, request
import os
import sqlite3
import numpy as np
from datetime import datetime
import logging

# Import de toutes les classes métier
from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW
from AFS_IncidenceCalc import AFS_IncidenceCalc
from afs_Intensity import AFSIntensityCalc
from aFSPopHhInDiff import AFSPopHHDiff
from AFS_InequalityCalc import AFS_InequalityCalc
from AFSAffIndicBWCar import AFSAffIndicBWCar
from AFSAffIndicDWCar import AFSAffIndicDWCar
from aFS_IncidCalcCar import AFS_IncidCalcCar
from aFSIntensCalcCar import aFSIntensCalcCar
from aFSIntensCalcCarDa import aFSIntensCalcCarDa
from AFSInequalCalcCar import AFSInequalCalcCar
from aFSPopHhDiffCar import aFSPopHhDiffCar

# Initialisation de Flask et du logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

# --- Utility function ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Endpoints originaux de la première application ---

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

# --- Endpoints originaux de la deuxième application ---

@app.route('/')
def index():
    return jsonify({"message": "API unifiée opérationnelle"}), 200

@app.route('/api/AFSAffIndicBWCar/<int:project_id>', methods=['GET'])
def get_AFSAffIndicBWCar(project_id):
    app.logger.info(f"[AFSAffIndicBWCar] project_id={project_id}")
    if not AFSAffIndicBWCar.project_exists(project_id):
        return jsonify({"status": "error", "message": f"Project {project_id} not found"}), 404
    
    with AFSAffIndicBWCar(project_id) as car_data:
        data = car_data.get_indicators()
    
    return jsonify({
        "status": "success",
        "project_id": project_id,
        "data": data
    })

@app.route('/api/AFSAffIndicDWCar/<int:project_id>', methods=['GET'])
def get_AFSAffIndicDWCar(project_id):
    app.logger.info(f"[AFSAffIndicDWCar] project_id={project_id}")
    car_data = AFSAffIndicDWCar()
    project_data = car_data.get_project_data(project_id)
    if not project_data:
        return jsonify({"status": "error", "message": f"Project {project_id} not found"}), 404
    return jsonify({"status": "success", "project_id": project_id, "data": project_data})

@app.route("/api/afs_incid_calc_car/<int:project_id>", methods=["GET"])
def get_afs_incid_calc_car(project_id):
    app.logger.info(f"[AFS_IncidCalcCar] project_id={project_id}")
    try:
        calc = AFS_IncidCalcCar(project_id=project_id)
        data = calc.to_dict()
        return jsonify(data), 200
    except Exception as e:
        app.logger.error(f"Error in get_afs_incid_calc_car: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/get_afsintenscalc_by_project', methods=['GET'])
def get_afsintenscalc_by_project():
    id_projet = request.args.get('id_projet')
    app.logger.info(f"[aFSIntensCalcCar] id_projet={id_projet}")

    if id_projet is None:
        return jsonify({'error': 'id_projet parameter is required'}), 400

    try:
        id_projet = int(id_projet)
    except ValueError:
        return jsonify({'error': 'id_projet must be an integer'}), 400

    calc = aFSIntensCalcCar()
    conn = sqlite3.connect(calc.db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, DeficitApparent, CAR_IBT, CAR_TBSE, Delta_CAR, id_projet
        FROM aFSIntensCalcCar
        WHERE id_projet = ?
    """, (id_projet,))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            'id': row[0],
            'DeficitApparent': row[1],
            'CAR_IBT': row[2],
            'CAR_TBSE': row[3],
            'Delta_CAR': row[4],
            'id_projet': row[5]
        })

    return jsonify(results)

@app.route("/api/aFSIntensCalcCarDa/<int:project_id>", methods=["GET"])
def get_aFSIntensCalcCarDa(project_id):
    app.logger.info(f"[aFSIntensCalcCarDa] project_id={project_id}")
    try:
        db_path = 'database.db'
        table_name = 'aFSIntensCalcCarDa'
        calc = aFSIntensCalcCarDa(id_projet=project_id, db_path=db_path)
        calc.create_table(table_name=table_name)
        calc.insert_data(table_name=table_name)

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
        app.logger.error(f"Error in get_aFSIntensCalcCarDa: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/inequal-calc-car/<int:id_projet>', methods=['GET'])
def get_inequal_calc_car(id_projet):
    app.logger.info(f"[AFSInequalCalcCar] id_projet={id_projet}")
    try:
        afs = AFSInequalCalcCar()
        df = afs.get_data(id_projet)

        if df.empty:
            app.logger.warning(f"No data found for id_projet: {id_projet}")
            return jsonify({
                "status": "error",
                "message": f"Aucune donnée trouvée pour l'ID projet {id_projet}",
                "id_projet": id_projet
            }), 404

        result = df.to_dict(orient='records')
        return jsonify({
            "status": "success",
            "id_projet": id_projet,
            "data": result
        }), 200

    except Exception as e:
        app.logger.error(f"Error in get_inequal_calc_car: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "id_projet": id_projet
        }), 500

@app.route('/api/pop-hh-diffcar/<int:id_projet>', methods=['GET'])
def get_pop_hh_diffcar(id_projet):
    app.logger.info(f"[aFSPopHhDiffCar] id_projet={id_projet}")
    try:
        data_handler = aFSPopHhDiffCar(id_projet=id_projet)
        df = data_handler.construire_dataframe()
        data_handler.creer_table_sqlite()
        data_handler.inserer_donnees_sqlite()

        if df.empty:
            app.logger.warning(f"No data found for id_projet: {id_projet}")
            return jsonify({
                "status": "error",
                "message": f"Aucune donnée trouvée pour l'ID projet {id_projet}",
                "id_projet": id_projet
            }), 404

        result = df.to_dict(orient='records')
        return jsonify({
            "status": "success",
            "id_projet": id_projet,
            "data": result
        }), 200

    except Exception as e:
        app.logger.error(f"Error in get_pop_hh_diffcar: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "id_projet": id_projet
        }), 500

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