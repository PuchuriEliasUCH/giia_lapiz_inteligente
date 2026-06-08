import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Any

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.mqtt.schemas import IMUReading
from app.sessions.buffer import session_buffer
from app.sessions.watchdog import update_last_seen
from app.ai.rules import evaluate_realtime
from app.websocket.manager import manager

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


async def _handle_message(topic: str, payload: bytes) -> None:
    try:
        raw = parse_payload(payload.decode())
        reading = IMUReading(**raw).model_dump()
        session_id = extract_session_id(topic)

        session_buffer.append(session_id, reading)
        update_last_seen(session_id)

        alerts = evaluate_realtime(reading)
        if alerts and manager.is_connected(session_id):
            for alert in alerts:
                await manager.send(session_id, alert)
    except Exception as e:
        logger.warning(f"MQTT mensaje inválido en {topic}: {e}")


def on_message(client, userdata, msg):
    loop = userdata.get("loop") if isinstance(userdata, dict) else None
    if loop is None:
        return
    asyncio.run_coroutine_threadsafe(_handle_message(msg.topic, msg.payload), loop)


mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


@asynccontextmanager
async def lifespan_mqtt():
    logger.info("Iniciando cliente MQTT...")
    mqtt_client.user_data_set({"loop": asyncio.get_event_loop()})
    try:
        mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
        mqtt_client.loop_start()
    except Exception as e:
        logger.error(f"MQTT no pudo conectar: {e}")
    yield
    logger.info("Deteniendo cliente MQTT...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
