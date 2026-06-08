import csv
import math

def calculate_metrics(csv_path: str) -> dict:
    readings = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            readings.append({
                "ax": float(row["ax"]), "ay": float(row["ay"]), "az": float(row["az"]),
                "gx": float(row["gx"]), "gy": float(row["gy"]), "gz": float(row["gz"]),
                "fsr": float(row["fsr"]),
            })
    if not readings:
        return {}

    n = len(readings)
    fsr_vals = [r["fsr"] for r in readings]
    avg_p = sum(fsr_vals) / n
    max_p = max(fsr_vals)
    std_p = math.sqrt(sum((v - avg_p) ** 2 for v in fsr_vals) / n)
    p_stability = max(0.0, min(1.0, 1.0 - (std_p / avg_p if avg_p > 0 else 0.0)))

    acc_vals = [(r["ax"], r["ay"], r["az"]) for r in readings]
    am = [sum(v[i] for v in acc_vals) / n for i in range(3)]
    acc_var = sum((v[0]-am[0])**2 + (v[1]-am[1])**2 + (v[2]-am[2])**2 for v in acc_vals) / n
    m_stability = max(0.0, min(1.0, 1.0 - math.sqrt(acc_var) / 49.05))

    tremor = sum(abs(r["gx"]) + abs(r["gy"]) + abs(r["gz"]) for r in readings) / (n * 3)

    return {
        "avg_pressure": round(avg_p, 2),
        "max_pressure": round(max_p, 2),
        "pressure_stability": round(p_stability, 4),
        "movement_stability": round(m_stability, 4),
        "tremor_level": round(tremor, 4),
    }