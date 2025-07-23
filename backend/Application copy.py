import sqlite3
import pandas as pd
from flask import Flask, jsonify, request, abort, Response
from AFS_AffordabilityIndicatorBW import AFS_AffordabilityIndicatorBW
from AFS_AffordabilityIndicatorDW import AFS_AffordabilityIndicatorDW
from AFS_IncidenceCalc import AFS_IncidenceCalc
from afs_Intensity import AFSIntensityCalc
from AFS_InequalityCalc import AFS_InequalityCalc
from AFS_pop_hh_in_difficulty import AFS_pop_hh_in_difficulty
from PopulationDifficultyService import PopulationDifficultyService
from datetime import datetime
from functools import wraps
import math
import json
import os
from ProjectCheckService import ProjectCheckService

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données
DATABASE_PATH = os.getenv('DATABASE_PATH', 'default_database.db')
# Créez une instance du service
project_check_service = ProjectCheckService()

# ------------------ Utilitaires ------------------
def get_db_connection():
    """Crée une connexion à la base de données"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def project_exists_in_database(project_id):
    """Vérifie si un projet existe dans la base de données"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM projets WHERE id = ?", (project_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    except sqlite3.Error as e:
        app.logger.error(f"Erreur base de données: {str(e)}")
        return False

def nan_converter(o):
    """Convertit les valeurs NaN en None pour la sérialisation JSON"""
    if isinstance(o, float) and math.isnan(o):
        return None
    if pd.isna(o):
        return None
    return o

def clean_dataframe(df):
    """Nettoie un DataFrame en remplaçant tous les NaN/NaT/None par None"""
    return df.where(pd.notna(df), None).replace([pd.NA, pd.NaT, None], None)

def nan_to_null_decorator(func):
    """Décorateur pour convertir les NaN en null dans les réponses JSON"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, Response):
            try:
                if response.is_json:
                    data = response.get_json()
                    cleaned = json.loads(json.dumps(data, default=nan_converter))
                    response.set_data(json.dumps(cleaned))
            except Exception:
                pass
        return response
    return wrapper

# Décorateur spécifique pour pop-hh-difficulty
def check_pop_hh_project_exists(f):
    @wraps(f)
    def wrapper(project_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM AFS_pop_hh_in_difficulty WHERE id_projet = ?", 
            (project_id,)
        )
        if not cursor.fetchone():
            conn.close()
            abort(404, description=f"Le projet {project_id} n'existe pas dans AFS_pop_hh_in_difficulty")
        conn.close()
        return f(project_id)
    return wrapper

# ------------------ Middleware de vérification de projet ------------------
def check_project_exists(f):
    """Middleware pour vérifier l'existence d'un projet"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get('project_id')
        if not project_exists_in_database(project_id):
            return jsonify({
                'error': 'not_found',
                'message': f'Le projet {project_id} n\'existe pas dans la base de données'
            }), 404
        return f(*args, **kwargs)
    return decorated_function

# ------------------ Endpoints ------------------
@app.route('/api/affordability-indicators/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_project_exists
def get_affordability_indicators(project_id):
    """Endpoint pour les indicateurs d'accessibilité BW"""
    try:
        with AFS_AffordabilityIndicatorBW(project_id) as analyzer:
            response_data = analyzer.get_project_data()
            
            if not response_data:
                return jsonify({
                    'error': 'not_found',
                    'message': f'Aucun indicateur trouvé pour le projet {project_id}'
                }), 404
                
            return jsonify(response_data)
            
    except ValueError as e:
        return jsonify({'error': 'invalid_input', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'server_error', 'message': str(e)}), 500
    
    
@app.route('/api/affordability-dw/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_project_exists
def get_affordability_dw_data(project_id):
    """Endpoint pour les indicateurs d'accessibilité DW"""
    try:
        analyzer = AFS_AffordabilityIndicatorDW(project_id=project_id)
        df = clean_dataframe(analyzer.build_dataframe())
        project_data = df[df['id_projet'] == project_id]

        if project_data.empty:
            return jsonify({'message': f'Aucun indicateur DW pour le projet {project_id}'}), 404

        return jsonify({
            'id_projet': project_id,
            'count': len(project_data),
            'data': project_data.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/incidence-calc/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_project_exists
def get_incidence_calc_data(project_id):
    """Endpoint pour les calculs d'incidence"""
    try:
        calculator = AFS_IncidenceCalc(project_id=project_id)
        df = clean_dataframe(calculator.build_dataframe())
        project_data = df[df['id_projet'] == project_id]

        if project_data.empty:
            return jsonify({'message': f'Aucune donnée de calcul pour le projet {project_id}'}), 404

        return jsonify({
            'id_projet': project_id,
            'count': len(project_data),
            'data': project_data.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/intensity-calc/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_project_exists
def get_intensity_calc_data(project_id):
    """Endpoint pour les calculs d'intensité"""
    try:
        calculator = AFSIntensityCalc(project_id=project_id)
        df = clean_dataframe(calculator.build_dataframe())

        result = {
            'id_projet': project_id,
            'metrics': [],
            'stats': {
                'total_metrics': len(df),
                'has_null_values': df.isnull().values.any()
            }
        }

        for index, row in df.iterrows():
            metric = {
                'metric_name': index,
                'values': {
                    'par_ibt': row['par_ibt'],
                    'par_tbse': row['par_tbse'],
                    'delta_par': row['delta_par']
                },
                'detailed_stats': {
                    'de_moy': row['de_moy'],
                    'de_med': row['de_med'],
                    'de_var': row.get('de_var'),
                    'de_std': row.get('de_std'),
                    'de_cv': row.get('de_cv'),
                    'de_mape': row.get('de_mape')
                }
            }
            result['metrics'].append(metric)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': f"Erreur lors du calcul des intensités pour le projet {project_id}"
        }), 500

@app.route('/api/inequality-calc/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_project_exists
def get_inequality_data(project_id):
    """Endpoint pour les calculs d'inégalité"""
    try:
        calculator = AFS_InequalityCalc(project_id)
        df = clean_dataframe(calculator.build_dataframe())

        if df.empty:
            return jsonify({
                'message': f'Aucune donnée d\'inégalité pour le projet {project_id}',
                'status': 'no_data'
            }), 404

        response = {
            'project_id': project_id,
            'indicators': df.to_dict(orient='records'),
            'metadata': {
                'source': calculator.database_name,
                'indicators_count': len(df),
                'generated_at': datetime.now().isoformat()
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': str(e)
        }), 500

# Modifiez l'endpoint
@app.route('/api/pop-hh-difficulty/<int:project_id>', methods=['GET'])
@nan_to_null_decorator
@check_pop_hh_project_exists  # Utilise le décorateur modifié
def get_pop_hh_difficulty(project_id):
    """Endpoint pour les difficultés de population/ménages"""
    try:
        if not 1 <= project_id <= 1000:
            abort(400, description="ID de projet hors plage valide")

        # Utilise le service modifié
        data = PopulationDifficultyService.get_data(project_id)

        if data.empty:  # Vérifie si le DataFrame est vide
            abort(404, description=f"Données non trouvées pour le projet {project_id}")

        cleaned_data = clean_dataframe(data)

        return jsonify({
            'project_id': project_id,
            'data': cleaned_data.to_dict(orient='records'),
            '_links': {
                'self': f'/api/pop-hh-difficulty/{project_id}',
                'projects': '/api/projects'
            }
        })

    except sqlite3.Error as e:
        abort(503, description="Service temporairement indisponible")

# ------------------ Health Check ------------------
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'application"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': 'connected' if get_db_connection() else 'disconnected'
        }
    })

# ------------------ Lancement de l'application ------------------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)