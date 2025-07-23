from flask import Flask, jsonify, abort

import sqlite3
from typing import Dict, Any
from datetime import datetime
import os

from flask import Flask, request, jsonify
from AFS_InequalityCalc import AFS_InequalityCalc  # Import de la classe

app = Flask(__name__)

@app.route('/api/inequality/<int:project_id>', methods=['GET', 'POST'])
def handle_inequality(project_id):
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
            "data": data
        })

if __name__ == '__main__':
    app.run(debug=True)