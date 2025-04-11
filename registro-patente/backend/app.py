from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection

app = Flask(__name__)
CORS(app)  # Permite peticiones desde React

@app.route('/registro-visita', methods=['POST'])
def registro_visita():
    data = request.get_json()
    nombre = data.get('nombre')
    motivo = data.get('motivo')
    persona = data.get('persona')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visitas (nombre, motivo, persona) VALUES (%s, %s, %s)", (nombre, motivo, persona))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Visita registrada"}), 200

@app.route('/registro-propietario', methods=['POST'])
def registro_propietario():
    data = request.get_json()
    nombre = data.get('nombre')
    unidad = data.get('unidad')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO propietarios (nombre, unidad) VALUES (%s, %s)", (nombre, unidad))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Propietario registrado"}), 200

if __name__ == '__main__':
    app.run(debug=True)
