import base64
import paho.mqtt.client as mqtt
from datetime import datetime
import os

# ⚙️ CONFIGURACIÓN
MQTT_BROKER = "54.243.184.8"
MQTT_PORT = 1883
MQTT_TOPIC = "patentes/captura"
IMAGES_DIR = "imagenes_recibidas"

# 📁 Crear carpeta si no existe
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# 📥 CALLBACK cuando llega un mensaje
def on_message(client, userdata, msg):
    print("📥 Imagen recibida desde topic:", msg.topic)

    try:
        # Decodificamos el base64
        img_data = base64.b64decode(msg.payload)

        # Nombre con timestamp
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        filepath = os.path.join(IMAGES_DIR, filename)

        # Guardamos la imagen
        with open(filepath, "wb") as f:
            f.write(img_data)

        print(f"✅ Imagen guardada en {filepath}")
    except Exception as e:
        print("❌ Error al guardar imagen:", e)

# 🚀 Conectar al broker
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
print("📡 Escuchando en topic:", MQTT_TOPIC)

# 🌀 Loop infinito
client.loop_forever()
