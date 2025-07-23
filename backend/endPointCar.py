from flask import Flask, jsonify, request
import logging
import sqlite3

# Import de tes classes métier
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

@app.route('/')
def index():
    return jsonify({"message": "API unifiée opérationnelle"}), 200

# ----------------------------------------------------
# Endpoint 1 : get_AFSAffIndicBWCar
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

# ----------------------------------------------------
# Endpoint 2 : appAFSAffIndicDWCar
@app.route('/api/AFSAffIndicDWCar/<int:project_id>', methods=['GET'])
def get_AFSAffIndicDWCar(project_id):
    app.logger.info(f"[AFSAffIndicDWCar] project_id={project_id}")
    car_data = AFSAffIndicDWCar()
    project_data = car_data.get_project_data(project_id)
    if not project_data:
        return jsonify({"status": "error", "message": f"Project {project_id} not found"}), 404
    return jsonify({"status": "success", "project_id": project_id, "data": project_data})

# ----------------------------------------------------
# Endpoint 3 : get_afs_incid_calc_car
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

# ----------------------------------------------------
# Endpoint 4 : get_aFSIntensCalcCar
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

# ----------------------------------------------------
# Endpoint 5 : generate_aFSIntensCalcCarDa
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

# ----------------------------------------------------
# Endpoint 6 : get_inequal_calc_car
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

# ----------------------------------------------------
# Endpoint 7 : get_pop_hh_diffcar
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

# ----------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
