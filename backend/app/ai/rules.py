from typing import Any

REALTIME_RULES = [
    {
        "id": "presion_excesiva",
        "condition": lambda r: r.get("fsr", 0) > 2500,
        "feedback": "Estás presionando demasiado fuerte. Relaja la mano.",
        "severity": "warning",
    },
    {
        "id": "presion_insuficiente",
        "condition": lambda r: 0 < r.get("fsr", 0) < 150,
        "feedback": "Presiona un poco más para que el trazo sea visible.",
        "severity": "info",
    },
    {
        "id": "temblor_alto",
        "condition": lambda r: (
            abs(r.get("gx", 0)) + abs(r.get("gy", 0)) + abs(r.get("gz", 0)) > 1.5
        ),
        "feedback": "Intenta mover el lápiz más despacio y con más control.",
        "severity": "warning",
    },
]


def evaluate_realtime(reading: dict[str, Any]) -> list[dict[str, Any]]:
    triggered = []
    for rule in REALTIME_RULES:
        try:
            if rule["condition"](reading):
                triggered.append(
                    {
                        "id": rule["id"],
                        "feedback": rule["feedback"],
                        "severity": rule["severity"],
                    }
                )
        except Exception:
            pass
    return triggered
