# api_manual_access.py
from flask import Blueprint, jsonify, request
import paho.mqtt.publish as publish
from mqtt_manual_access import manual_event

api = Blueprint("manual_api", __name__)


@api.route("/estado-solicitud", methods=["GET"])
def estado():
    return jsonify({"pendiente": manual_event["pendiente"]})


@api.route("/responder-solicitud", methods=["POST"])
def responder():
    data = request.json
    decision = data.get("autorizar", False)
    publish.single("acceso/autorizado", "true" if decision else "false", hostname="54.243.184.8")
    manual_event["pendiente"] = False
    return jsonify({"msg": "Enviado a ESP32"}), 200
