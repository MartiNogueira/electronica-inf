from flask import Flask, request, jsonify
from db import verificar_patente, registrar_invitado

app = Flask(__name__)

@app.route('/verificar_patente', methods=['POST'])
def verificar():
    data = request.get_json()
    patente = data.get('patente')
    resultado = verificar_patente(patente)
    return jsonify({"acceso": "permitido" if resultado != "denegado" else "denegado", "tipo": resultado})

@app.route('/registrar_invitado', methods=['POST'])
def registrar():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    patente = data['patente']
    
    
    registrar_invitado(nombre, apellido, patente,)
    return jsonify({"status": "invitado registrado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
