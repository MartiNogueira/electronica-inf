import psycopg2
from datetime import datetime

# 📸 Simulación de ESP32-CAM
ESP32_CAM_URL = "http://192.168.0.68/capture"  # Ya no se usa, solo decorativo

# 🔐 Conexión a la base de datos (instancia accesscontrol)
DB_CONFIG = {
    "host": "172.31.25.254",   # ⚠️ Si estás ejecutando esto desde la instancia 'prueba'
    "user": "postgres",
    "password": "postgres",            # Poné la contraseña si tu user postgres tiene
    "dbname": "accesscontrol",
    "port": 5432
}

def capture_and_validate():
    try:
        print("📸 Simulando solicitud a ESP32-CAM...")
        print("✅ Imagen capturada (mock)")

        # 🔠 Patente simulada para la prueba
        patente = "AB123CD"
        print(f"🔠 Patente detectada (mock): {patente}")

        # 🔗 Conexión a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Consulta de autorización
        cur.execute("SELECT autorizado FROM vehiculos WHERE patente = %s", (patente,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        # Resultado
        if result and result[0] is True:
            print("✅ Patente autorizada → abrir barrera 🚧")
            return True
        else:
            print("🚫 Patente NO autorizada → acceso denegado ❌")
            return False

    except Exception as e:
        print("⚠️ Error general:", e)
        return False

# 🎬 Ejecutar al correr el script
if __name__ == "__main__":
    capture_and_validate()
