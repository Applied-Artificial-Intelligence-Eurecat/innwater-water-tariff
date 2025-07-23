from flask import Flask, jsonify, abort
import os
import sqlite3
from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

@app.route('/api/affordability-indicators/<int:project_id>', methods=['GET'])
def get_affordability_indicators(project_id):
    """Endpoint adapté au nouveau schéma"""
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)