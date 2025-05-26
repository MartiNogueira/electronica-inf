# mqtt_manual_access.py
import paho.mqtt.client as mqtt

manual_event = {"pendiente": False}


def on_message(client, userdata, msg):
    if msg.topic == "acceso/manual":
        print("🔔 Solicitud manual recibida")
        manual_event["pendiente"] = True


client = mqtt.Client()
client.on_message = on_message
client.connect("54.243.184.8", 1883)
client.subscribe("acceso/manual")
client.loop_start()
