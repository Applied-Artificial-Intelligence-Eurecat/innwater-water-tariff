from flask import Flask, jsonify, request
import sqlite3
from aFSIntensCalcCar import aFSIntensCalcCar

app = Flask(__name__)

# Instanciation de la classe pour utilisation si besoin
calc = aFSIntensCalcCar()

@app.route('/get_afsintenscalc_by_project', methods=['GET'])
def get_afsintenscalc_by_project():
    # Récupération de l'id_projet depuis les paramètres GET
    id_projet = request.args.get('id_projet')

    if id_projet is None:
        return jsonify({'error': 'id_projet parameter is required'}), 400

    try:
        id_projet = int(id_projet)
    except ValueError:
        return jsonify({'error': 'id_projet must be an integer'}), 400

    # Connexion à la base de données
    conn = sqlite3.connect(calc.db_path)
    cursor = conn.cursor()

    # Requête filtrée sur id_projet
    cursor.execute("""
        SELECT id, DeficitApparent, CAR_IBT, CAR_TBSE, Delta_CAR, id_projet
        FROM aFSIntensCalcCar
        WHERE id_projet = ?
    """, (id_projet,))

    rows = cursor.fetchall()

    conn.close()

    # Transformation en liste de dictionnaires pour retour JSON
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

if __name__ == '__main__':
    app.run(debug=True)
