from flask import Flask, jsonify, abort
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/incidence_calc/<int:project_id>", methods=["GET"])
def get_incidence_calc(project_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT ensemble, ibt, tbse
        FROM AFS_InequalityCalc
        WHERE id_projet = ?
        """
        cursor.execute(query, (project_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({
                "status": "error",
                "message": f"Projet avec l'ID {project_id} introuvable."
            }), 404

        metrics = []
        for row in rows:
            delta_par = round(row["ibt"] - row["tbse"], 2)
            metrics.append({
                "metric": row["ensemble"],
                "par_ibt": row["ibt"],
                "par_tbse": row["tbse"],
                "delta_par": delta_par
            })

        response = {
            "status": "success",
            "project_id": project_id,
            "metrics": metrics,
            "metadata": {
                "source": "SQLite database",
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
        }
        return jsonify(response), 200

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return jsonify({
            "status": "error",
            "message": "Erreur interne du serveur. Veuillez réessayer plus tard."
        }), 500

    except Exception as e:
        print(f"Erreur générale: {e}")
        return jsonify({
            "status": "error",
            "message": "Erreur interne du serveur. Veuillez réessayer plus tard."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
