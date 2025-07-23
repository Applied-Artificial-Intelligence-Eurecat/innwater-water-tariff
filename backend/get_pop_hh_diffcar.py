from flask import Flask, jsonify
from aFSPopHhDiffCar import aFSPopHhDiffCar

app = Flask(__name__)

@app.route('/api/pop-hh-diffcar/<int:id_projet>', methods=['GET'])
def get_pop_hh_diffcar(id_projet):
    try:
        # Initialisation de l'handler de données
        data_handler = aFSPopHhDiffCar(id_projet=id_projet)
        
        # Construction du DataFrame
        df = data_handler.construire_dataframe()
        
        # Création de la table si elle n'existe pas (optionnelle)
        data_handler.creer_table_sqlite()
        
        # Insertion des données dans la table (append)
        data_handler.inserer_donnees_sqlite()
        
        # Conversion du DataFrame en JSON
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
