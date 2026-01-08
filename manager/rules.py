"""
Rules engine for AQUA_SENSE.

Evaluates incoming telemetry and triggers alerts and actuator commands.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from .storage import Storage


@dataclass
class RuleResult:
    alert_type: str
    message: str
    command_topic: Optional[str] = None
    command_payload: Optional[Dict[str, Any]] = None


class RuleEngine:
    def __init__(self, storage: Storage, water_level_threshold: int = 350, rain_threshold: int = 80):
        self.storage = storage
        self.water_level_threshold = water_level_threshold
        self.rain_threshold = rain_threshold

    def evaluate(self, telemetry: Dict[str, Any]) -> List[RuleResult]:
        """Return list of rule outcomes (alerts/commands) for given telemetry."""
        device_type = telemetry.get("deviceType")
        results: List[RuleResult] = []
        ts = telemetry.get("timestamp", datetime.utcnow().isoformat())

        if device_type == "water_sensor":
            water_level = telemetry.get("water_level_cm", 0)
            if water_level >= self.water_level_threshold:
                message = f"High water level detected: {water_level} cm"
                results.append(
                    RuleResult(
                        alert_type="FLOOD_RISK",
                        message=message,
                        command_topic=f"commands/emergency_light/{telemetry.get('deviceId', 'unknown')}",
                        command_payload={"action": "ON", "reason": "flood_risk"},
                    )
                )
        if device_type == "rain_sensor":
            rain_mm = telemetry.get("rain_mm", 0)
            if rain_mm >= self.rain_threshold:
                message = f"Heavy rainfall detected: {rain_mm} mm"
                results.append(
                    RuleResult(
                        alert_type="HEAVY_RAIN",
                        message=message,
                        command_topic="alerts/notification",
                        command_payload={
                            "deviceId": telemetry.get("deviceId", "unknown"),
                            "alertType": "HEAVY_RAIN",
                            "message": message,
                            "timestamp": ts,
                        },
                    )
                )

        # Persist alerts
        for res in results:
            self.storage.save_alert(
                alert_type=res.alert_type,
                message=res.message,
                device_id=telemetry.get("deviceId"),
                ts=ts,
                payload=telemetry,
            )
        return results


def default_engine(storage: Storage) -> RuleEngine:
    return RuleEngine(storage=storage)