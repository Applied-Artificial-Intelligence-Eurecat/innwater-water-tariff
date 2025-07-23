from flask import Flask, jsonify
from AFSAffIndicDWCar import AFSAffIndicDWCar # adapte selon ton chemin réel

app = Flask(__name__)
car_data = AFSAffIndicDWCar()

@app.route('/api/AFSAffIndicDWCar/<int:project_id>', methods=['GET'])
def get_car_data(project_id):
    project_data = car_data.get_project_data(project_id)
    if not project_data:
        return jsonify({"status": "error", "message": f"Project {project_id} not found"}), 404
    return jsonify({"status": "success", "project_id": project_id, "data": project_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
