import base64
import boto3
import paho.mqtt.client as mqtt
from datetime import datetime
import os

# === CONFIGURACIÓN ===

MQTT_BROKER = "172.31.83.70"  # IP privada de la instancia MQTT (desde EC2 "prueba")
MQTT_PORT = 1883
MQTT_TOPIC = "patentes/captura"

IMAGE_PATH = "/tmp/captura.jpg"
BUCKET_NAME = "esp32-captures"
S3_IMAGE_KEY = "captura.jpg"

rekognition = boto3.client("rekognition", region_name="us-east-1")
s3 = boto3.client("s3")

# === LÓGICA PRINCIPAL ===

def subir_imagen_a_s3():
    try:
        if not os.path.exists(IMAGE_PATH):
            print("❌ No se encontró la imagen:", IMAGE_PATH)
            return False

        print("☁️ Subiendo imagen a S3...")
        s3.upload_file(IMAGE_PATH, BUCKET_NAME, S3_IMAGE_KEY)
        print("✅ Imagen subida a S3")
        return True

    except Exception as e:
        print("⚠️ Error subiendo a S3:", e)
        return False

def detectar_patente_rekognition():
    try:
        response = rekognition.detect_text(
            Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': S3_IMAGE_KEY}}
        )
        posibles_lineas = [d for d in response['TextDetections'] if d['Type'] == 'LINE']
        for linea in posibles_lineas:
            texto = linea['DetectedText'].replace(" ", "")
            if 6 <= len(texto) <= 8 and any(c.isdigit() for c in texto):
                return texto
        return None
    except Exception as e:
        print("⚠️ Error en Rekognition:", e)
        return None

# === CALLBACKS MQTT ===

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado a MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print("❌ Error de conexión MQTT. Código:", rc)

def on_message(client, userdata, msg):
    print(f"\n📥 Imagen recibida en {msg.topic}")
    try:
        image_data = base64.b64decode(msg.payload)
        with open(IMAGE_PATH, "wb") as f:
            f.write(image_data)
        print(f"💾 Imagen guardada como {IMAGE_PATH}")

        if subir_imagen_a_s3():
            patente = detectar_patente_rekognition()
            if patente:
                print(f"🔠 Patente detectada: {patente}")
            else:
                print("🚫 No se detectó ninguna patente")

    except Exception as e:
        print("❌ Error procesando imagen:", e)

# === INICIALIZACIÓN MQTT ===

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Conectando a MQTT...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
