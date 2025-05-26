import base64
import boto3
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime
import os
import re

# === CONFIGURACIÓN GENERAL ===
MQTT_BROKER = "54.243.184.8"
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "patentes/captura"
MQTT_TOPIC_PUB = "acceso/autorizado"
IMAGE_PATH = os.path.join(os.getcwd(), "captura.jpg")
BUCKET_NAME = "esp32-captures"

# === CONFIGURACIÓN POSTGRES ===
DB_HOST = "172.31.25.254"   # ← IP PRIVADA de accesscontrol
DB_NAME = "accesscontrol"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_PORT = 5432

# === AWS CONFIG ===
rekognition = boto3.client("rekognition", region_name="us-east-1")
s3 = boto3.client("s3")

# === MQTT ===
client = mqtt.Client()

def guardar_imagen(payload):
    try:
        with open(IMAGE_PATH, "wb") as f:
            f.write(base64.b64decode(payload))
        print(f"✅ Imagen guardada en {IMAGE_PATH}")
        return True
    except Exception as e:
        print("❌ Error guardando imagen:", e)
        return False

def subir_imagen_a_s3(s3_key):
    try:
        s3.upload_file(IMAGE_PATH, BUCKET_NAME, s3_key)
        print(f"☁️ Imagen subida a S3 como {s3_key}")
        return s3_key
    except Exception as e:
        print("❌ Error subiendo a S3:", e)
        return None

def filtrar_patente(textos):
    patron = re.compile(r'[A-Z]{2}\d{3}[A-Z]{2}')
    for texto in textos:
        if texto["Type"] == "LINE":
            t = texto["DetectedText"].replace(" ", "").upper()
            if patron.match(t):
                print("✅ Patente detectada:", t)
                return t
    return "NO_DETECTADA"

def detectar_patente_con_rekognition(s3_key):
    try:
        response = rekognition.detect_text(Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": s3_key}})
        textos = response["TextDetections"]
        return filtrar_patente(textos)
    except Exception as e:
        print("❌ Error con Rekognition:", e)
        return "NO_DETECTADA"

def verificar_autorizacion(patente):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT autorizado FROM vehiculos WHERE patente = %s", (patente,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row and row[0] == True:
            print("✅ Patente autorizada")
            return "true"
        else:
            print("⛔ Patente no autorizada")
            return "false"
    except Exception as e:
        print("❌ Error al conectar con PostgreSQL:", e)
        return "false"

def on_message(client, userdata, msg):
    print("📥 Imagen recibida por MQTT")

    if guardar_imagen(msg.payload):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_key = f"capturas/{timestamp}.jpg"
        subir_imagen_a_s3(s3_key)

        patente = detectar_patente_con_rekognition(s3_key)
        resultado = "false" if patente == "NO_DETECTADA" else verificar_autorizacion(patente)

        print("📡 Publicando resultado:", resultado)
        client.publish(MQTT_TOPIC_PUB, resultado)

# === INICIO ===
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC_SUB)
print("🚀 Escuchando en", MQTT_TOPIC_SUB)
client.loop_forever()
