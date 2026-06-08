import json
import logging
from contextlib import asynccontextmanager
from typing import Any

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.mqtt.schemas import IMUReading
from app.sessions.buffer import session_buffer

logger = logging.getLogger(__name__)

TOPIC = "session/+/data"


def parse_payload(payload: str) -> dict[str, Any]:
    stripped = payload.strip()
    if stripped.startswith("{"):
        return json.loads(stripped)
    parts = stripped.split(",")
    if len(parts) != 8:
        raise ValueError(f"Esperados 8 campos CSV, recibidos {len(parts)}")
    return {
        "ts": int(parts[0]),
        "ax": float(parts[1]),
        "ay": float(parts[2]),
        "az": float(parts[3]),
        "gx": float(parts[4]),
        "gy": float(parts[5]),
        "gz": float(parts[6]),
        "fsr": int(parts[7]),
    }


def extract_session_id(topic: str) -> int:
    parts = topic.split("/")
    return int(parts[1])


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info(
            f"MQTT conectado al broker {settings.MQTT_BROKER}:{settings.MQTT_PORT}"
        )
        client.subscribe(TOPIC)
        logger.info(f"MQTT suscrito a {TOPIC}")
    else:
        logger.error(f"MQTT error de conexión: {reason_code}")


def on_message(client, userdata, msg):
    try:
        raw = parse_payload(msg.payload.decode())
        reading = IMUReading(**raw)
        session_id = extract_session_id(msg.topic)
        session_buffer.append(session_id, reading.model_dump())
    except Exception as e:
        logger.warning(f"MQTT mensaje inválido en {msg.topic}: {e}")


mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


@asynccontextmanager
async def lifespan_mqtt():
    logger.info("Iniciando cliente MQTT...")
    try:
        mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
        mqtt_client.loop_start()
    except Exception as e:
        logger.error(f"MQTT no pudo conectar: {e}")
    yield
    logger.info("Deteniendo cliente MQTT...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
