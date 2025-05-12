from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Verificar que se ha enviado un archivo
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        # Guardar la imagen en el servidor
        filename = "captura.jpg"
        file.save(filename)

        return "Imagen recibida", 200
    except Exception as e:
        print(e)
        return "Error en el servidor", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
