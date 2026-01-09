"""
FastAPI application exposing AQUA_SENSE northbound APIs.
"""
from __future__ import annotations
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .device_registry import registry
from .mqtt_client import manager_mqtt
from .storage import storage
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AQUA_SENSE_API")

app = FastAPI(
    title="AQUA_SENSE API",
    version="1.0.0",
    description="REST interface for the AQUA_SENSE water monitoring system.",
)
# CORS middleware for dashboard connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Device(BaseModel):
    deviceId: str
    deviceType: str
    capabilities: List[str] = []
class Command(BaseModel):
    topic: str
    payload: Dict
@app.on_event("startup")
def startup_event():
    manager_mqtt.start()
    # Register default devices
    registry.register("water-01", "water_sensor", ["telemetry"])
    registry.register("rain-01", "rain_sensor", ["telemetry"])
    registry.register("emergency-light-01", "emergency_light", ["telemetry", "commands"])
    registry.register("notification-hub-01", "notification_hub", ["commands"])
    logger.info("Startup completed")
@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/devices", response_model=List[Dict])
def list_devices():
    return registry.list_devices()
@app.post("/devices", response_model=Dict)
def register_device(device: Device):
    return registry.register(device.deviceId, device.deviceType, device.capabilities)
@app.get("/telemetry", response_model=List[Dict])
def telemetry(deviceId: Optional[str] = None, limit: int = 100):
    return storage.get_telemetry(device_id=deviceId, limit=limit)
@app.get("/alerts", response_model=List[Dict])
def alerts(limit: int = 100):
    return storage.get_alerts(limit=limit)
@app.post("/commands")
def send_command(command: Command):
    if not command.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    manager_mqtt.publish_command(command.topic, command.payload)
    return {"status": "sent"}
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("manager.api_server:app", host="0.0.0.0", port=7070, reload=True)