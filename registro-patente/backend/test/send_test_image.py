import base64
import paho.mqtt.client as mqtt

# Cargar imagen
with open("patente.jpeg", "rb") as f:
    image_base64 = base64.b64encode(f.read())

# Enviar por MQTT
client = mqtt.Client()
client.connect("54.243.184.8", 1883, 60)
client.publish("patentes/captura", image_base64)
client.disconnect()

print("✅ Imagen enviada al topic 'patentes/captura'.")
