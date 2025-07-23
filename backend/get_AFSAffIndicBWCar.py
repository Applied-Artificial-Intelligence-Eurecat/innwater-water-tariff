from flask import Flask, jsonify
from AFSAffIndicBWCar import AFSAffIndicBWCar  # adapte ce chemin selon ton projet

app = Flask(__name__)

@app.route('/api/AFSAffIndicBWCar/<int:project_id>', methods=['GET'])
def get_car_data(project_id):
    if not AFSAffIndicBWCar.project_exists(project_id):
        return jsonify({"status": "error", "message": f"Project {project_id} not found"}), 404
    
    with AFSAffIndicBWCar(project_id) as car_data:
        data = car_data.get_indicators()
    
    return jsonify({
        "status": "success",
        "project_id": project_id,
        "data": data
    })

if __name__ == '__main__':
    # Initialise la base au lancement
    AFSAffIndicBWCar.initialize_database()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
