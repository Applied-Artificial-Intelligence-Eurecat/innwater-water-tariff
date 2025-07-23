from flask import Flask, jsonify
from aFSPopHhInDiff import AFSPopHHDiff

app = Flask(__name__)

@app.route('/api/pop-hh-difficulty/<int:id_projet>', methods=['GET'])
def get_pop_hh_difficulty(id_projet):
    try:
        # Initialisation du handler de données
        data_handler = AFSPopHHDiff(id_projet=id_projet)
        
        # Initialisation de la base de données (au premier appel)
        data_handler.initialize_database()
        
        # Récupération des données
        df = data_handler.get_data()
        
        # Conversion en format JSON
        if df.empty:
            return jsonify({
                "status": "error",
                "message": f"Aucune donnée trouvée pour l'ID projet {id_projet}"
            }), 404
        
        result = df.to_dict(orient='records')
        
        return jsonify({
            "status": "success",
            "data": result,
            "id_projet": id_projet
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "id_projet": id_projet
        }), 500

if __name__ == '__main__':
    app.run(debug=True)