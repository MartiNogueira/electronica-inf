from flask import Flask, jsonify
import subprocess

app = Flask(__name__)


@app.route('/capture', methods=['GET'])
def capturar_y_procesar():
    try:
        print("📥 Solicitud recibida desde ESP32. Ejecutando controlador de captura...")

        result = subprocess.run(
            ["python3", "camera/rekognition_capture_controller.py"],  # asegúrate de tener este script en el mismo directorio
            capture_output=True,
            text=True
        )

        print("🧠 Resultado del script:")
        print(result.stdout)

        if result.returncode == 0:
            return jsonify({"status": "ok", "output": result.stdout}), 200
        else:
            return jsonify({"status": "error", "output": result.stderr}), 500

    except Exception as e:
        print("⚠️ Error ejecutando script:", e)
        return jsonify({"status": "exception", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
