import argparse
import json
import math
import time

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument("--session-id", type=int, default=13)
parser.add_argument("--broker", default="localhost")
parser.add_argument("--port", type=int, default=1883)
args = parser.parse_args()

BROKER = args.broker
PORT = args.port
SESSION_ID = args.session_id
TOPIC = f"session/{SESSION_ID}/data"

SEND_CSV = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Conectado al broker MQTT en {BROKER}:{PORT}")
    else:
        print(f"Error de conexión: {reason_code}")


client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()

fmt = "CSV" if SEND_CSV else "JSON"
print(f"Publicando en {TOPIC} como {fmt}")
t = 0.0

try:
    while True:
        reading = {
            "ts": int(time.time() * 1000),
            "ax": round(1.5 * math.sin(t), 3),
            "ay": round(0.8 * math.cos(t * 0.7), 3),
            "az": round(9.81 + 0.3 * math.sin(t * 0.3), 3),
            "gx": round(0.02 * math.sin(t * 2), 3),
            "gy": round(0.015 * math.cos(t * 1.5), 3),
            "gz": round(0.005 * math.sin(t * 0.5), 3),
            "fsr": int(max(0, 3000.0 * abs(math.sin(t * 0.3)) + 200.0 * math.sin(t * 2.0))),
        }
        if SEND_CSV:
            payload = (
                f"{reading['ts']},{reading['ax']},{reading['ay']},{reading['az']},"
                f"{reading['gx']},{reading['gy']},{reading['gz']},{reading['fsr']}"
            )
        else:
            payload = json.dumps(reading)
        client.publish(TOPIC, payload)
        print(f"{payload}")
        time.sleep(0.1)
        t += 0.1
except KeyboardInterrupt:
    print("\nDetenido.")
    client.loop_stop()
    client.disconnect()
