import asyncio
import json
import logging
import math
import time

from app.core.config import settings
from app.mqtt.client import mqtt_client

logger = logging.getLogger(__name__)

TOPIC_TEMPLATE = "session/{session_id}/data"

_sim_tasks: dict[int, asyncio.Task] = {}


async def _simulate(session_id: int) -> None:
    topic = TOPIC_TEMPLATE.format(session_id=session_id)
    t = 0.0
    logger.info("Iniciando simulación de datos para sesión %d", session_id)
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
                "fsr": int(
                    max(0, 3000.0 * abs(math.sin(t * 0.3)) + 200.0 * math.sin(t * 2.0))
                ),
            }
            payload = json.dumps(reading)
            mqtt_client.publish(topic, payload)
            await asyncio.sleep(0.1)
            t += 0.1
    except asyncio.CancelledError:
        logger.info("Simulación detenida para sesión %d", session_id)
    except Exception as e:
        logger.error("Error en simulación sesión %d: %s", session_id, e)


async def start_simulation(session_id: int) -> None:
    if not settings.SIMULATED_DATA:
        return
    if session_id in _sim_tasks and not _sim_tasks[session_id].done():
        logger.warning("Simulación ya activa para sesión %d", session_id)
        return
    task = asyncio.create_task(_simulate(session_id))
    _sim_tasks[session_id] = task


async def stop_simulation(session_id: int) -> None:
    task = _sim_tasks.pop(session_id, None)
    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
