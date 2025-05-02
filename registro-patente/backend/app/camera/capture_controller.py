import requests
import psycopg2
from datetime import datetime

# IP de tu ESP32-CAM (reemplazar si es distinta)
ESP32_CAM_URL = "http://192.168.0.68/capture"

# IP privada de la instancia que tiene la base de datos (accesscontrol)
DB_CONFIG = {
    "host": "172.31.25.254",  # IP privada de accesscontrol
    "user": "postgres",
    "password": "",           # dejar vacío si no tiene contraseña
    "dbname": "accesscontrol",
    "port": 5432
}

def capture_and_validate():
    try:
        print("📸 Solicitando imagen a ESP32-CAM...")
        response = requests.get(ESP32_CAM_URL, timeout=10, stream=True)

        if response.status_code != 200:
            print("❌ Error al capturar imagen")
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"✅ Imagen capturada (mock): capture_{timestamp}.jpg")

        # Simulación de patente detectada
        patente = "AB123CD"
        print(f"🔠 Patente detectada (mock): {patente}")

        # Conexión a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Verificamos si está autorizada
        cur.execute("SELECT autorizado FROM vehiculos WHERE patente = %s", (patente,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result and result[0] is True:
            print("✅ Patente autorizada → abrir barrera")
            return True
        else:
            print("🚫 Patente NO autorizada")
            return False

    except Exception as e:
        print("⚠️ Error general:", e)
        return False
if __name__ == "__main__":
    capture_and_validate()
