import requests
import psycopg2
import boto3
from datetime import datetime

# IP de tu ESP32-CAM
ESP32_CAM_URL = "http://192.168.0.68/capture"

# Configuración AWS Rekognition
rekognition = boto3.client("rekognition", region_name="us-east-1")
S3_BUCKET = "esp32-captures"
IMAGE_NAME = "patente.jpeg"  # ⚠️ Cambiar si subís una imagen diferente

# Configuración base de datos
DB_CONFIG = {
    "host": "172.31.25.254",
    "user": "postgres",
    "password": "",  # ⚠️ Si tiene password, ponerlo
    "dbname": "accesscontrol",
    "port": 5432
}

def detect_license_plate():
    try:
        response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": S3_BUCKET, "Name": IMAGE_NAME}}
        )

        for item in response['TextDetections']:
            if item['Type'] == 'LINE' and ' ' in item['DetectedText'] and len(item['DetectedText']) >= 7:
                patente = item['DetectedText'].replace(" ", "")
                print("🔠 Patente detectada (rekognition):", patente)
                return patente

        print("🚫 No se detectó ninguna patente válida")
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
            return True
        else:
            print("🚫 Patente NO autorizada → acceso denegado ❌")
            return False

    except Exception as e:
        print("⚠️ Error de base de datos:", e)
        return False

if __name__ == "__main__":
    print("📸 Simulando solicitud a ESP32-CAM...")
    try:
        requests.get(ESP32_CAM_URL, timeout=5)
        print("✅ Imagen capturada (simulada)")
    except:
        print("⚠️ Error al capturar imagen. Se sigue igual para pruebas")

    patente = detect_license_plate()
    if patente:
        validar_patente(patente)
