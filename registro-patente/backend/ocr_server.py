import base64
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from io import BytesIO
import paho.mqtt.client as mqtt
import os
import re

# Crear carpeta de logs si no existe
os.makedirs("../logs", exist_ok=True)

# Callback al recibir mensaje
def on_message(client, userdata, msg):
    print(f"[MQTT] Mensaje recibido en {msg.topic}")
    try:
        # Decodificar imagen
        image_data = base64.b64decode(msg.payload)
        image = Image.open(BytesIO(image_data))

        # Preprocesamiento de la imagen
        image = image.convert("L")  # Escala de grises
        image = image.filter(ImageFilter.MedianFilter())  # Reducir ruido
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Aumentar contraste

        # Binarización
        image = image.point(lambda p: p > 128 and 255)
        image = ImageOps.crop(image, 10)  # Recortar bordes

        # Guardar imagen procesada
        image_path = "../logs/imagen_recibida_procesada.jpg"
        image.save(image_path)

        # OCR con configuración personalizada
        custom_oem_psm_config = r'--oem 3 --psm 6'
        raw_text = pytesseract.image_to_string(image, config=custom_oem_psm_config)

        # Buscar posibles patentes usando regex
        matches = re.findall(r'[A-Z]{2}\s?\d{3}\s?[A-Z]{2}', raw_text.upper())

        print("Texto detectado:")
        if matches:
            print(matches[0].replace(" ", ""))  # Mostrar solo la patente, sin espacios
        else:
            print("⚠️ No se encontró una patente válida.")

    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")

# Config MQTT
broker = "54.243.184.8"
topic = "patentes/captura"

client = mqtt.Client()
client.on_message = on_message

client.connect(broker, 1883, 60)
client.subscribe(topic)

print(f"[MQTT] Escuchando en topic '{topic}'...")
client.loop_forever()
