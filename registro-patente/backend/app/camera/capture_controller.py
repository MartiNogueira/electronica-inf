import psycopg2
from datetime import datetime
import paho.mqtt.publish as publish

# 📸 Simulación de ESP32-CAM
ESP32_CAM_URL = "http://192.168.0.68/capture"  # No se usa, simulación

# 🔐 Conexión a la base de datos
DB_CONFIG = {
    "host": "172.31.25.254",  # IP privada de accesscontrol
    "user": "postgres",
    "password": "postgres",  # ← reemplazá con tu contraseña real
    "dbname": "accesscontrol",
    "port": 5432
}

# 🌐 Configuración del broker MQTT
MQTT_BROKER = "54.243.184.8"  # por ejemplo, 172.31.xx.xx
MQTT_PORT = 1883
MQTT_TOPIC = "barrera/accion"

def capture_and_validate():
    try:
        print("📸 Simulando solicitud a ESP32-CAM...")
        print("✅ Imagen capturada (mock)")

        patente = "AB123CD"
        print(f"🔠 Patente detectada (mock): {patente}")

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT autorizado FROM vehiculos WHERE patente = %s", (patente,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result and result[0] is True:
            print("✅ Patente autorizada → abrir barrera 🚧")

            # Publicar en MQTT
            publish.single(MQTT_TOPIC, payload="abrir", hostname=MQTT_BROKER, port=MQTT_PORT)
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
