from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capturar_y_procesar():
    try:
        print("📥 Solicitud recibida desde ESP32. Ejecutando controlador de captura...")

        # Ruta correcta y completa al script en el servidor EC2
        script_path = "/home/ubuntu/electronica-inf/registro-patente/backend/app/camera/rekognition_capture_controller.py"

        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True
        )

        print("🧠 Resultado del script:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0:
            return jsonify({"status": "ok", "output": result.stdout}), 200
        else:
            return jsonify({"status": "error", "output": result.stderr}), 500

    except Exception as e:
        print("⚠️ Error ejecutando script:", e)
        return jsonify({"status": "exception", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
