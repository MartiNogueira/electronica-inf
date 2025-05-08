import requests
import psycopg2
import boto3
import paho.mqtt.publish as publish
from datetime import datetime

# 📸 IP local de tu ESP32-CAM
ESP32_CAM_URL = "http://192.168.0.68/capture"
LOCAL_IMAGE_PATH = "/tmp/captura.jpg"
BUCKET_NAME = "esp32-captures"
S3_IMAGE_KEY = "captura.jpg"

# 🔐 Configuración base de datos
DB_CONFIG = {
    "host": "172.31.25.254",
    "user": "postgres",
    "password": "postgres",
    "dbname": "accesscontrol",
    "port": 5432
}

# MQTT broker
MQTT_BROKER = "54.243.184.8"
MQTT_TOPIC = "barrera/accion"

# AWS clients
rekognition = boto3.client("rekognition", region_name="us-east-1")
s3 = boto3.client("s3")

def capturar_y_subir_imagen():
    try:
        print("📸 Capturando imagen desde ESP32-CAM...")
        response = requests.get(ESP32_CAM_URL, timeout=10)
        if response.status_code == 200:
            with open(LOCAL_IMAGE_PATH, "wb") as f:
                f.write(response.content)
            print("✅ Imagen guardada localmente")

            s3.upload_file(LOCAL_IMAGE_PATH, BUCKET_NAME, S3_IMAGE_KEY)
            print("☁️ Imagen subida a S3")
            return True
        else:
            print("❌ Error al capturar imagen. Código:", response.status_code)
            return False
    except Exception as e:
        print("⚠️ Error capturando/subiendo imagen:", e)
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

def validar_patente(patente):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT autorizado FROM vehiculos WHERE patente = %s", (patente,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and result[0] is True:
            print("✅ Patente autorizada → abrir barrera 🚧")
            publish.single(MQTT_TOPIC, payload="abrir", hostname=MQTT_BROKER)
            print("📡 Mensaje MQTT enviado: abrir")
            return True
        else:
            print("🚫 Patente NO autorizada → acceso denegado ❌")
            return False
    except Exception as e:
        print("⚠️ Error en la base de datos:", e)
        return False

def ejecutar_flujo():
    if capturar_y_subir_imagen():
        patente = detectar_patente_rekognition()
        if patente:
            print(f"🔠 Patente detectada: {patente}")
            validar_patente(patente)
        else:
            print("🚫 No se pudo detectar ninguna patente")

if __name__ == "__main__":
    ejecutar_flujo()
