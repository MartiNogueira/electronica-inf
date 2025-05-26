import boto3
import paho.mqtt.client as mqtt
from datetime import datetime
import os

# === CONFIGURACIÓN ===

MQTT_BROKER = "54.243.184.8"
MQTT_PORT = 1883
MQTT_TOPIC = "patentes/captura"

IMAGE_PATH = "/tmp/captura.jpg"
BUCKET_NAME = "esp32-captures"

rekognition = boto3.client("rekognition", region_name="us-east-1")
s3 = boto3.client("s3")

# === LÓGICA PRINCIPAL ===

def subir_imagen_a_s3(s3_image_key):
    try:
        if not os.path.exists(IMAGE_PATH):
            print("❌ No se encontró la imagen local:", IMAGE_PATH)
            return False

        print("☁️ Subiendo imagen a S3 como:", s3_image_key)
        s3.upload_file(IMAGE_PATH, BUCKET_NAME, s3_image_key)
        print("✅ Imagen subida correctamente a S3")
        return True

    except Exception as e:
        print("⚠️ Error subiendo a S3:", e)
        return False

def detectar_patente_rekognition(s3_image_key):
    try:
        print("🔎 Enviando imagen a Rekognition para detectar texto...")
        response = rekognition.detect_text(
            Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': s3_image_key}}
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
        result, _ = client.subscribe(MQTT_TOPIC)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"📡 Suscripción exitosa al topic: {MQTT_TOPIC}")
        else:
            print(f"❌ Error al suscribirse al topic {MQTT_TOPIC}. Código:", result)
    else:
        print("❌ Error de conexión MQTT. Código:", rc)

def on_message(client, userdata, msg):
    print(f"\n📥 Imagen recibida en {msg.topic}")
    print(f"📦 Tamaño del payload: {len(msg.payload)} bytes")
    try:
        with open(IMAGE_PATH, "wb") as f:
            f.write(msg.payload)
        print(f"💾 Imagen guardada como: {IMAGE_PATH}")

        # Copia local con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"captura_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(msg.payload)
        print(f"🗂️ Imagen también guardada como: {filename}")

        s3_image_key = filename

        if subir_imagen_a_s3(s3_image_key):
            patente = detectar_patente_rekognition(s3_image_key)
            if patente:
                print(f"✅ Patente detectada: {patente}")
            else:
                print("🚫 No se detectó ninguna patente")
        else:
            print("⚠️ No se pudo subir la imagen a S3, se cancela detección")

    except Exception as e:
        print("❌ Error procesando la imagen:", e)

# === INICIALIZACIÓN MQTT ===

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Conectando al broker MQTT...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print("❌ Error conectando al broker:", e)
    exit(1)

client.loop_forever()
