import paho.mqtt.client as mqtt

# Dirección del broker MQTT y tópico
broker = "54.243.184.8"
topic = "XJXT06/aleatorio"

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado al broker con código {rc}")
    client.subscribe(topic)
    print(f"Suscripto al tópico: {topic}")

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

# Crear cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker
client.connect(broker, 1883, 60)

# Mantener el cliente activo
client.loop_forever()
