import paho.mqtt.client as mqtt
from capture_controller import capture_and_validate

MQTT_BROKER = "54.243.184.8"  # IP privada de tu instancia MQTT
MQTT_PORT = 1883
TOPIC = "captura/iniciar"

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker MQTT con código", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"📩 Mensaje recibido: {message}")
    if message == "iniciar":
        print("🚗 Auto detectado → ejecutando captura")
        capture_and_validate()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("⏳ Esperando mensajes MQTT...")
client.loop_forever()
