from app.ai.rules import evaluate_realtime


class TestEvaluateRealtime:
    def test_high_pressure_triggers_alert(self):
        reading = {"fsr": 3000, "gx": 0, "gy": 0, "gz": 0}
        alerts = evaluate_realtime(reading)
        assert any(a["id"] == "presion_excesiva" for a in alerts)

    def test_no_alerts_on_normal_reading(self):
        reading = {"fsr": 800, "gx": 0.1, "gy": 0.1, "gz": 0.0}
        alerts = evaluate_realtime(reading)
        assert alerts == []

    def test_low_pressure_triggers_alert(self):
        reading = {"fsr": 100, "gx": 0, "gy": 0, "gz": 0}
        alerts = evaluate_realtime(reading)
        assert any(a["id"] == "presion_insuficiente" for a in alerts)

    def test_high_tremor_triggers_alert(self):
        reading = {"fsr": 500, "gx": 1.0, "gy": 0.5, "gz": 0.3}
        alerts = evaluate_realtime(reading)
        assert any(a["id"] == "temblor_alto" for a in alerts)

    def test_reading_with_zero_fsr_does_not_trigger_low_pressure(self):
        reading = {"fsr": 0, "gx": 0, "gy": 0, "gz": 0}
        alerts = evaluate_realtime(reading)
        assert not any(a["id"] == "presion_insuficiente" for a in alerts)

    def test_multiple_alerts_can_trigger(self):
        reading = {"fsr": 3000, "gx": 1.0, "gy": 0.5, "gz": 0.3}
        alerts = evaluate_realtime(reading)
        ids = [a["id"] for a in alerts]
        assert "presion_excesiva" in ids
        assert "temblor_alto" in ids
