"""
Device registry keeps metadata and last-known state for AQUA_SENSE devices.
"""
from __future__ import annotations
import threading
from datetime import datetime
from typing import Dict, List, Optional

class DeviceRegistry:
    def __init__(self) -> None:
        self._devices: Dict[str, Dict] = {}
        self._lock = threading.Lock()
    def register(self, device_id: str, device_type: str, capabilities: List[str]) -> Dict:
        with self._lock:
            device = self._devices.get(device_id, {})
            device.update(
                {
                    "deviceId": device_id,
                    "deviceType": device_type,
                    "capabilities": capabilities,
                    "lastSeen": device.get("lastSeen"),
                    "lastPayload": device.get("lastPayload"),
                }
            )
            self._devices[device_id] = device
            return device
    def update_state(self, device_id: str, payload: Dict) -> None:
        with self._lock:
            if device_id not in self._devices:
                # If not known, register with generic metadata
                self._devices[device_id] = {
                    "deviceId": device_id,
                    "deviceType": payload.get("deviceType", "unknown"),
                    "capabilities": [],
                }
            self._devices[device_id]["lastSeen"] = datetime.utcnow().isoformat()
            self._devices[device_id]["lastPayload"] = payload
    def list_devices(self) -> List[Dict]:
        with self._lock:
            return list(self._devices.values())
    def get(self, device_id: str) -> Optional[Dict]:
        with self._lock:
            return self._devices.get(device_id)
registry = DeviceRegistry()