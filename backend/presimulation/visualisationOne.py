from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/plot_data', methods=['GET'])
def get_plot_data():
    try:
        # Chargement du fichier Excel
        fichier_excel = "CAR.xls"
        df = pd.read_excel(fichier_excel)
        df.columns = df.columns.str.strip()  # Nettoyage des colonnes

        # Vérification des colonnes attendues
        if 'CAR TBSE' not in df.columns or 'Rang N' not in df.columns:
            raise ValueError("Les colonnes 'CAR TBSE' et 'Rang N' sont manquantes dans le fichier Excel.")

        # Conversion des données
        df['CAR TBSE'] = pd.to_numeric(df['CAR TBSE'], errors='coerce')
        df['Rang N'] = pd.to_numeric(df['Rang N'], errors='coerce')
        df.fillna(0, inplace=True)

        # Préparation des données pour l'affichage graphique
        plot_data = {
            'percentiles': df['Rang N'].tolist(),
            'values': df['CAR TBSE'].tolist()
        }

        return jsonify(plot_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
