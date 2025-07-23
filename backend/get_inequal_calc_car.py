from flask import Flask, jsonify
from AFSInequalCalcCar import AFSInequalCalcCar

app = Flask(__name__)

@app.route('/api/inequal-calc-car/<int:id_projet>', methods=['GET'])
def get_inequal_calc_car(id_projet):
    try:
        afs = AFSInequalCalcCar()
        df = afs.get_data(id_projet)

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
