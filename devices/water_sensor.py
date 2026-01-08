"""
Watwer Level Sensor Emulator

THis module simulates an IOT water level sensor.The device periodically generates
synthetic water level mesurements (in centimeters) and publishes them as telemetry
events to an MQTT broker. The sensor is part of the AQUA-SENSE flood monitoring system.
"""
import paho.mqtt.client as mqtt
import time
import random
import json
import threading
import logging
from configparser import ConfigParser
from datetime import datetime
import signal
import argparse
from logging.handlers import RotatingFileHandler
# Global variables
config = None
mqtt_client = None
logger = None
stop_event = threading.Event()

# Function to load configuration
def load_config(config_file):
    parser = ConfigParser()
    parser.read(config_file)
    return parser
# Function to setup logging
def setup_logging(log_file, log_level):
    logger = logging.getLogger("WaterSensor")
    logger.setLevel(log_level)
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
# Function to connect to MQTT broker
def connect_mqtt(broker, port, username, password):
    client = mqtt.Client()
    if username and password:
        client.username_pw_set(username, password)
    client.connect(broker, port, 60)
    return client
# Function to publish water level data
def publish_water_level_data():
    global mqtt_client, config, logger, stop_event
    topic = config.get('MQTT', 'topic', fallback='telemetry/water/{device_id}')
    interval = config.getint('SENSOR', 'interval', fallback=10)
    while not stop_event.is_set():
        water_level_cm = random.randint(0, 500)
        data = {
            "deviceId": config.get('DEVICE', 'id', fallback='water-01'),
            "deviceType": "water_sensor",
            "timestamp": datetime.utcnow().isoformat(),
            "water_level_cm": water_level_cm
        }
        payload = json.dumps(data)
        mqtt_client.publish(topic.format(device_id=data["deviceId"]), payload, qos=1)
        logger.info(f"Published water level data: {payload}")
        stop_event.wait(interval)
# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    global stop_event, logger
    logger.info("Shutdown signal received. Stopping water sensor...")
    stop_event.set()
# Main function
def main():
    global config, mqtt_client, logger
    parser = argparse.ArgumentParser(description="Water Level Sensor Emulator")
    parser.add_argument('--config', type=str, default='config.ini', help='Path to configuration file')
    args = parser.parse_args()
    config = load_config(args.config)
    log_file = config.get('LOGGING', 'file', fallback='water_sensor.log')
    log_level_str = config.get('LOGGING', 'level', fallback='INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger = setup_logging(log_file, log_level)
    broker = config.get('MQTT', 'broker', fallback='localhost')
    port = config.getint('MQTT', 'port', fallback=1883)
    username = config.get('MQTT', 'username', fallback=None)
    password = config.get('MQTT', 'password', fallback=None)
    mqtt_client = connect_mqtt(broker, port, username, password)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info("Starting Water Level Sensor Emulator...")
    publish_water_level_data()
    logger.info("Water Level Sensor Emulator stopped.")
if __name__ == "__main__":
    main()    