"""
MQTT bridge for AQUA_SENSE manager.

Listens to telemetry topics, stores data, evaluates rules, and publishes commands.
"""
from __future__ import annotations

import json
import logging
import threading
from typing import Callable, Optional

import paho.mqtt.client as mqtt

from .device_registry import registry
from .rules import RuleEngine, default_engine
from .storage import storage

logger = logging.getLogger("ManagerMQTT")


class ManagerMQTT:
    def __init__(
        self,
        broker: str = "localhost",
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
        telemetry_topic: str = "telemetry/+/+",
        engine_factory: Callable[[any], RuleEngine] = default_engine,
    ):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.telemetry_topic = telemetry_topic
        self.client = mqtt.Client()
        self.engine = engine_factory(storage)
        self._lock = threading.Lock()

    def start(self) -> None:
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(self.broker, self.port, 60)
        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        thread.start()
        logger.info("Manager MQTT bridge started")

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT broker with result code %s", rc)
        client.subscribe(self.telemetry_topic)
        logger.info("Subscribed to telemetry topic pattern %s", self.telemetry_topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            device_id = payload.get("deviceId", "unknown")
            device_type = payload.get("deviceType", "unknown")
            ts = payload.get("timestamp")

            storage.save_telemetry(device_id, device_type, ts, payload)
            registry.update_state(device_id, payload)

            results = self.engine.evaluate(payload)
            for res in results:
                if res.command_topic and res.command_payload is not None:
                    self.client.publish(res.command_topic, json.dumps(res.command_payload), qos=1)
                    logger.info("Published command to %s: %s", res.command_topic, res.command_payload)
        except Exception as exc:
            logger.exception("Error handling MQTT message: %s", exc)

    def publish_command(self, topic: str, payload: dict) -> None:
        with self._lock:
            self.client.publish(topic, json.dumps(payload), qos=1)
            logger.info("Manual command published to %s: %s", topic, payload)


manager_mqtt = ManagerMQTT()