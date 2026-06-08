import csv
import math
import statistics

FIELDS = ["ts", "ax", "ay", "az", "gx", "gy", "gz", "fsr"]


def calculate_metrics(csv_path: str) -> dict:
    readings = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append({k: float(row[k]) for k in FIELDS})

    if not readings:
        return {}

    pressures = [r["fsr"] for r in readings]
    ax_vals = [r["ax"] for r in readings]
    ay_vals = [r["ay"] for r in readings]
    az_vals = [r["az"] for r in readings]
    gx_vals = [r["gx"] for r in readings]
    gy_vals = [r["gy"] for r in readings]
    gz_vals = [r["gz"] for r in readings]

    avg_p = statistics.mean(pressures)
    max_p = max(pressures)
    std_p = statistics.stdev(pressures) if len(pressures) > 1 else 0.0

    pressure_stability = round(1 - (std_p / max_p), 4) if max_p > 0 else 1.0
    pressure_stability = max(0.0, min(1.0, pressure_stability))

    tremor_level = round(
        statistics.mean(
            [
                abs(gx) + abs(gy) + abs(gz)
                for gx, gy, gz in zip(gx_vals, gy_vals, gz_vals)
            ]
        ),
        4,
    )

    magnitudes = [
        math.sqrt(ax**2 + ay**2 + az**2)
        for ax, ay, az in zip(ax_vals, ay_vals, az_vals)
    ]
    std_mag = statistics.stdev(magnitudes) if len(magnitudes) > 1 else 0.0
    movement_stability = round(max(0.0, 1 - (std_mag / 9.81)), 4)
    movement_stability = min(1.0, movement_stability)

    # Provisional: posture basada en inclinación media del eje Z
    # Un lápiz bien sostenido tiene az ≈ 9.81
    avg_az = statistics.mean(az_vals)
    posture_score = round(max(0.0, min(1.0, avg_az / 9.81)), 4)

    return {
        "avg_pressure": round(avg_p, 4),
        "max_pressure": round(max_p, 4),
        "pressure_stability": pressure_stability,
        "movement_stability": movement_stability,
        "tremor_level": tremor_level,
        "posture_score": posture_score,
    }
