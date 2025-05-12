import paho.mqtt.client as mqtt
import json
import time

BROKER = "54.243.184.8"
PORT = 1883
TOPIC = "vehicle/detected"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print("❌ Error al conectar. Código:", rc)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"📩 Mensaje recibido en '{msg.topic}': {data}")

        # Lógica de reacción → por ejemplo:
        if data.get("estado") == "presente":
            print("🚗 Vehículo detectado. Iniciando reconocimiento...")
            # Acá podrías llamar a Rekognition, activar cámara, etc.

    except Exception as e:
        print("⚠️ Error procesando mensaje:", e)


def start_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    # mantener corriendo
    while True:
        time.sleep(1)


if __name__ == "__main__":
    start_listener()
