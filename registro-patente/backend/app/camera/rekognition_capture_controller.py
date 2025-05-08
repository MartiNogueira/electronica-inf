import requests
import psycopg2
import boto3
import paho.mqtt.publish as publish
from datetime import datetime
import json

# 📸 IP local de tu ESP32-CAM
ESP32_CAM_URL = "http://192.168.0.68/capture"

# 🔐 Conexión a la base de datos
DB_CONFIG = {
    "host": "172.31.25.254",
    "user": "postgres",
    "password": "postgres",
    "dbname": "accesscontrol",
    "port": 5432
}

# AWS Rekognition config
rekognition = boto3.client('rekognition', region_name='us-east-1')
BUCKET_NAME = 'esp32-captures'
IMAGE_NAME = 'patente.jpeg'

# MQTT config
MQTT_BROKER = "54.243.184.8"  # IP pública o privada del broker MQTT
MQTT_TOPIC = "barrera/accion"


def detectar_patente_rekognition():
    try:
        response = rekognition.detect_text(
            Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': IMAGE_NAME}}
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

def capture_and_validate():
    try:
        print("📸 Simulando solicitud a ESP32-CAM...")
        try:
            requests.get(ESP32_CAM_URL, timeout=5)
        except:
            print("⚠️ Error al capturar imagen. Se sigue igual para pruebas")

        patente = detectar_patente_rekognition()
        if not patente:
            print("🚫 No se detectó ninguna patente válida")
            return False

        print(f"🔠 Patente detectada (rekognition): {patente}")

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
        print("⚠️ Error general:", e)
        return False

if __name__ == "__main__":
    capture_and_validate()
