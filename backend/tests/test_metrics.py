import csv
from app.sessions.metrics import calculate_metrics


def _write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["ts", "ax", "ay", "az", "gx", "gy", "gz", "fsr"]
        )
        writer.writeheader()
        writer.writerows(rows)


class TestCalculateMetrics:
    def test_uniform_pressure(self, tmp_path):
        path = tmp_path / "test.csv"
        _write_csv(
            path,
            [
                {
                    "ts": i,
                    "ax": 0,
                    "ay": 0,
                    "az": 9.81,
                    "gx": 0,
                    "gy": 0,
                    "gz": 0,
                    "fsr": 500,
                }
                for i in range(10)
            ],
        )
        metrics = calculate_metrics(str(path))
        assert metrics["avg_pressure"] == 500.0
        assert metrics["max_pressure"] == 500.0
        assert metrics["pressure_stability"] == 1.0

    def test_empty_csv(self, tmp_path):
        path = tmp_path / "empty.csv"
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["ts", "ax", "ay", "az", "gx", "gy", "gz", "fsr"]
            )
            writer.writeheader()
        metrics = calculate_metrics(str(path))
        assert metrics == {}

    def test_movement_stability_range(self, tmp_path):
        path = tmp_path / "range.csv"
        _write_csv(
            path,
            [
                {
                    "ts": i,
                    "ax": 0.1,
                    "ay": 0.2,
                    "az": 9.8,
                    "gx": 0.01,
                    "gy": 0.02,
                    "gz": 0.01,
                    "fsr": 300,
                }
                for i in range(20)
            ],
        )
        metrics = calculate_metrics(str(path))
        assert 0 <= metrics["movement_stability"] <= 1
        assert 0 <= metrics["pressure_stability"] <= 1
        assert 0 <= metrics["posture_score"] <= 1

    def test_tremor_detected(self, tmp_path):
        path = tmp_path / "tremor.csv"
        _write_csv(
            path,
            [
                {
                    "ts": i,
                    "ax": 0,
                    "ay": 0,
                    "az": 9.81,
                    "gx": 5,
                    "gy": 5,
                    "gz": 5,
                    "fsr": 300,
                }
                for i in range(10)
            ],
        )
        metrics = calculate_metrics(str(path))
        assert metrics["tremor_level"] > 0
