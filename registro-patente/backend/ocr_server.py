import base64
import pytesseract
from PIL import Image
from io import BytesIO
import paho.mqtt.client as mqtt
import os

# Crear carpeta de logs si no existe
os.makedirs("../logs", exist_ok=True)

# Callback al recibir mensaje
def on_message(client, userdata, msg):
    print(f"[MQTT] Mensaje recibido en {msg.topic}")
    try:
        # Decodificar imagen
        image_data = base64.b64decode(msg.payload)
        image = Image.open(BytesIO(image_data))
        image_path = "../logs/imagen_recibida.jpg"
        image.save(image_path)

        # Aplicar OCR
        text = pytesseract.image_to_string(image)
        print("Texto detectado:")
        print(text.strip())

    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")

# Config MQTT
broker = "localhost"
topic = "patentes/captura"

client = mqtt.Client()
client.on_message = on_message

client.connect(broker, 1883, 60)
client.subscribe(topic)

print(f"[MQTT] Escuchando en topic '{topic}'...")
client.loop_forever()
